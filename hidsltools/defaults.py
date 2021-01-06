"""Defaults."""

from pathlib import Path

from hidsltools.device import Device


__all__ = ['BOOT', 'DEVICE', 'IMAGE', 'ROOT']


BOOT = Path('/boot')
DEVICE = Device('/dev/sda')
IMAGE = Path('/opt/hidsl/ddb.bsdtar.lzop')
ROOT = Path('/')
