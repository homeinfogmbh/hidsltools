"""Digital signage data and user handling."""

from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, rmsubtree
from hidsltools.logging import LOGGER
from hidsltools.passwd import get_user


__all__ = ['clean_homes']


USERS = {'digsig', 'homeinfo', 'root'}


def clean_homes(*, root: Path = ROOT) -> None:
    """Removes all digital-signage related data."""

    for user in sorted(USERS):
        try:
            home = get_user(user, root=root).home
        except ValueError:
            LOGGER.error('No such user: %s', user)
            continue

        LOGGER.debug('Cleaning home %s of user %s.', home, user)

        if home == ROOT:
            LOGGER.warning('Skipping root directory.')
            continue

        rmsubtree(chroot(root, home))
