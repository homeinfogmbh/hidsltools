"""Common data types."""

from pathlib import Path
from typing import NamedTuple, Union


__all__ = ['Partition']


class Partition(NamedTuple):
    """A partition."""

    mountpoint: Union[Path, str, None]
    device: Path
    filesystem: str

    def relative_to(self, root: Path):
        """Returns a path relative to the root."""
        if not self.mountpoint:
            return root

        if (path := Path(self.mountpoint)).is_absolute():
            path = path.relative_to('/')

        return root.joinpath(path)
