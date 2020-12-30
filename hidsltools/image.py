"""Creating images."""

from argparse import ArgumentParser, Namespace
from getpass import getpass
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from sys import exit    # pylint: disable=W0622
from tempfile import TemporaryDirectory
from typing import Union

from hidsltools.bsdtar import create
from hidsltools.errorhandler import ErrorHandler
from hidsltools.functions import chroot, get_timestamp
from hidsltools.logging import FORMAT, LOGGER
from hidsltools.mount import MountContext
from hidsltools.types import Filesystem, Partition


__all__ = ['main']


FILENAME_TEMPLATE = 'hidsl-{timestamp}.bsdtar.{suffix}'
USER_NAME = 'images'


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser(description='Creates HIDSL images.')
    parser.add_argument('root', type=Path, help='reference system root')
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

    return args.file.format(timestamp=get_timestamp(), suffix=args.compression)


def cifs_mount(mountpoint: Union[Path, str], args: Namespace) -> MountContext:
    """Returns a mount context."""

    passwd = getpass('CIFS password: ')
    options = {'user': args.user, 'password': passwd}
    fstab = Partition(args.cifs, Path('/'), Filesystem.CIFS)
    return MountContext([fstab], root=mountpoint, verbose=args.verbose,
                        **options)


def make_image(root: Path, file: Path, args: Namespace) -> int:
    """Creates a tarball from a reference system's root directory."""

    create(file, *root.glob('*'), compression=args.compression,
           compression_level=args.compression_level, verbose=args.verbose)
    return 0


def mkhidslimg(args: Namespace) -> int:
    """Creates an image from a given mount point."""

    if not args.root.is_mount():
        LOGGER.error('Specified root is not a mount point.')
        return 1

    file = Path(get_filename(args.file))

    if args.cifs:
        with TemporaryDirectory() as tmp:
            with cifs_mount(tmp, args) as mount:
                return make_image(args.root, chroot(mount, file), args)

    return make_image(args.root, file, args)


def main():
    """Runs the program."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    with ErrorHandler(LOGGER):
        exit(mkhidslimg(args))
