"""Bsdtar invocation."""

from pathlib import Path
from typing import Optional

from hidsltools.functions import exe
from hidsltools.types import Compression


__all__ = ['create', 'extract']


BSDTAR = '/usr/bin/bsdtar'


def create(tarball: Path, *files: Path,
           compression: Compression = Compression.LZOP,
           compression_level: int = 9, verbose: bool = False) -> None:
    """Creates a tarball from the given files."""

    command = [BSDTAR, '-c', '-p', '-f', str(tarball)]
    options = []

    if verbose:
        command.append('-v')

    if compression is not None:
        command.append(compression.bsdtar_arg)

    if compression_level is not None:
        options.append(f'compression-level={compression_level}')

    if options:
        command += ['--options', ','.join(options)]

    exe([*command, *files], verbose=verbose)


def extract(tarball: Path, target: Optional[Path] = None, *,
            verbose: bool = False) -> None:
    """Extracts an image using bsdtar."""

    command = [BSDTAR, '-x', '-p', '-f', str(tarball)]

    if verbose:
        command.append('-v')

    if target is not None:
        command += ['-C', str(target)]

    exe(command, verbose=verbose)
