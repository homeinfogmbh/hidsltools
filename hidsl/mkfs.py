"""File system creation."""

from enum import Enum
from pathlib import Path

from hidsl.functions import exe


__all__ = ['Filesystem', 'mkfs']


MKFS = '/usr/bin/mkfs'


class Filesystem(Enum):
    """Known file systems."""

    FAT32 = 'fat32'
    EXT4 = 'ext4'


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
