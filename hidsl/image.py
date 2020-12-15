"""Creating images."""

from argparse import ArgumentParser, Namespace
from datetime import datetime
from getpass import getpass
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from subprocess import CalledProcessError
from sys import exit    # pylint: disable=W0622
from tempfile import TemporaryDirectory
from typing import Union

from hidsl.bsdtar import create
from hidsl.device import Device
from hidsl.functions import chroot
from hidsl.logging import FORMAT, LOGGER
from hidsl.mount import MountContext
from hidsl.types import Filesystem, Partition


__all__ = ['main']


FILENAME_TEMPLATE = 'hidsl-{timestamp}.bsdtar.{suffix}'
USER_NAME = 'images'


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser(description='Creates HIDSL images.')
    parser.add_argument('source', type=Path, help='image source')
    parser.add_argument('-f', '--file', default=FILENAME_TEMPLATE,
                        metavar='filename', help='the image file name')
    parser.add_argument('-c', '--cifs', metavar='share', help='CIFS share')
    parser.add_argument('-u', '--user', default=USER_NAME, metavar='name',
                        help='CIFS user name')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
    return parser.parse_args()


def get_filename(args: Namespace) -> str:
    """Returns the image file name."""

    return args.file.format(timestamp=datetime.now(), suffix=args.compression)


def cifs_mount(mountpoint: Union[Path, str], args: Namespace) -> MountContext:
    """Returns a mount context."""

    passwd = getpass('CIFS password: ')
    options = {'user': args.user, 'password': passwd}
    partition = Partition(Path('/'), args.cifs, Filesystem.CIFS)
    return MountContext(mountpoint, [partition], verbose=args.verbose,
                        **options)


def make_image(mountpoint: Path, file: Path, args: Namespace) -> int:
    """Creates the tarball."""

    create(file, *mountpoint.glob('*'), compression=args.compression,
           compression_level= args.compression_level, verbose=args.verbose)
    return 0


def from_mountpoint(mountpoint: Path, args: Namespace) -> int:
    """Creates an image from a given mount point."""

    file = Path(get_filename(args.file))

    if args.cifs:
        with TemporaryDirectory() as tmp:
            with cifs_mount(tmp, args) as mount:
                return make_image(mountpoint, chroot(mount, file), args)

    return make_image(mountpoint, file, args)


def from_block_device(device: Device, args: Namespace) -> int:
    """Creates an image from a block device."""

    with TemporaryDirectory() as tmp:
        with MountContext(tmp, device.partitions, verbose=args.verbose) as mnt:
            return from_mountpoint(mnt, args)


def mkhidslimg(args: Namespace) -> int:
    """Creates a HIDSL image."""

    if args.source.is_mount():
        return from_mountpoint(args.source, args)

    if args.source.is_block_device():
        return from_block_device(Device(args.source), args)

    LOGGER.error('Source %s is neither a mount point, nor a block device.',
                 args.source)
    return 1


def main():
    """Runs the program."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    try:
        returncode = mkhidslimg(args)
    except CalledProcessError as error:
        LOGGER.critical('Subprocess error.')
        LOGGER.error(error)
        exit(error.returncode)

    exit(returncode)
