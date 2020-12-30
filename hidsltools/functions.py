"""Common functions."""

from datetime import datetime
from functools import wraps
from pathlib import Path
from subprocess import DEVNULL, CompletedProcess, check_output, run
from typing import Callable, IO, Iterable, Union

from hidsltools.logging import LOGGER
from hidsltools.types import PasswdEntry


__all__ = [
    'arch_chroot',
    'chroot',
    'exe',
    'get_timestamp',
    'getent',
    'returning',
    'rmsubtree'
]


ARCH_CHROOT = '/usr/bin/arch-chroot'
GETENT = '/usr/bin/getent'


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


def get_timestamp(timespec: str = 'seconds') -> str:
    """Returns the current datetime in ISO format."""

    return datetime.now().isoformat(timespec=timespec)


def getent(user: str, *, root: Union[Path, str] = None) -> PasswdEntry:
    """Returns the home of the user."""

    command = [GETENT, 'passwd', user]

    if root is not None:
        command = arch_chroot(root, command)

    text = check_output(command)
    return PasswdEntry.from_string(text.strip())


def returning(typ: type):
    """Returns a decorator to coerce a callable's return value."""

    def decorator(function: Callable) -> Callable:
        """Returns a wrapper function to coerce the return value."""
        @wraps(function)
        def wrapper(*args, **kwargs) -> typ:
            """Retuns the result from the function
            casted to the given type.
            """
            return typ(function(*args, **kwargs))

        return wrapper

    return decorator


def rmsubtree(directory: Path):
    """Removes all files and folders below the given directory."""

    for inode in directory.iterdir():
        if inode.is_dir():
            rmsubtree(inode)

        inode.unlink()
