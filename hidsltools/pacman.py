"""Pacman related operations."""

from pathlib import Path
from typing import Optional

from hidsltools.functions import exe


__all__ = ['LOCKFILE', 'clean']


LOCKFILE = Path('/var/lib/pacman/db.lck')
PACMAN = '/usr/bin/pacman'


def clean(*, chroot: Optional[Path] = None, verbose: bool = False) -> None:
    """Cleans the pacman cache."""

    command = [PACMAN, '-S', '-c', '-c', '--noconfirm']

    if chroot is not None:
        command += ['--sysroot', str(chroot)]

    exe(command, verbose=verbose)
