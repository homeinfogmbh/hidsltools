"""Resores HIDSL images."""

from argparse import Namespace
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from sys import exit    # pylint: disable=W0622
from tempfile import TemporaryDirectory

from hidsl.argparse import get_args
from hidsl.bsdtar import extract
from hidsl.logging import FORMAT, LOGGER
from hidsl.mkfs import Filesystem, mkfs
from hidsl.mount import MountContext, Partition
from hidsl.sgdisk import mkparts


__all__ = ['main']


def restore_image(image: Path, mountpoint: Path, verbose: bool = False):
    """Restores an image."""

    extract(image, mountpoint, verbose=verbose)
    mkhostid(root=mountpoint)
    generate_ssh_host_keys(root=mountpoint)
    genfstab(root=mountpoint)
    syslinux_install_update(chroot=mountpoint)
    mkinitcpio(chroot=mountpoint)


def restore(args: Namespace) -> int:
    """Restores the HIDSL image."""

    if args.root:
        return restore_image(args.image, args.root, verbose=args.verbose)

    if args.wipefs:
        wipefs(args.device, verbose=args.verbose)

    LOGGER.info('Partitioning disk: %s', args.device)
    first, *other = mkparts(args.device, mbr=args.mbr, verbose=args.verbose)
    LOGGER.debug('Created partitions: %s', [first, *other])

    if other:
        partitions = [
            Partition('/', other[0], Filesystem.EXT4),
            Partition('/boot', first, Filesystem.FAT32)
        ]
    else:
        partitions = [Partition('/', first, Filesystem.EXT4)]

    LOGGER.info('Creating file systems.')

    for partition in partitions:
        LOGGER.debug('Formatting %s with %s.', partition.device,
                     partition.filesystem)
        mkfs(partition.device, partition.filesystem)

    LOGGER.info('Mounting partitions.')

    with TemporaryDirectory() as tmpd:
        with MountContext(tmpd, partitions) as mountpoint:
            return restore_image(args.image, mountpoint, verbose=args.verbose)


def main():
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)
    retval = restore(args)

    if args.beep:
        beep()

    exit(retval)
