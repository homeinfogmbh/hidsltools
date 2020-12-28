"""Defaults."""

from pathlib import Path

from hidsltools.device import Device


__all__ = ['DEVICE', 'IMAGE']


DEVICE = Device('/dev/sda')
IMAGE = Path('/opt/hidsl/ddb.bsdtar.lzop')
