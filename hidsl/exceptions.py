"""Common exceptions."""

from pathlib import Path


__all__ = ['NotAMountPointOrBlockDevice']


class NotAMountPointOrBlockDevice(Exception):
    """Indicates that the given path is neither
    a mount point, nor a block device.
    """

    def __init__(self, path: Path):
        """Sets the path."""
        super().__init__(path)
        self.path = path
