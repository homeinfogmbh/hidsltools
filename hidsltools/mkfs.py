"""File system creation."""

from pathlib import Path
from typing import Optional

from hidsltools.functions import exe
from hidsltools.types import Filesystem


__all__ = ['mkfs']


MKFS = '/usr/bin/mkfs'


def mkvfat(
        device: Path,
        *,
        label: Optional[str] = None,
        fat_size: int = 32,
        verbose: bool = False
) -> None:
    """Creates a vfat file system."""

    command = [MKFS, '-t', 'vfat']

    if fat_size is not None:
        command += ['-F', str(fat_size)]

    if label is not None:
        command += ['-n', label]

    command.append(str(device))
    exe(command, verbose=verbose)


def mkext4(
        device: Path,
        *,
        label: Optional[str] = None,
        verbose: bool = False
) -> None:
    """Creates an ext4 file system."""

    command = [MKFS, '-t', 'ext4', '-F']

    if label is not None:
        command += ['-L', label]

    command.append(str(device))
    exe(command, verbose=verbose)


def mkfs(
        device: Path,
        filesystem: Filesystem,
        *,
        verbose: bool = False,
        **kwargs
) -> None:
    """Creates the given file system."""

    if filesystem == Filesystem.VFAT:
        return mkvfat(device, verbose=verbose, **kwargs)

    if filesystem == Filesystem.EXT4:
        return mkext4(device, verbose=verbose, **kwargs)

    raise NotImplementedError('File system not implemented:', filesystem)
