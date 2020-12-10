"""Initramfs tools."""

from pathlib import Path
from typing import Union

from hidsl.functions import arch_chroot, exe
from hidsl.types import Glob


__all__ = ['INITRAMFS', 'mkinitcpio']


INITRAMFS = Glob('/boot', 'initramfs-linux*.img')
MKINITCPIO = '/usr/bin/mkinitcpio'


def mkinitcpio(*, chroot: Union[Path, str] = None, verbose: bool = False):
    """Re-generates the initramfs."""

    command = [MKINITCPIO, '-P']

    if chroot is not None:
        command = arch_chroot(chroot, command)

    exe(command, verbose=verbose)
