"""Common data types."""

from pathlib import Path
from typing import NamedTuple, Union


__all__ = ['Partition']


class Partition(NamedTuple):
    """A partition."""

    mountpoint: Union[Path, str, None]
    device: Path
    filesystem: str
