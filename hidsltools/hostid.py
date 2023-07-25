"""Host ID generation."""

from os import linesep
from pathlib import Path
from uuid import uuid4

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot


__all__ = ["HOST_ID", "HOSTNAME", "MACHINE_ID", "mkhostid"]


HOST_ID = Path("/etc/host-id")
HOSTNAME = Path("/etc/hostname")
MACHINE_ID = Path("/etc/machine-id")


def mkhostid(*, root: Path = ROOT) -> None:
    """Generates the host id on the system."""

    with chroot(root, HOST_ID).open("w") as file:
        file.write(uuid4().hex)
        file.write(linesep)
