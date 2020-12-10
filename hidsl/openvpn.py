"""OpenVPN related operations."""

from pathlib import Path
from typing import Union

from hidsl.functions import chroot, rmsubtree


__all__ = ['delete_client_config']


CLIENTS_DIR = Path('/etc/openvpn/client')


def delete_client_config(*, root: Union[Path, str] = '/'):
    """Deletes OpenVPN clients configuration."""

    rmsubtree(chroot(root, CLIENTS_DIR))
