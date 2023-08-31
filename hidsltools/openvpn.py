"""OpenVPN related operations."""

from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, rmsubtree


__all__ = ["delete_client_config"]


CLIENTS_DIR = Path("/etc/openvpn/client")


def delete_client_config(*, root: Path = ROOT) -> None:
    """Deletes OpenVPN clients configuration."""

    if not (clients_dir := chroot(root, CLIENTS_DIR)).exists():
        return

    rmsubtree(clients_dir)
