"""Resets a HIDSL installation."""

from argparse import ArgumentParser, Namespace
from itertools import chain
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from subprocess import CalledProcessError
from sys import exit    # pylint: disable=W0622

from hidsl.exceptions import NotAMountPointOrBlockDevice
from hidsl.fstab import FSTAB
from hidsl.functions import chroot
from hidsl.hostid import HOST_ID, HOSTNAME, MACHINE_ID
from hidsl.initcpio import INITRAMFS
from hidsl.logging import FORMAT, LOGGER
from hidsl.mount import EnsuredMountpoint
from hidsl.openvpn import delete_client_config
from hidsl.ssh import HOST_KEYS
from hidsl.syslinux import AUTOUPDATE
from hidsl.systemd import vacuum, disable, enable
from hidsl.types import Glob
from hidsl.users import rmdotfiles


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
    parser.add_argument('target', type=Path, default=MOUNTPOINT,
                        help='the target system')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not beep after completion')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
    return parser.parse_args()


def reset(mountpoint: Path, args: Namespace):
    """Performs the reset."""

    LOGGER.info('Disabling application.service.')
    disable(APPLICATION, root=mountpoint, verbose=args.verbose)
    LOGGER.info('Enabling unconfigured-warning.service.')
    enable(WARNING, root=mountpoint, verbose=args.verbose)
    LOGGER.info('Removing OpenVPN client configuration.')
    delete_client_config(root=mountpoint)
    remove_globs = [
        Glob(chroot(args.chroot, glob.path), glob.glob)
        for glob in REMOVE_GLOBS
    ]

    for path in chain(REMOVE_FILES, *remove_globs):
        LOGGER.info('Removing: %s', path)
        chroot(mountpoint, path).unlink()

    LOGGER.info('Clearing journal.')
    vacuum(root=mountpoint, verbose=args.verbose)
    LOGGER.info('removing dotfiles.')
    rmdotfiles(root=mountpoint)


def main():
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    try:
        with EnsuredMountpoint(args.target) as mountpoint:
            reset(mountpoint, args)
    except NotAMountPointOrBlockDevice:
        LOGGER.error('Target %s is neither a mount point, nor a block device.',
                     args.target)
        exit(1)
    except CalledProcessError as error:
        LOGGER.critical('Subprocess error.')
        LOGGER.error(error)
        exit(error.returncode)
