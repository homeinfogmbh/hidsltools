"""Common functions."""

from pathlib import Path
from subprocess import CompletedProcess
from typing import Iterable, Union

from hidsl.functions import chroot, exe
from hidsl.logging import LOGGER
from hidsl.types import Partition


__all__ = ['MountContext']


MOUNT = '/usr/bin/mount'
UMOUNT = '/usr/bin/umount'


def mount(device: Path, mountpoint: Path, *,
          verbose: bool = False) -> CompletedProcess:
    """Mounts a partition."""

    return exe([MOUNT, str(device), str(mountpoint)], verbose=verbose)


def umount(mountpoint_or_device: Path, *,
           verbose: bool = False) -> CompletedProcess:
    """Umounts a mountpoint."""

    return exe([UMOUNT, str(mountpoint_or_device)], verbose=verbose)


class MountContext:
    """Context manager for mounts."""

    def __init__(self, mountpoint: Union[Path, str],
                 partitions: Iterable[Partition], *, verbose: bool = False):
        """Sets the partitions."""
        self.mountpoint = Path(mountpoint)
        self.partitions = partitions
        self.verbose = verbose

    def __enter__(self):
        self.mount()
        return self.mountpoint

    def __exit__(self, *_):
        self.umount()

    def mount(self):
        """Mounts all partitions to the mountpoint."""
        for partition in sorted(self.partitions):
            mountpoint = chroot(self.mountpoint, partition.mountpoint)
            LOGGER.debug('Mounting %s to %s.', partition.device, mountpoint)
            mount(partition.device, mountpoint, verbose=self.verbose)

    def umount(self):
        """Mounts all partitions to the mountpoint."""
        for partition in sorted(self.partitions, reverse=True):
            mountpoint = chroot(self.mountpoint, partition.mountpoint)
            LOGGER.debug('Umounting %s.', mountpoint)
            umount(mountpoint, verbose=self.verbose)
