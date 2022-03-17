"""Audio notifications via PC speaker."""

from typing import Iterable, Iterator

from hidsltools.functions import exe
from hidsltools.types import Note


__all__ = ['beep']


BEEP = '/usr/bin/beep'
MELODY = (
    Note(1000),
    Note(1500),
    Note(600),
    Note(500),
    Note(100, 2, 10),
    Note(50, 2, 200),
    Note(40, 2, 300),
    Note(60, 3),
    Note(50, 3)
)


def get_args(melody: Iterable[Note]) -> Iterator[str]:
    """Yields corresponding beep arguments."""

    first, *rest = melody
    yield from first.args

    for note in rest:
        yield '-n'
        yield from note.args


def beep(melody: Iterable[Note] = MELODY, *, verbose: bool = False) -> None:
    """Beeps the given melody."""

    exe([BEEP, *get_args(melody)], verbose=verbose)
