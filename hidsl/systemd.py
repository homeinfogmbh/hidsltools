"""Systemd invocation."""

from pathlib import Path
from typing import Union

from hidsl.functions import exe


__all__ = [
    'clear',
    'disable',
    'enable',
    'journalctl',
    'systemctl',
    'vacuum_size',
    'vacuum_time'
]


JOURNALCTL = '/usr/bin/journalctl'
SYSTEMCTL = '/usr/bin/systemctl'


def systemctl(*args: str, root: Union[Path, str] = None,
              verbose: bool = False):
    """Runs a systemctl command."""

    command = [SYSTEMCTL, *args]

    if root is not None:
        command += ['--root', str(root)]

    exe(command, verbose=verbose)


def disable(unit: str, root: Union[Path, str] = None, verbose: bool = False):
    """Disables a unit."""

    systemctl('disable', unit, root=root, verbose=verbose)


def enable(unit: str, root: Union[Path, str] = None, verbose: bool = False):
    """Enables a unit."""

    systemctl('enable', unit, root=root, verbose=verbose)


def journalctl(*args: str, root: Union[Path, str] = None,
               verbose: bool = False):
    """Runs journalctl."""

    command = [JOURNALCTL, *args]

    if root is not None:
        command += ['--root', str(root)]

    exe(command, verbose=verbose)


def vacuum_size(size: int, root: Union[Path, str] = None,
                verbose: bool = False):
    """Empties the journal by size."""

    journalctl('--vacuum-size', str(size), root=root, verbose=verbose)


def vacuum_time(time: int, root: Union[Path, str] = None,
                verbose: bool = False):
    """Empties the journal by time."""

    journalctl('--vacuum-time', str(time), root=root, verbose=verbose)


def clear(*, root: Union[Path, str] = None, verbose: bool = False):
    """Clears the journal."""

    vacuum_size(1, root=root, verbose=verbose)
    vacuum_time(1, root=root, verbose=verbose)
