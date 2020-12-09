"""Bsdtar invocation."""

from pathlib import Path

from hidsl.functions import exe


__all__ = ['extract']


BSDTAR = '/usr/bin/bsdtar'


def extract(image: Path, target: Path, *, verbose: bool = False):
    """Extracts an image using bsdtar."""

    command = [BSDTAR, '-x', '-p']

    if verbose:
        command.append('-v')

    command += [str(image), '-C', str(target)]
    exe(command, verbose=verbose)
