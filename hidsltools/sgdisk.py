"""Partitioning."""

from pathlib import Path
from typing import Generator

from hidsltools.device import Device
from hidsltools.functions import exe, returning
from hidsltools.types import Filesystem, Partition


__all__ = ['mkparts']


SGDISK = '/usr/bin/sgdisk'


def mkefipart(device: Device, *, size: str = '500M', verbose: bool = False):
    """Creates an EFI partition."""

    exe([SGDISK, '-n', f'1::+{size}', str(device)], verbose=verbose)
    exe([SGDISK, '-t', '1:ef00', str(device)], verbose=verbose)


def mkroot(device: Device, *, partno: int = 1, verbose: bool = False):
    """Makes a root partition."""

    exe([SGDISK, '-n', f'{partno}::', str(device)], verbose=verbose)
    exe([SGDISK, '-t', f'{partno}:ef00', str(device)], verbose=verbose)


@returning(sorted)
def mkparts(device: Device, *, mbr: bool = False,
            verbose: bool = False) -> Generator[Partition, None, None]:
    """Partitions a disk."""

    exe([SGDISK, '-og', str(device)], verbose=verbose)
    root_partno = 1

    if not mbr:
        root_partno = 2
        mkefipart(device, verbose=verbose)
        yield Partition(Path('/boot'), device.partition(1), Filesystem.FAT32)

    mkroot(device, partno=root_partno, verbose=verbose)
    yield Partition(Path('/'), device.partition(root_partno), Filesystem.EXT4)
