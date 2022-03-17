"""Parsing of /etc/passwd."""

from __future__ import annotations
from pathlib import Path
from typing import Iterator, NamedTuple


__all__ = ['PasswdEntry', 'passwd']


ETC_PASSWD = Path('etc/passwd')


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


def passwd(*, root: Path = Path('/')) -> Iterator[PasswdEntry]:
    """Yields passwd entries."""

    with (root / ETC_PASSWD).open('r', encoding='utf-8') as file:
        for line in file:
            if line := line.strip():
                yield PasswdEntry.from_string(line)
