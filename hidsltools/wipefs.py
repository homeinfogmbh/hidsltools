"""File system wiping."""

from hidsltools.device import Device
from hidsltools.functions import exe


__all__ = ["wipefs"]


WIPEFS = "/usr/bin/wipefs"


def wipefs(device: Device, *, verbose: bool = False) -> None:
    """Wipes file systems from a device."""

    command = [WIPEFS, "-a", "-f", str(device)]
    exe(command, verbose=verbose)
