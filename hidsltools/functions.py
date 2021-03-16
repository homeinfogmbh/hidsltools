"""Common functions."""

from pathlib import Path
from subprocess import DEVNULL, CompletedProcess, check_output, run
from typing import IO, Iterable, Optional

from hidsltools.defaults import ROOT
from hidsltools.logging import LOGGER
from hidsltools.types import PasswdEntry


__all__ = [
    'arch_chroot',
    'chroot',
    'exe',
    'getent',
    'rmsubtree',
    'rmtree'
]


ARCH_CHROOT = '/usr/bin/arch-chroot'
GETENT = '/usr/bin/getent'


def arch_chroot(root: Path, command: Iterable[str]) -> list[str]:
    """Converts a command into a chrooted command."""

    return [ARCH_CHROOT, str(root), *command]


def chroot(root: Path, path: Path) -> Path:
    """Changes tht root of the path."""

    if path.is_absolute():
        path = path.relative_to(ROOT)

    return root.joinpath(path)


# pylint: disable=W0622
def exe(command, *, input: Optional[bytes] = None, stdout: Optional[IO] = None,
        verbose: bool = False) -> CompletedProcess:
    """Returns stdout and stderr parameters for subprocess.run()."""

    stderr = None if verbose else DEVNULL
    stdout = stdout if stdout is not None else None if verbose else DEVNULL
    LOGGER.debug('Running command: %s', command)
    return run(command, input=input, check=True, stderr=stderr, stdout=stdout)


def getent(user: str, *, root: Optional[Path] = None) -> PasswdEntry:
    """Returns the home of the user."""

    command = [GETENT, 'passwd', user]

    if root is not None:
        command = arch_chroot(root, command)

    text = check_output(command, text=True)
    return PasswdEntry.from_string(text.strip())


def rmsubtree(directory: Path) -> None:
    """Removes all files and folders below the given directory."""

    for child in directory.iterdir():
        rmtree(child)


def rmtree(inode: Path) -> None:
    """Recursively removes the inode."""

    if inode.is_dir():
        for child in inode.iterdir():
            rmtree(child)

        inode.rmdir()
    else:
        inode.unlink()
