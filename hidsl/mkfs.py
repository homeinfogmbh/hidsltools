"""File system creation."""

from pathlib import Path

from hidsl.functions import exe
from hidsl.types import Filesystem


__all__ = ['mkfs']


MKFS = '/usr/bin/mkfs'


def mkfat32(device: Path, *, label: str = None, verbose: bool = False):
    """Creates a FAT32 file system."""

    command = [MKFS, '-t', 'vfat', '-F32']

    if label is not None:
        command += ['-n', label]

    command.append(str(device))
    exe(command, verbose=verbose)


def mkext4(device: Path, *, label: str = None, verbose: bool = False):
    """Creates a FAT32 file system."""

    command = [MKFS, '-t', 'ext4', '-F']

    if label is not None:
        command += ['-L', label]

    command.append(str(device))
    exe(command, verbose=verbose)


def mkfs(device: Path, filesystem: Filesystem, *, label: str = None,
         verbose: bool = False):
    """Creates the given file system."""

    if filesystem == Filesystem.FAT32:
        return mkfat32(device, label=label, verbose=verbose)

    if filesystem == Filesystem.EXT4:
        return mkext4(device, label=label, verbose=verbose)

    raise NotImplementedError('File system not implemented:', filesystem)
