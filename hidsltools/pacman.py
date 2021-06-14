"""Pacman related operations."""

from pathlib import Path
from typing import Optional

from hidsltools.functions import exe
from hidsltools.types import Glob


__all__ = ['CACHED_PKGS', 'LOCKFILE', 'clean']


CACHED_PKGS = Glob('/var/cache/pacman/pkg', '*.pkg*')
LOCKFILE = Path('/var/lib/pacman/db.lck')
PACMAN = '/usr/bin/pacman'


def pacman_sc(*, root: Optional[Path] = None, verbose: bool = False) -> None:
    """Run pacman -Sc."""

    command = [PACMAN, '-S', '-c', '--noconfirm']

    if root is not None:
        command += ['--sysroot', str(root)]

    exe(command, verbose=verbose)


def pacman_scc(*, root: Optional[Path] = None, verbose: bool = False) -> None:
    """Run pacman -Scc."""

    command = [PACMAN, '-S', '-c', '-c', '--noconfirm']

    if root is not None:
        command += ['--sysroot', str(root)]

    exe(command, verbose=verbose)


def clean(*, root: Optional[Path] = None, verbose: bool = False) -> None:
    """Clean the pacman cache."""

    pacman_sc(root=root, verbose=verbose)
    pacman_scc(root=root, verbose=verbose)
