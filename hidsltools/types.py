"""Common data types."""

from __future__ import annotations
from enum import Enum
from pathlib import Path
from re import Pattern
from typing import Iterator, NamedTuple, Union


__all__ = [
    'Compression',
    'DeviceType',
    'Filesystem',
    'FSTabEntry',
    'Glob',
    'Note',
    'PasswdEntry'
]


class Compression(Enum):
    """Compression types."""

    XZ = 'xz'
    BZIP2 = 'bzip2'
    LRZIP = 'lrzip'
    LZ4 = 'lz4'
    ZSTD = 'zstd'
    LZMA = 'lzma'
    LZOP = 'lzop'
    GZIP = 'gzip'

    @property
    def bsdtar_arg(self):
        """Returns the corresponding argument for bsdtar."""
        return f'--{self.value}'


class DeviceType(NamedTuple):
    """Block device types."""

    regex: Pattern
    infix: str = ''

    def check(self, path: Path) -> bool:
        """Checks is the given path is a device of this type."""
        return self.regex.fullmatch(path.stem) and path.is_block_device()


class Filesystem(Enum):
    """Known file systems."""

    CIFS = 'cifs'
    EXT4 = 'ext4'
    VFAT = 'vfat'

    def __str__(self):  # pylint: disable=E0307
        return self.value


class FSTabEntry(NamedTuple):
    """A partition."""

    device: Union[Path, str]
    mountpoint: Path
    filesystem: Filesystem


class Glob:
    """A re-iterable path glob."""

    def __init__(self, path: Path, glob: str):
        """Sets path and glob expression."""
        self.path = path
        self.glob = glob

    def __iter__(self):
        """Returns the glob generator."""
        return self.path.glob(self.glob)


class Note(NamedTuple):
    """A note for a beep melody."""

    frequency: int
    repetitions: int = None
    length: int = None

    @property
    def args(self) -> Iterator[str]:
        """Yields arguments for the beep command."""
        yield '-f'
        yield str(self.frequency)

        if self.repetitions is not None:
            yield '-r'
            yield str(self.repetitions)

        if self.length is not None:
            yield '-l'
            yield str(self.length)


class PasswdEntry(NamedTuple):
    """An entry of /etc/passwd."""

    name: str
    passwd: str
    uid: int
    gid: int
    gecos: str
    home: Path
    shell: str

    @classmethod
    def from_string(cls, string: str, *, sep: str = ':'):
        """Creates the passwd entry from a string."""
        name, passwd, uid, gid, gecos, home, shell = string.split(sep)
        return cls(name, passwd, int(uid), int(gid), gecos, Path(home), shell)
