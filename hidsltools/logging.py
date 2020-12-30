"""Logging facility."""

from logging import getLogger
from pathlib import Path
from sys import argv


__all__ = ['FORMAT', 'LOGGER']


FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger(Path(argv[0]).stem)
