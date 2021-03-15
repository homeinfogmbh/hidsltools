"""Creating images."""

from argparse import ArgumentParser, Namespace
from datetime import date
from getpass import getpass
from logging import DEBUG, INFO, basicConfig
from pathlib import Path
from sys import exit    # pylint: disable=W0622
from tempfile import TemporaryDirectory

from hidsltools.bsdtar import create
from hidsltools.defaults import ROOT
from hidsltools.errorhandler import ErrorHandler
from hidsltools.functions import chroot
from hidsltools.logging import FORMAT, LOGGER
from hidsltools.mount import MountContext
from hidsltools.types import Compression, Filesystem, Partition


__all__ = ['main']


FILENAME_TEMPLATE = 'hidsl-{}.bsdtar.{}'
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
    parser.add_argument('-x', '--compression', type=Compression,
                        metavar='compression', default=Compression.LZOP,
                        help='compression algorithm')
    parser.add_argument('-l', '--compression-level', type=int, metavar='level',
                        default=9, help='compression algorithm')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='show output of subprocesses')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='enable verbose logging')
    return parser.parse_args()


def get_filename(args: Namespace) -> str:
    """Returns the image file name."""

    return args.file.format(date.today().isoformat(), args.compression.value)


def cifs_mount(mountpoint: Path, args: Namespace) -> MountContext:
    """Returns a mount context."""

    passwd = getpass('CIFS password: ')
    options = {'user': args.user, 'password': passwd}
    fstab = Partition(args.cifs, ROOT, Filesystem.CIFS)
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

    file = Path(get_filename(args))

    if args.cifs:
        with TemporaryDirectory() as tmp:
            with cifs_mount(tmp, args) as mount:
                return make_image(args.root, chroot(mount, file), args)

    return make_image(args.root, file, args)


def main() -> None:
    """Runs the program."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    with ErrorHandler(LOGGER):
        exit(mkhidslimg(args))
