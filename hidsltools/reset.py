"""Resets a HIDSL installation."""

from argparse import ArgumentParser, Namespace
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from subprocess import CalledProcessError
from typing import Iterator

from hidsltools.errorhandler import ErrorHandler
from hidsltools.fstab import FSTAB
from hidsltools.functions import chroot
from hidsltools.hostid import HOST_ID, HOSTNAME, MACHINE_ID
from hidsltools.initcpio import INITRAMFS
from hidsltools.logging import FORMAT, LOGGER
from hidsltools.openvpn import delete_client_config
from hidsltools.pacman import CACHED_PKGS, LOCKFILE, clean
from hidsltools.ssh import HOST_KEYS
from hidsltools.syslinux import AUTOUPDATE
from hidsltools.systemd import CORE_DUMPS, JOURNALS, vacuum, disable, enable
from hidsltools.types import Glob
from hidsltools.users import clean_homes


__all__ = ["main"]


SYSTEMD_UNITS_TO_DISABLE = {
    "application.service",
    "chromium.service",
    "html5ds.service",
    "installation-instructions.service",
}
DESCRIPTION = "Resets operating system for image creation."
WARNING = "unconfigured-warning.service"
MOUNTPOINT = Path("/mnt")
REMOVE_FILES = [AUTOUPDATE, FSTAB, HOST_ID, HOSTNAME, LOCKFILE, MACHINE_ID]
REMOVE_GLOBS = [CACHED_PKGS, CORE_DUMPS, HOST_KEYS, INITRAMFS, JOURNALS]


def get_args() -> Namespace:
    """Returns the CLI arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument("root", type=Path, default=MOUNTPOINT, help="the target system")
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="do not beep after completion"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show output of subprocesses"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="do not error out if root is not a mountpoint",
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable verbose logging"
    )
    parser.add_argument(
        "-h", "--home", action="store_true", help="dont delete home directory"
    )
    return parser.parse_args()


def get_files_to_be_removed(root: Path) -> Iterator[Path]:
    """Yields files to be removed."""

    for file in REMOVE_FILES:
        yield chroot(root, file)

    for glob in REMOVE_GLOBS:
        for file in Glob(chroot(root, glob.path), glob.glob):
            yield file


def reset(args: Namespace) -> int:
    """Performs the reset."""

    if not args.root.is_mount():
        if not args.force:
            LOGGER.error("Specified root is not a mount point.")
            return 1

        LOGGER.warning("Specified root is not a mount point.")

    for systemd_unit in SYSTEMD_UNITS_TO_DISABLE:
        LOGGER.info("Disabling %s.", systemd_unit)

        try:
            disable(systemd_unit, root=args.root, verbose=args.verbose)
        except CalledProcessError as error:
            if error.returncode != 1:  # Ignore non-existent units
                raise

    LOGGER.info("Enabling unconfigured-warning.service.")
    enable(WARNING, root=args.root, verbose=args.verbose)
    LOGGER.info("Removing OpenVPN client configuration.")
    delete_client_config(root=args.root)

    for file in get_files_to_be_removed(args.root):
        LOGGER.info("Removing: %s", file)
        file.unlink(missing_ok=True)

    LOGGER.info("Clearing journal.")
    vacuum(root=args.root, verbose=args.verbose)
    LOGGER.info("Cleaning up package cache.")
    clean(root=args.root, verbose=args.verbose)
    if not args.home:
        LOGGER.info("Cleaning up home folders.")
        clean_homes(root=args.root)
    else:
        LOGGER.info("Dont clean home directories.")
    return 0


def main() -> int:
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    with ErrorHandler(LOGGER):
        return reset(args)
