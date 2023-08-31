"""Systemd invocation."""

from pathlib import Path

from hidsltools.functions import exe
from hidsltools.types import Glob


__all__ = [
    "CORE_DUMPS",
    "disable",
    "enable",
    "journalctl",
    "systemctl",
    "vacuum",
    "vacuum_size",
    "vacuum_time",
]


CORE_DUMPS = Glob("/var/lib/systemd/coredump", "*")
JOURNALCTL = "/usr/bin/journalctl"
SYSTEMCTL = "/usr/bin/systemctl"


def systemctl(*args: str, root: Path | None = None, verbose: bool = False) -> None:
    """Runs a systemctl command."""

    command = [SYSTEMCTL, *args]

    if root is not None:
        command += ["--root", str(root)]

    exe(command, verbose=verbose)


def disable(unit: str, *, root: Path | None = None, verbose: bool = False) -> None:
    """Disables a unit."""

    systemctl("disable", unit, root=root, verbose=verbose)


def enable(unit: str, *, root: Path | None = None, verbose: bool = False) -> None:
    """Enables a unit."""

    systemctl("enable", unit, root=root, verbose=verbose)


def journalctl(*args: str, root: Path | None = None, verbose: bool = False) -> None:
    """Runs journalctl."""

    command = [JOURNALCTL, *args]

    if root is not None:
        command += ["--root", str(root)]

    exe(command, verbose=verbose)


def vacuum_size(size: int, *, root: Path | None = None, verbose: bool = False) -> None:
    """Empties the journal by size."""

    journalctl("--vacuum-size", str(size), root=root, verbose=verbose)


def vacuum_time(time: int, *, root: Path | None = None, verbose: bool = False) -> None:
    """Empties the journal by time."""

    journalctl("--vacuum-time", str(time), root=root, verbose=verbose)


def vacuum(value: int = 1, *, root: Path | None = None, verbose: bool = False) -> None:
    """Clears the journal."""

    vacuum_size(value, root=root, verbose=verbose)
    vacuum_time(value, root=root, verbose=verbose)
