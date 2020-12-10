"""Host ID generation."""

from os import linesep
from pathlib import Path
from typing import Union
from uuid import uuid4

from hidsl.functions import relpath


__all__ = ['mkhostid']


HOST_ID = '/etc/host-id'


def mkhostid(*, root: Union[Path, str] = '/'):
    """Generates the host id on the system."""

    with relpath(root, HOST_ID).open('w') as file:
        file.write(uuid4().hex)
        file.write(linesep)
