"""Common functions."""

from pathlib import Path
from subprocess import DEVNULL, CompletedProcess, run
from typing import IO, Iterable, Union

from hidsl.logging import LOGGER


__all__ = ['arch_chroot', 'chroot', 'exe', 'rmsubtree', 'rmtree']


ARCH_CHROOT = '/usr/bin/arch-chroot'


def arch_chroot(root: Union[Path, str], command: Iterable[str]):
    """Converts a command into a chrooted command."""

    return [ARCH_CHROOT, str(root), *command]


def chroot(root: Union[Path, str], path: Union[Path, str]):
    """Changes tht root of the path."""

    if (path := Path(path)).is_absolute():
        path = path.relative_to('/')

    return Path(root).joinpath(path)


def exe(command, *, input: bytes = None,    # pylint: disable=W0622
        stdout: IO = None, verbose: bool = False) -> CompletedProcess:
    """Returns stdout and stderr parameters for subprocess.run()."""

    stderr = None if verbose else DEVNULL
    stdout = stdout if stdout is not None else None if verbose else DEVNULL
    LOGGER.debug('Running command: %s', command)
    return run(command, input=input, check=True, stderr=stderr, stdout=stdout)


def rmsubtree(directory: Path):
    """Removes all files and folders below the given directory."""

    for inode in directory.iterdir():
        if inode.is_dir():
            rmsubtree(inode)

        inode.unlink()


def rmtree(directory: Path):
    """Recursively removes the given directory and all of its contents."""

    rmsubtree(directory)
    directory.unlink()
