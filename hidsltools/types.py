"""Common data types."""

from __future__ import annotations
from enum import Enum
from pathlib import Path
from re import Pattern
from typing import Generator, NamedTuple, Union


__all__ = [
    'Compression',
    'DeviceType',
    'Enum',
    'Glob',
    'Melody',
    'Note',
    'Partition',
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
    FAT32 = 'fat32'

    def __str__(self):  # pylint: disable=E0307
        return self.value


class Glob:
    """A re-iterable path glob."""

    def __init__(self, path: Path, glob: str):
        """Sets path and glob expression."""
        self.path = path
        self.glob = glob

    def __iter__(self):
        """Returns the glob generator."""
        return self.path.glob(self.glob)


class Melody(tuple):
    """A melody of notes."""

    def __new__(cls, *notes: Note) -> Melody:
        """Creates a new melody from the given notes."""
        return super().__new__(cls, notes)

    @property
    def commands(self) -> Generator[str, None, None]:
        """Yields corresponsing beep commands."""
        try:
            first, *rest = self
        except ValueError:
            raise ValueError('Melody cannot be empty.') from None

        yield from first.commands

        for note in rest:
            yield '-n'
            yield from note.commands


class Note(NamedTuple):
    """A note for a beep melody."""

    frequency: int
    repetitions: int = None
    length: int = None

    @property
    def commands(self) -> Generator[str, None, None]:
        """Yields corresponding beep commands."""
        yield '-f'
        yield str(self.frequency)

        if self.repetitions is not None:
            yield '-r'
            yield str(self.repetitions)

        if self.length is not None:
            yield '-l'
            yield str(self.length)


class Partition(NamedTuple):
    """A partition."""

    mountpoint: Path
    device: Union[Path, str]
    filesystem: Filesystem


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
