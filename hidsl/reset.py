"""Resets a HIDSL installation."""

from argparse import ArgumentParser, Namespace
from itertools import chain
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from subprocess import CalledProcessError
from sys import exit    # pylint: disable=W0622

from hidsl.digsig import rmdotfiles
from hidsl.fstab import FSTAB
from hidsl.functions import chroot
from hidsl.hostid import HOST_ID, HOSTNAME, MACHINE_ID
from hidsl.initcpio import INITRAMFS
from hidsl.logging import FORMAT, LOGGER
from hidsl.openvpn import delete_client_config
from hidsl.ssh import HOST_KEYS
from hidsl.syslinux import AUTOUPDATE
from hidsl.systemd import vacuum, disable, enable


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
    parser.add_argument('mountpoint', nargs='?', type=Path,
                        default=MOUNTPOINT, help="the target system's root")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not beep after completion')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
    return parser.parse_args()


def reset(args: Namespace):
    """Performs the reset."""

    LOGGER.info('Disabling application.service.')
    disable(APPLICATION, root=args.mountpoint, verbose=args.verbose)
    LOGGER.info('Enabling unconfigured-warning.service.')
    enable(WARNING, root=args.mountpoint, verbose=args.verbose)
    LOGGER.info('Removing OpenVPN client configuration.')
    delete_client_config(root=args.mountpoint)

    for path in chain(REMOVE_FILES, *REMOVE_GLOBS):
        LOGGER.info('Removing: %s', path)
        chroot(args.mountpoint, path).unlink()

    LOGGER.info('Clearing journal.')
    vacuum(root=args.mountpoint, verbose=args.verbose)
    LOGGER.info('removing dotfiles.')
    rmdotfiles(root=args.mountpoint)


def main():
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    try:
        reset(args)
    except CalledProcessError as error:
        LOGGER.critical('Subprocess error.')
        LOGGER.error(error)
        exit(error.returncode)
