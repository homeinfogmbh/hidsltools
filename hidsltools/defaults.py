"""Defaults."""

from pathlib import Path

from hidsl.device import Device


__all__ = ['DEVICE', 'IMAGE']


DEVICE = Device('/dev/sda')
IMAGE = Path('/opt/hidsl/ddb.bsdtar.lzop')
