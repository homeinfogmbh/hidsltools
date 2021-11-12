"""Restores HIDSL images."""

from argparse import ArgumentParser, Namespace
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Optional

from hidsltools.beep import beep
from hidsltools.bsdtar import extract
from hidsltools.device import Device
from hidsltools.defaults import DEVICE, IMAGE, SSH_KEYS
from hidsltools.errorhandler import ErrorHandler
from hidsltools.fstab import genfstab
from hidsltools.hostid import mkhostid
from hidsltools.initcpio import mkinitcpio
from hidsltools.logging import FORMAT, LOGGER
from hidsltools.mkfs import mkfs
from hidsltools.mount import MountContext
from hidsltools.sgdisk import mkparts
from hidsltools.ssh import generate_host_keys, restore_authorized_keys
from hidsltools.syslinux import install_update
from hidsltools.wipefs import wipefs


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
    parser.add_argument('-s', '--ssh-keys', type=Path, metavar='file',
                        default=SSH_KEYS,
                        help='restore SSH keys from this JSON file')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='do not beep after completion')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
    return parser.parse_args()


def restore_image(args: Namespace, mountpoint: Optional[Path] = None) -> None:
    """Restores an image."""

    if mountpoint is None:
        mountpoint = args.root

    LOGGER.info('Extracting image archive.')
    extract(args.image, mountpoint, verbose=args.verbose)
    LOGGER.info('Creating a unique host ID.')
    mkhostid(root=mountpoint)
    LOGGER.info('Generating SSH host keys.')
    generate_host_keys(root=mountpoint, verbose=args.verbose)
    LOGGER.info('Restoring SSH keys.')
    restore_authorized_keys(args.ssh_keys, root=mountpoint)
    LOGGER.info('Generating fstab.')
    genfstab(root=mountpoint, verbose=args.verbose)

    if args.mbr:
        LOGGER.info('Installing syslinux.')
        install_update(chroot=mountpoint, verbose=args.verbose)

    LOGGER.info('Generating initramfs.')
    mkinitcpio(chroot=mountpoint, verbose=args.verbose)


def restore(args: Namespace) -> None:
    """Restores the HIDSL image."""

    if args.root:
        restore_image(args)
        return

    if not args.device.is_block_device():
        LOGGER.critical('%s is not a block device.', args.device)

    if args.wipefs:
        LOGGER.info('Wiping file systems: %s', args.device)
        wipefs(args.device, verbose=args.verbose)

    LOGGER.info('Partitioning disk: %s', args.device)
    partitions = []

    for partition in mkparts(args.device, efi=not args.mbr,
                             verbose=args.verbose):
        partitions.append(partition)
        LOGGER.debug('Created partition: %s', partition)

    LOGGER.info('Creating file systems.')

    for partition in partitions:
        LOGGER.info('Formatting %s with %s as %s.', partition.device,
                    partition.filesystem, partition.label)
        mkfs(partition.device, partition.filesystem, label=partition.label,
             verbose=args.verbose)

    LOGGER.info('Mounting partitions.')

    with TemporaryDirectory() as tmpd:
        with MountContext(partitions, root=tmpd) as mountpoint:
            restore_image(args, mountpoint=mountpoint)


def main() -> None:
    """Runs the script."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    with ErrorHandler(LOGGER):
        restore(args)

        if not args.quiet:
            beep()
