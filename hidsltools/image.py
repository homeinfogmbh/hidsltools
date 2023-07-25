"""Create HIDSL images."""

from argparse import ArgumentParser, Namespace
from datetime import date
from getpass import getpass
from logging import DEBUG, INFO, basicConfig
from pathlib import Path

from hidsltools.bsdtar import create
from hidsltools.defaults import ROOT
from hidsltools.errorhandler import ErrorHandler
from hidsltools.functions import chroot
from hidsltools.logging import FORMAT, LOGGER
from hidsltools.mount import MountContext
from hidsltools.types import Compression
from hidsltools.types import Filesystem
from hidsltools.types import Partition
from hidsltools.types import SafeTemporaryDirectory


__all__ = ["main"]


FILENAME_TEMPLATE = "hidsl-{}.bsdtar.{}"
USER_NAME = "images"


def get_args() -> Namespace:
    """Parses the command line arguments."""

    parser = ArgumentParser(description="Creates HIDSL images.")
    parser.add_argument("root", type=Path, help="reference system root")
    parser.add_argument(
        "-f",
        "--file",
        default=FILENAME_TEMPLATE,
        metavar="filename",
        help="the image file name",
    )
    parser.add_argument("-c", "--cifs", metavar="share", help="CIFS share")
    parser.add_argument(
        "-u", "--user", default=USER_NAME, metavar="name", help="CIFS user name"
    )
    parser.add_argument(
        "-x",
        "--compression",
        type=Compression,
        metavar="compression",
        default=Compression.LZOP,
        help="compression algorithm",
    )
    parser.add_argument(
        "-l",
        "--compression-level",
        type=int,
        metavar="level",
        default=9,
        help="compression level",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show output of subprocesses"
    )
    parser.add_argument(
        "-d", "--debug", action="store_true", help="enable verbose logging"
    )
    return parser.parse_args()


def get_filename(args: Namespace) -> str:
    """Returns the image file name."""

    return args.file.format(date.today().isoformat(), args.compression.suffix)


def cifs_mount(mountpoint: Path, args: Namespace) -> MountContext:
    """Returns a mount context."""

    passwd = getpass("CIFS password: ")
    options = {"user": args.user, "password": passwd}
    fstab = Partition(args.cifs, ROOT, Filesystem.CIFS)
    return MountContext([fstab], root=mountpoint, verbose=args.verbose, **options)


def make_image(file: Path, args: Namespace) -> int:
    """Creates a tarball from a reference system's root directory."""

    create(
        file,
        args.root,
        compression=args.compression,
        compression_level=args.compression_level,
        verbose=args.verbose,
    )
    return 0


def mkhidslimg(args: Namespace) -> int:
    """Creates an image from a given mount point."""

    if not args.root.is_mount():
        LOGGER.error("Specified root is not a mount point.")
        return 1

    file = Path(get_filename(args))

    if args.cifs:
        with SafeTemporaryDirectory() as tmpd:
            with cifs_mount(tmpd, args) as mount:
                return make_image(chroot(mount, file), args)

    return make_image(file, args)


def main() -> int:
    """Runs the program."""

    args = get_args()
    basicConfig(format=FORMAT, level=DEBUG if args.debug else INFO)

    with ErrorHandler(LOGGER):
        return mkhidslimg(args)
