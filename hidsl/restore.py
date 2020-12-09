"""Resores HIDSL images."""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from sys import exit

from hidsl.device import Device
from hidsl.logging import LOGGER
from hidsl.mkfs import Filesystem, mkfs
from hidsl.mount import MountContext, Partition


DEFAULT_DEVICE = Device('/dev/sda')
DEFAULT_IMAGE = Path('/opt/hidsl/ddb.bsdtar.lzop')


def get_args() -> Namespace:
    """Returns the CLI arguments."""

    parser = ArgumentParser(description='Restore operating system images.')
    parser.add_argument('device', nargs='?', type=Device,
                        default=DEFAULT_DEVICE, help='target device')
    parser.add_argument('-i', '--image', type=Path, metavar='file',
                        default=DEFAULT_IMAGE, help='image file')
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


def restore(args: Namespace) -> int:
    """Restores the HIDSL image."""

    if args.root:
        return restore_image(args.image, args.root, verbose=args.verbose)

    if args.wipefs:
        wipefs(args.device, verbose=args.verbose)

    first, *other = partition(args.device, mbr=args.mbr, verbose=args.verbose)
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

    with TemporaryDirectory() as tmpd:
        with MountContext(tmpd, reversed(parts)) as mountpoint:
            return restore_image(args.image, mountpoint, verbose=args.verbose)


def main():
    """Runs the script."""

    args = get_args()
    basicConfig(format=LOG_FORMAT, level=DEBUG if args.debug else INFO)
    retval = restore(args)

    if args.beep:
        beep()

    exit(retval)
