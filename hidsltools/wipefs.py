"""File system wiping."""

from hidsl.device import Device
from hidsl.functions import exe


__all__ = ['wipefs']


WIPEFS = '/usr/bin/wipefs'


def wipefs(device: Device, *, verbose: bool = False):
    """Wipes file systems from a device."""

    command = [WIPEFS, '-a', '-f', str(device)]
    exe(command, verbose=verbose)
