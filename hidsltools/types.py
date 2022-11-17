"""Common data types."""

from __future__ import annotations
from enum import Enum
from pathlib import Path
from re import fullmatch
from tempfile import TemporaryDirectory
from typing import Iterator, NamedTuple, Protocol


__all__ = [
    'Compression',
    'DeviceType',
    'Filesystem',
    'Glob',
    'Hash',
    'Note',
    'Partition',
    'PasswdEntry',
    'SafeTemporaryDirectory'
]


class Compression(Enum):
    """Compression types."""

    XZ = 'xz'
    BZIP2 = ('bzip2', 'bz2')
    LRZIP = 'lrzip'
    LZ4 = 'lz4'
    ZSTD = 'zstd'
    LZMA = 'lzma'
    LZOP = 'lzop'
    GZIP = ('gzip', 'gz')

    def __init__(self, full_name: str, suffix: str | None = None):
        """Creates a compression instance."""
        self.full_name = full_name
        self.suffix = suffix or full_name


class DeviceType(NamedTuple):
    """Block device types."""

    regex: str
    infix: str = ''

    def check(self, path: Path) -> bool:
        """Checks is the given path is a device of this type."""
        return fullmatch(self.regex, path.stem) and path.is_block_device()


class Filesystem(Enum):
    """Known file systems."""

    CIFS = 'cifs'
    EXT4 = 'ext4'
    VFAT = 'vfat'

    def __str__(self):
        return self.value


class Glob:
    """A re-iterable path glob."""

    __slots__ = ('path', 'glob')

    def __init__(self, path: Path | str, glob: str):
        """Sets path and glob expression."""
        self.path = Path(path)
        self.glob = glob

    def __iter__(self):
        """Returns the glob generator."""
        return self.path.glob(self.glob)


class Hash(Protocol):
    """Objects returned from hashlib.* algorithms."""

    def hexdigest(self) -> str:
        pass


class Note(NamedTuple):
    """A note for a beep melody."""

    frequency: int
    repetitions: int | None = None
    length: int | None = None

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


class Partition(NamedTuple):
    """Information about a partition."""

    device: Path
    mountpoint: Path
    filesystem: Filesystem
    label: str | None = None


class PasswdEntry(NamedTuple):
    """An /etc/passwd entry."""

    name: str
    password: str
    uid: int
    gid: int
    gecos: str
    directory: Path
    shell: str

    @classmethod
    def from_string(cls, string: str) -> PasswdEntry:
        """Creates a passwd entry from a string."""
        name, password, uid, gid, gecos, directory, shell = string.split(':')
        return cls(
            name, password, int(uid), int(gid), gecos, Path(directory), shell
        )

    @property
    def home(self) -> Path:
        """Returns the home directory. Alias to directory."""
        return self.directory

    @property
    def passwd(self) -> str:
        """Returns the password. Alias to password."""
        return self.password


class SafeTemporaryDirectory(TemporaryDirectory):
    """Temporary directory that only gets
    deleted if no exception occurred.
    """

    def __exit__(self, typ, value, traceback):
        if typ is None and value is None:
            return super().__exit__(typ, value, traceback)

        return None
