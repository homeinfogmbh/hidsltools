"""Common error handling."""

from logging import Logger
from subprocess import CalledProcessError
from sys import exit    # pylint: disable=W0622


__all__ = ['ErrorHandler']


class ErrorHandler:
    """Handles errors."""

    def __init__(self, logger: Logger):
        """Sets the logger to use."""
        self.logger = logger

    def __enter__(self):
        return self

    def __exit__(self, _, value, __):
        """Checks for known errors and handles them."""
        if isinstance(value, CalledProcessError):
            self.logger.critical('Subprocess error.')
            self.logger.error(value)
            exit(value.returncode)
