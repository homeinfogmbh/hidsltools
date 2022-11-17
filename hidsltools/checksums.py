"""Validate checksums."""

from hashlib import sha256
from pathlib import Path
from typing import Callable

from hidsltools.types import Hash


__all__ = ['validate']


def validate(
        checksums: dict[Path, str],
        *,
        hash_func: Callable[[bytes], Hash] = sha256
) -> bool:
    """Validate files with a hash function."""

    for path, checksum in checksums.items():
        with path.open('rb') as file:
            if (hex_hash := hash_func(file.read()).hexdigest()) != checksum:
                raise ValueError(
                    f'Checksum mismatch: {path} ({hex_hash} != {checksum})'
                )

    return True
