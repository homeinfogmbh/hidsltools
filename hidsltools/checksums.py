"""Validate checksums."""

from hashlib import sha256
from pathlib import Path
from typing import Callable, Iterator

from hidsltools.logging import LOGGER
from hidsltools.types import Hash


__all__ = ['validate_files']


CHECKSUMS_FILE = Path('/opt/hidsl/.checksums.sha256')


def validate_files() -> None:
    """Validate checksums of critical files."""

    for filename, checksum in iter_hashes():
        try:
            validate(filename, checksum)
        except ValueError as error:
            LOGGER.error('Hashes differ for file: "%s"', filename)
            LOGGER.debug(str(error))
            raise SystemExit(1) from error
        except FileNotFoundError as error:
            LOGGER.error('File "%s" not found.', filename)
            LOGGER.debug(str(error))
            raise SystemExit(1) from error
        else:
            LOGGER.info('File "%s": ok', filename)


def iter_hashes(hashes: Path = CHECKSUMS_FILE) -> Iterator[tuple[Path, str]]:
    """Load hashes from file."""

    with hashes.open('r', encoding='utf-8') as file:
        for line in file:
            if line := line.strip():
                checksum, filename = line.split()
                yield hashes.parent / filename, checksum


def validate(
        filename: Path,
        checksum: str,
        *,
        hash_func: Callable[[bytes], Hash] = sha256
) -> bool:
    """Validate files with a hash function."""

    with filename.open('rb') as file:
        if (hex_hash := hash_func(file.read()).hexdigest()) != checksum:
            raise ValueError(
                f'Checksum mismatch: {filename} ({hex_hash} != {checksum})'
            )

    return True
