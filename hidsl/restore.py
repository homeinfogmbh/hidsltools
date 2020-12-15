"""Resores HIDSL images."""

from argparse import ArgumentParser, Namespace
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from subprocess import CalledProcessError
from sys import exit    # pylint: disable=W0622
from tempfile import TemporaryDirectory

from hidsl.beep import beep
from hidsl.bsdtar import extract
from hidsl.device import Device
from hidsl.defaults import DEVICE, IMAGE
from hidsl.fstab import genfstab
from hidsl.hostid import mkhostid
from hidsl.initcpio import mkinitcpio
from hidsl.logging import FORMAT, LOGGER
from hidsl.mkfs import mkfs
from hidsl.mount import MountContext
from hidsl.sgdisk import mkparts
from hidsl.ssh import generate_host_keys
from hidsl.syslinux import install_update
from hidsl.wipefs import wipefs


__all__ = ['main']


def get_args() -> Namespace:
    """Returns the CLI arguments."""

    parser = ArgumentParser(description='Restore operating system images.')
    parser.add_argument('device', nargs='?', type=Device,
                        default=DEVICE, help='target device')
    parser.add_argument('-i', '--image', type=Path, metavar='file',
                        default=IMAGE, help='image file')
    parser.add_argument('-r', '--root', type=Path, metavar='mountpoint',
                        help='target root directory')
    parser.add_argument('-w', '--wipefs', action='store_true',
                        help='wipe filesystems before partitioning')
    parser.add_argument('-m', '--mbr', action='store_true',
                        help='perform an MBR instead of an EFI installation')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not beep after completion')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
    return parser.parse_args()


def restore_image(image: Path, mountpoint: Path, verbose: bool = False):
    """Restores an image."""

    extract(image, mountpoint, verbose=verbose)
    mkhostid(root=mountpoint)
    generate_host_keys(root=mountpoint, verbose=verbose)
    genfstab(root=mountpoint, verbose=verbose)
    install_update(chroot=mountpoint, verbose=verbose)
    mkinitcpio(chroot=mountpoint, verbose=verbose)


def restore(args: Namespace):
    """Restores the HIDSL image."""

    if args.root:
        restore_image(args.image, args.root, verbose=args.verbose)
        return

    if args.wipefs:
        wipefs(args.device, verbose=args.verbose)

    LOGGER.info('Partitioning disk: %s', args.device)
    partitions = set(mkparts(args.device, mbr=args.mbr, verbose=args.verbose))
    LOGGER.debug('Created partitions: %s', partitions)
    LOGGER.info('Creating file systems.')

    for partition in partitions:
        LOGGER.debug('Formatting %s with %s.', partition.device,
                     partition.filesystem)
        mkfs(partition.device, partition.filesystem)

    LOGGER.info('Mounting partitions.')

    with TemporaryDirectory() as tmpd:
        with MountContext(tmpd, partitions) as mountpoint:
            restore_image(args.image, mountpoint, verbose=args.verbose)


def main():
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    try:
        restore(args)

        if args.beep:
            beep()
    except CalledProcessError as error:
        LOGGER.critical('Subprocess error.')
        LOGGER.error(error)
        exit(error.returncode)
