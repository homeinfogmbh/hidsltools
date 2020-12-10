"""Syslinux invocation."""

from pathlib import Path
from typing import Union

from hidsl.functions import exe


__all__ = ['AUTOUPDATE', 'install_update']


AUTOUPDATE = Path('/boot/syslinux/SYSLINUX_AUTOUPDATE')
SYSLINUX_INSTALL_UPDATE = '/usr/bin/syslinux-install_update'


def install_update(*, chroot: Union[Path, str] = None, verbose: bool = False):
    """Installs or updates syslinux."""

    command = [SYSLINUX_INSTALL_UPDATE, '-i', '-a', '-m']

    if chroot is not None:
        command += ['-c', str(chroot)]

    exe(command, verbose=verbose)
