"""Resets a HIDSL installation."""

from argparse import ArgumentParser, Namespace
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from sys import exit    # pylint: disable=W0622
from typing import Iterator

from hidsltools.errorhandler import ErrorHandler
from hidsltools.fstab import FSTAB
from hidsltools.functions import chroot
from hidsltools.hostid import HOST_ID, HOSTNAME, MACHINE_ID
from hidsltools.initcpio import INITRAMFS
from hidsltools.logging import FORMAT, LOGGER
from hidsltools.openvpn import delete_client_config
from hidsltools.pacman import clean
from hidsltools.ssh import HOST_KEYS
from hidsltools.syslinux import AUTOUPDATE
from hidsltools.systemd import vacuum, disable, enable
from hidsltools.types import Glob
from hidsltools.users import rmdotfiles


__all__ = ['main']


APPLICATION = 'application.service'
DESCRIPTION = 'Resets operating system for image creation.'
WARNING = 'unconfigured-warning.service'
MOUNTPOINT = Path('/mnt')
REMOVE_FILES = [AUTOUPDATE, FSTAB, HOST_ID, HOSTNAME, MACHINE_ID]
REMOVE_GLOBS = [INITRAMFS, HOST_KEYS]


def get_args() -> Namespace:
    """Returns the CLI arguments."""

    parser = ArgumentParser(description=DESCRIPTION)
    parser.add_argument('root', type=Path, default=MOUNTPOINT,
                        help='the target system')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not beep after completion')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
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
        LOGGER.error('Specified root is not a mount point.')
        return 1

    LOGGER.info('Disabling application.service.')
    disable(APPLICATION, root=args.root, verbose=args.verbose)
    LOGGER.info('Enabling unconfigured-warning.service.')
    enable(WARNING, root=args.root, verbose=args.verbose)
    LOGGER.info('Removing OpenVPN client configuration.')
    delete_client_config(root=args.root)

    for file in get_files_to_be_removed(args.root):
        LOGGER.info('Removing: %s', file)
        file.unlink(missing_ok=True)

    LOGGER.info('Clearing journal.')
    vacuum(root=args.root, verbose=args.verbose)
    LOGGER.info('Cleaning up package cache.')
    clean(root=args.root)
    LOGGER.info('Removing dotfiles.')
    rmdotfiles(root=args.root)
    return 0


def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    with ErrorHandler(LOGGER):
        exit(reset(args))
