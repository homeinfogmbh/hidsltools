"""Initramfs tools."""

from pathlib import Path
from typing import Union

from hidsl.functions import exe, arch_chroot


__all__ = ['mkinitcpio']


MKINITCPIO = '/usr/bin/mkinitcpio'


def mkinitcpio(*, chroot: Union[Path, str] = None, verbose: bool = False):
    """Re-generates the initramfs."""

    command = [MKINITCPIO, '-P']

    if chroot is not None:
        command = arch_chroot(chroot, command)

    exe(command, verbose=verbose)
