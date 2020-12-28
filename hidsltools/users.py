"""Digital signage data and user handling."""

from pathlib import Path
from typing import Union

from hidsltools.functions import chroot, getent, rmsubtree
from hidsltools.logging import LOGGER


__all__ = ['rmdotfiles']


DATA = Path('/usr/share/digsig')
USERS = {'digsig', 'hidslcfg', 'homeinfo', 'root'}


def rmdotfiles(*, root: Union[Path, str] = '/'):
    """Removes all digital-signage related data."""

    rmsubtree(chroot(root, DATA))

    for user in sorted(USERS):
        home = getent(user).home
        LOGGER.debug('Cleaning home %s of user %s.', home, user)
        rmsubtree(chroot(root, home))
