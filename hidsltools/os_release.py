"""Image meta data."""

from datetime import datetime
from os import linesep
from pathlib import Path

from hidsltools.defaults import ROOT
from hidsltools.functions import chroot


__all__ = ['write_os_release']


OS_RELEASE = Path('/etc/os-release')


def write_os_release(root: Path = ROOT, *, file: Path = OS_RELEASE) -> None:
    """Write the OS release info and image metadata to the os-release file."""

    with file.open('r') as src, chroot(root, file).open('w') as dst:
        dst.write(src.read())
        dst.write(f'INSTALL_DATE={datetime.now().isoformat()}')
        dst.write(linesep)
