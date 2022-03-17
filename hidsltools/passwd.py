"""Parsing of /etc/passwd."""

from __future__ import annotations
from pathlib import Path
from typing import Callable, Iterator

from hidsltools.defaults import ROOT
from hidsltools.types import PasswdEntry


__all__ = ['get_user', 'passwd']


ETC_PASSWD = Path('etc/passwd')


def passwd(*, root: Path = ROOT) -> Iterator[PasswdEntry]:
    """Yields passwd entries."""

    with (root / ETC_PASSWD).open('r', encoding='utf-8') as file:
        for line in file:
            if line := line.strip():
                yield PasswdEntry.from_string(line)


def match(ident: str | int) -> Callable[[PasswdEntry], bool]:
    """Returns a function to match passwd entries."""

    if isinstance(ident, str):
        return lambda passwd_entry: passwd_entry.name == ident

    if isinstance(ident, int):
        return lambda passwd_entry: passwd_entry.uid == ident

    raise TypeError('Identifier must be str (name) or int (UID).')


def get_user(ident: str | int, *, root: Path = ROOT) -> PasswdEntry:
    """Returns the passwd entry for the given user."""

    for passwd_entry in filter(match(ident), passwd(root=root)):
        return passwd_entry

    raise ValueError('No matching passwd entry found.')
