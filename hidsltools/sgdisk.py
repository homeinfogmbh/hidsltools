"""Partitioning."""

from typing import Iterator

from hidsltools.defaults import BOOT, ROOT
from hidsltools.device import Device
from hidsltools.functions import exe
from hidsltools.types import Filesystem, Partition


__all__ = ["mkparts"]


SGDISK = "/usr/bin/sgdisk"


def mkefipart(device: Device, *, size: str = "500M", verbose: bool = False) -> None:
    """Creates an EFI partition."""

    exe([SGDISK, "-n", f"1::+{size}", str(device)], verbose=verbose)
    exe([SGDISK, "-t", "1:ef00", str(device)], verbose=verbose)


def mkroot(device: Device, *, partno: int = 1, verbose: bool = False) -> None:
    """Makes a root partition."""

    exe([SGDISK, "-n", f"{partno}::", str(device)], verbose=verbose)
    exe([SGDISK, "-t", f"{partno}:8304", str(device)], verbose=verbose)


def mkparts(
    device: Device, *, efi: bool = True, verbose: bool = False
) -> Iterator[Partition]:
    """Partitions a disk."""

    exe([SGDISK, "-og", str(device)], verbose=verbose)
    root_partition_number = 1

    if efi:
        root_partition_number = 2
        mkefipart(device, verbose=verbose)
        partition = device.partition(1)
        yield Partition(partition, BOOT, Filesystem.VFAT, "EFI")

    mkroot(device, partno=root_partition_number, verbose=verbose)
    partition = device.partition(root_partition_number)
    yield Partition(partition, ROOT, Filesystem.EXT4, "root")
