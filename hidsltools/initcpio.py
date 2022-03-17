"""Initramfs tools."""

from pathlib import Path
from typing import Optional

from hidsltools.functions import arch_chroot, exe
from hidsltools.types import Glob


__all__ = ['INITRAMFS', 'mkinitcpio']


INITRAMFS = Glob('/boot', 'initramfs-linux*.img')
MKINITCPIO = '/usr/bin/mkinitcpio'


def mkinitcpio(
        *,
        chroot: Optional[Path] = None,
        verbose: bool = False
) -> None:
    """Re-generates the initramfs."""

    command = [MKINITCPIO, '-P']

    if chroot is not None:
        command = arch_chroot(chroot, command)

    exe(command, verbose=verbose)
