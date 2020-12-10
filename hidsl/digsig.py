"""Digital signage data and user handling."""

from pathlib import Path
from typing import Union

from hidsl.functions import chroot, homedir, rmsubtree, rmtree


__all__ = ['clear']


DATA = Path('/usr/share/digsig')
DOT_DIRS = {'.adobe', '.appdata', '.macromedia'}
HOME = Path('/var/lib/digsig)
USER = 'digsig'


def clear(*, root: Union[Path, str] = '/', verbose: bool = False):
    """Removes all digital-signage related data."""

    rmsubtree(chroot(root, DATA))

    for directory in DOT_DIRS:
        rmtree(chroot(root, HOME).joinpath(directory))
