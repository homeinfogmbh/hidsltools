"""SSH related functions."""

from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot, exe
from hidsltools.types import Glob


__all__ = ['HOST_KEYS', 'generate_host_keys']


CIPHERS = {'dsa', 'rsa', 'ecdsa', 'ed25519'}
HOST_KEYS = Glob('/etc/ssh/host', '*key*')
KEY_TEMPLATE = '/etc/ssh/ssh_host_{cipher}_key'
SSH_KEYGEN = '/usr/bin/ssh-keygen'


def generate_host_key(cipher: str, *, root: Path = ROOT,
                      verbose: bool = False) -> None:
    """Generates an SSH host key."""

    path = chroot(root, Path(KEY_TEMPLATE.format(cipher=cipher)))
    command = [SSH_KEYGEN, '-f', str(path), '-N', '', '-t', cipher]
    exe(command, input=b'y', verbose=verbose)


def generate_host_keys(*, root: Path = ROOT, verbose: bool = False) -> None:
    """Generates the SSH host keys."""

    for cipher in CIPHERS:
        generate_host_key(cipher, root=root, verbose=verbose)
