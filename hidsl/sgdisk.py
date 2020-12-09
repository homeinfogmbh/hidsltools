"""Partitioning."""

from typing import Generator

from hidsl.device import Device
from hidsl.functions import exe
from hidsl.types import Partition


__all__ = ['Partition', 'mkparts']


SGDISK = '/usr/bin/sgdisk'


def mkefipart(device: Device, *, size: str = '500M', verbose: bool = False):
    """Creates an EFI partition."""

    exe([SGDISK, '-n', f'1::+{size}', str(device)], verbose=verbose)
    exe([SGDISK, '-t', '1:ef00', str(device)], verbose=verbose)


def mkroot(device: Device, *, partno: int = 1, verbose: bool = False):
    """Makes a root partition."""

    exe([SGDISK, '-n', f'{partno}::', str(device)], verbose=verbose)
    exe([SGDISK, '-t', f'{partno}:ef00', str(device)], verbose=verbose)


def mkparts(device: Device, *, mbr: bool = False,
            verbose: bool = False) -> Generator[Partition, None, None]:
    """Partitions a disk."""

    exe([SGDISK, '-og', str(device)], verbose=verbose)
    root_partno = 1

    if not mbr:
        root_partno = 2
        mkefipart(device, verbose=verbose)
        yield device.partition(1)

    mkroot(device, partno=root_partno, verbose=verbose)
    yield device.partition(root_partno)
