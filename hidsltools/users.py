"""Digital signage data and user handling."""

from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, getent, rmsubtree
from hidsltools.logging import LOGGER


__all__ = ['clean_homes']


USERS = {'digsig', 'homeinfo', 'root'}


def clean_homes(*, root: Path = ROOT) -> None:
    """Removes all digital-signage related data."""

    for user in sorted(USERS):
        home = getent(user, root=root).home
        LOGGER.debug('Cleaning home %s of user %s.', home, user)

        if home == ROOT:
            LOGGER.warning('Skipping root directory.')
            continue

        rmsubtree(chroot(root, home))
