"""Partitioning."""

from typing import Iterator

from hidsltools.defaults import BOOT, ROOT
from hidsltools.device import Device
from hidsltools.functions import exe
from hidsltools.types import Filesystem, Partition


__all__ = ['mkparts']


SGDISK = '/usr/bin/sgdisk'


def mkefipart(device: Device, *, size: str = '500M',
              verbose: bool = False) -> None:
    """Creates an EFI partition."""

    exe([SGDISK, '-n', f'1::+{size}', str(device)], verbose=verbose)
    exe([SGDISK, '-t', '1:ef00', str(device)], verbose=verbose)


def mkroot(device: Device, *, partno: int = 1,
           verbose: bool = False) -> None:
    """Makes a root partition."""

    exe([SGDISK, '-n', f'{partno}::', str(device)], verbose=verbose)
    exe([SGDISK, '-t', f'{partno}:8304', str(device)], verbose=verbose)


def mkparts(device: Device, *, mbr: bool = False,
            verbose: bool = False) -> Iterator[Partition]:
    """Partitions a disk."""

    exe([SGDISK, '-og', str(device)], verbose=verbose)
    root_partno = 1

    if not mbr:
        root_partno = 2
        mkefipart(device, verbose=verbose)
        partition = device.partition(1)
        yield Partition(partition, BOOT, Filesystem.VFAT, 'EFI')

    mkroot(device, partno=root_partno, verbose=verbose)
    partition = device.partition(root_partno)
    yield Partition(partition, ROOT, Filesystem.EXT4, 'root')
