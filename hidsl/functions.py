"""Common functions."""

from subprocess import DEVNULL, CompletedProcess, run

from hidsl.logging import LOGGER


__all__ = ['exe']


def exe(command, verbose: bool = False) -> CompletedProcess:
    """Returns stdout and stderr parameters for subprocess.run()."""

    out = None if verbose else DEVNULL
    LOGGER.debug('Running command: %s', command)
    return run(command, check=True, stderr=out, stdout=out)
