"""Digital signage data and user handling."""

from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, getent, rmsubtree
from hidsltools.logging import LOGGER


__all__ = ['rmdotfiles']


DATA = Path('/var/lib/digsig')
USERS = {'digsig', 'hidslcfg', 'homeinfo', 'root'}


def rmdotfiles(*, root: Path = ROOT) -> None:
    """Removes all digital-signage related data."""

    rmsubtree(chroot(root, DATA))

    for user in sorted(USERS):
        home = getent(user).home
        LOGGER.debug('Cleaning home %s of user %s.', home, user)
        rmsubtree(chroot(root, home))
