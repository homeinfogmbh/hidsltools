"""Audio notifications via PC speaker."""

from hidsltools.functions import exe
from hidsltools.types import Melody, Note


__all__ = ['beep']


BEEP = '/usr/bin/beep'
MELODY = Melody(
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


def beep(melody: Melody = MELODY, *, verbose: bool = False):
    """Beeps the given melody."""

    exe([BEEP, *melody.commands], verbose=verbose)
