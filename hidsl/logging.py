"""Logging facility."""

from logging import getLogger


__all__ = ['LOGGER']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger('restore')
