"""SSH related functions."""

from json import load
from os import chown, linesep
from pathlib import Path
from typing import Iterable

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, exe
from hidsltools.passwd import get_user
from hidsltools.types import Glob


__all__ = ["HOST_KEYS", "generate_host_keys", "restore_authorized_keys"]


CIPHERS = {"rsa", "ecdsa", "ed25519"}
HOST_KEYS = Glob("/etc/ssh/host", "*key*")
KEY_TEMPLATE = "/etc/ssh/ssh_host_{cipher}_key"
SSH_KEYGEN = "/usr/bin/ssh-keygen"


def generate_host_key(cipher: str, *, root: Path = ROOT, verbose: bool = False) -> None:
    """Generates an SSH host key."""

    path = chroot(root, Path(KEY_TEMPLATE.format(cipher=cipher)))
    command = [SSH_KEYGEN, "-f", str(path), "-N", "", "-t", cipher]
    exe(command, input=b"y", verbose=verbose)


def generate_host_keys(*, root: Path = ROOT, verbose: bool = False) -> None:
    """Generates the SSH host keys."""

    for cipher in CIPHERS:
        generate_host_key(cipher, root=root, verbose=verbose)


def install_authorized_keys(
    user: str, keys: Iterable[str], *, root: Path = ROOT
) -> None:
    """Installs the authorized keys for the given user."""

    user = get_user(user, root=root)
    ssh_dir = chroot(root, user.home).joinpath(".ssh")
    ssh_dir.mkdir(mode=0o700, exist_ok=True)
    chown(ssh_dir, user.uid, user.gid)
    authorized_keys = ssh_dir.joinpath("authorized_keys")

    with authorized_keys.open("w") as file:
        for key in keys:
            file.write(key)
            file.write(linesep)

    chown(authorized_keys, user.uid, user.gid)


def restore_authorized_keys(path: Path, *, root: Path = ROOT) -> None:
    """Restores authorized keys from a JSON file."""

    with path.open("r") as file:
        json = load(file)

    for user, keys in json.items():
        install_authorized_keys(user, keys, root=root)
