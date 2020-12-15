"""Common data types."""

from __future__ import annotations
from enum import Enum
from pathlib import Path
from typing import Generator, NamedTuple


__all__ = ['Enum', 'Glob', 'Melody', 'Note', 'Partition']


class Filesystem(Enum):
    """Known file systems."""

    FAT32 = 'fat32'
    EXT4 = 'ext4'


class Glob:
    """A re-iterable path glob."""

    def __init__(self, path: Path, glob: str):
        """Sets path and glob expression."""
        self.path = path
        self.glob = glob

    def __iter__(self):
        """Returns the glob generator."""
        return self.path.glob(self.glob)


class Melody(list):
    """A melody of notes."""

    def __new__(cls, *notes: Note) -> Melody:
        """Creates a new melody from the given notes."""
        return super().__new__(cls, notes)

    @property
    def command(self) -> Generator[str, None, None]:
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
    device: Path
    filesystem: str
