"""Common functions."""

from datetime import datetime
from pathlib import Path
from subprocess import DEVNULL, CompletedProcess, check_output, run
from typing import IO, Iterable, List, Optional

from hidsltools.defaults import ROOT
from hidsltools.logging import LOGGER
from hidsltools.types import PasswdEntry


__all__ = [
    'arch_chroot',
    'chroot',
    'exe',
    'get_timestamp',
    'getent',
    'rmsubtree'
]


ARCH_CHROOT = '/usr/bin/arch-chroot'
GETENT = '/usr/bin/getent'


def arch_chroot(root: Path, command: Iterable[str]) -> List[str]:
    """Converts a command into a chrooted command."""

    return [ARCH_CHROOT, str(root), *command]


def chroot(root: Path, path: Path) -> Path:
    """Changes tht root of the path."""

    if path.is_absolute():
        path = path.relative_to(ROOT)

    return root.joinpath(path)


def exe(command, *, input: Optional[bytes] = None, stdout: Optional[IO] = None,
        verbose: bool = False) -> CompletedProcess:
    """Returns stdout and stderr parameters for subprocess.run()."""

    stderr = None if verbose else DEVNULL
    stdout = stdout if stdout is not None else None if verbose else DEVNULL
    LOGGER.debug('Running command: %s', command)
    return run(command, input=input, check=True, stderr=stderr, stdout=stdout)


def get_timestamp(timespec: str = 'seconds') -> str:
    """Returns the current datetime in ISO format."""

    return datetime.now().isoformat(timespec=timespec)


def getent(user: str, *, root: Optional[Path] = None) -> PasswdEntry:
    """Returns the home of the user."""

    command = [GETENT, 'passwd', user]

    if root is not None:
        command = arch_chroot(root, command)

    text = check_output(command)
    return PasswdEntry.from_string(text.strip())


def rmsubtree(directory: Path) -> None:
    """Removes all files and folders below the given directory."""

    for inode in directory.iterdir():
        if inode.is_dir():
            rmsubtree(inode)

        inode.unlink()
