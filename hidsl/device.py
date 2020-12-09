"""Common stuff."""

from re import compile  # pylint: disable=W0622
from pathlib import Path
from typing import Tuple, Union


__all__ = ['Device']


EMMC = compile('mmcblk([0-9])')
NVME = compile('nvme([0-9])n([0-9])')
SDX = compile('sd([a-z])')


def is_valid(device: Path) -> bool:
    """Checks whether the device is valid."""

    if EMMC.fullmatch(device.stem) is not None:
        return device.is_file()

    if EMMC.fullmatch(device.stem) is not None:
        return device.is_file()

    if SDX.fullmatch(device.stem) is not None:
        return device.is_file()

    return False


class Device:
    """A block device."""

    def __init__(self, path: Union[Path, str]):
        """Sets the path."""
        self._path = path = Path(path)

        if not is_valid(path):
            raise ValueError('Unknown block device type:', path.stem)

    def __getattr__(self, attr):
        """Delegates to the path."""
        return getattr(self._path, attr)

    def __str__(self):
        """Delegates to the path."""
        return str(self._path)

    @property
    def devno(self) -> Union[int, Tuple[int, int], str]:
        """Returns the device number."""
        if (match := EMMC.fullmatch(self.stem)) is not None:
            return int(match.group(1))

        if (match := EMMC.fullmatch(self.stem)) is not None:
            return (int(match.group(1)), int(match.group(2)))

        if (match := SDX.fullmatch(self.stem)) is not None:
            return match.group(1)

        raise ValueError('Unknown block device type:', self.stem)

    def partition(self, index: int):
        """Returns the respective partition."""
        if EMMC.fullmatch(self.stem) is not None:
            return self.parent.joinpath(f'{self.stem}p{index}')

        if EMMC.fullmatch(self.stem) is not None:
            return self.parent.joinpath(f'{self.stem}p{index}')

        if SDX.fullmatch(self.stem) is not None:
            return self.parent.joinpath(f'{self.stem}{index}')

        raise ValueError('Unknown block device type:', self.stem)
