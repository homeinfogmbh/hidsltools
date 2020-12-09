"""Common functions."""

from subprocess import DEVNULL, CompletedProcess, run

__all__ = ['exe']


def exe(*args, verbose: bool = False, **kwargs) -> CompletedProcess:
    """Returns stdout and stderr parameters for subprocess.run()."""

    out = None if verbose else DEVNULL
    return run(*args, check=True, stderr=out, stdout=out, **kwargs)
