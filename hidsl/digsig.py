"""Digital signage data and user handling."""

from pathlib import Path
from typing import Union

from hidsl.functions import chroot, rmsubtree, rmtree
from hidsl.logging import LOGGER


__all__ = ['rmdotfiles']


DATA = Path('/usr/share/digsig')
DOT_DIRS = {'.adobe', '.appdata', '.macromedia'}
HOME = Path('/var/lib/digsig')
USER = 'digsig'


def rmdotfiles(*, root: Union[Path, str] = '/'):
    """Removes all digital-signage related data."""

    rmsubtree(chroot(root, DATA))

    for directory in DOT_DIRS:
        LOGGER.debug('Removing: %s', directory)
        rmtree(chroot(root, HOME).joinpath(directory))
