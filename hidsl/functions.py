"""Common functions."""

from pathlib import Path
from subprocess import DEVNULL, CompletedProcess, run
from typing import IO, Iterable, Union

from hidsl.logging import LOGGER


__all__ = ['exe', 'relpath']


ARCH_CHROOT = '/usr/bin/arch-chroot'


def arch_chroot(root: Union[Path, str], command: Iterable[str]):
    """Converts a command into a chrooted command."""

    return [ARCH_CHROOT, str(root), *command]


def exe(command, *, input: bytes = None,    # pylint: disable=W0622
        stdout: IO = None, verbose: bool = False) -> CompletedProcess:
    """Returns stdout and stderr parameters for subprocess.run()."""

    stderr = None if verbose else DEVNULL
    stdout = None if verbose else DEVNULL if stdout is None else stdout
    LOGGER.debug('Running command: %s', command)
    return run(command, input=input, check=True, stderr=stderr, stdout=stdout)


def relpath(root: Union[Path, str], path: Union[Path, str]):
    """Returns the path relative to the root."""

    if (path := Path(path)).is_absolute():
        path = path.relative_to('/')

    return Path(root).joinpath(path)
