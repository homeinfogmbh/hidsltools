"""Digital signage data and user handling."""

from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, getent, rmsubtree
from hidsltools.logging import LOGGER
from hidsltools.types import Glob


__all__ = ['rmdotfiles']


DATA = Path('/var/lib/digsig')
USERS = {'digsig', 'homeinfo', 'root'}


def rmdotfiles(*, root: Path = ROOT) -> None:
    """Removes all digital-signage related data."""

    rmsubtree(chroot(root, DATA))

    for user in sorted(USERS):
        home = getent(user, root=root).home
        LOGGER.debug('Cleaning home %s of user %s.', home, user)

        if home == Path('/'):
            LOGGER.warning('Skipping root directory.')
            continue

        for dotfile in Glob(chroot(root, home), '.*'):
            rmsubtree(dotfile)
