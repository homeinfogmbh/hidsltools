"""Common stuff."""

from pathlib import Path
from typing import Iterator

from hidsltools.types import DeviceType


__all__ = ["Device"]


EMMC = DeviceType("mmcblk([0-9])", "p")
NVME = DeviceType("nvme([0-9])n([0-9])", "p")
SDX = DeviceType("sd([a-z])")
DEVICE_TYPES = {EMMC, NVME, SDX}


class Device(type(Path())):
    """A block device."""

    @property
    def devtype(self):
        """Returns the device type."""
        for device_type in DEVICE_TYPES:
            if device_type.check(self):
                return device_type

        raise ValueError("Unknown block device type:", self)

    @property
    def partitions(self) -> Iterator[Path]:
        """Yields available partitions."""
        return self.parent.glob(f"{self.stem}{self.devtype.infix}[0-9]")

    def partition(self, index: int) -> Path:
        """Returns the respective partition."""
        return self.parent.joinpath(f"{self.stem}{self.devtype.infix}{index}")
