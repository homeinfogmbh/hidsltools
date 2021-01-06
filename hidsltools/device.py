"""Common stuff."""

from pathlib import Path
from typing import Iterator, Optional, Union

from hidsltools.types import DeviceType


__all__ = ['Device']


EMMC = DeviceType('mmcblk([0-9])', 'p')
NVME = DeviceType('nvme([0-9])n([0-9])', 'p')
SDX = DeviceType('sd([a-z])')
DEVICE_TYPES = {EMMC, NVME, SDX}


class Device:
    """A block device."""

    __slots__ = ('path', 'devtype')

    def __init__(self, path: Union[Path, str], *,
                 devtype: Optional[DeviceType] = None):
        """Sets the path."""
        self.path = Path(path)

        if devtype is None:
            for devtype in DEVICE_TYPES:    # pylint: disable=R1704
                if devtype.check(self.path):
                    break
            else:
                raise ValueError('Unknown block device type:', self.path)

        self.devtype = devtype

    def __getattr__(self, attr: str):
        """Delegates to the path."""
        return getattr(self.path, attr)

    def __str__(self):
        """Delegates to the path."""
        return str(self.path)

    @property
    def partitions(self) -> Iterator[Path]:
        """Yields available partitions."""
        return self.parent.glob(f'{self.stem}{self.devtype.infix}[0-9]')

    def partition(self, index: int) -> Path:
        """Returns the respective partition."""
        return self.parent.joinpath(f'{self.stem}{self.devtype.infix}{index}')
