"""File system table related functions."""

from pathlib import Path
from typing import Union

from hidsltools.functions import chroot, exe


__all__ = ['FSTAB', 'genfstab']


FSTAB = Path('/etc/fstab')
GENFSTAB = '/usr/bin/genfstab'


def genfstab(*, root: Union[Path, str] = '/', verbose: bool = False):
    """Generates a file system table."""

    command = [GENFSTAB, '-L', '-p', str(root)]

    with chroot(root, FSTAB).open('w') as file:
        exe(command, stdout=file, verbose=verbose)
