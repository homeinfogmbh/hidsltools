"""Bsdtar invocation."""

from pathlib import Path

from hidsltools.functions import exe
from hidsltools.types import Compression


__all__ = ["bsdtar", "create", "extract"]


BSDTAR = "/usr/bin/bsdtar"


def bsdtar(
    tarball: Path,
    *files: Path,
    chdir: Path | None = None,
    compression: Compression = Compression.LZOP,
    compression_level: int = 9,
    verbose: bool = False,
) -> None:
    """Creates a tarball from the given files."""

    command = [BSDTAR, "-c", "-p", "-f", str(tarball)]
    options = []

    if chdir:
        command += ["-C", str(chdir)]

    if verbose:
        command.append("-v")

    if compression is not None:
        command.append(f"--{compression.full_name}")

    if compression_level is not None:
        options.append(f"compression-level={compression_level}")

    if options:
        command += ["--options", ",".join(options)]

    exe([*command, *files], verbose=verbose)


def create(
    tarball: Path,
    root: Path,
    *,
    compression: Compression = Compression.LZOP,
    compression_level: int = 9,
    verbose: bool = False,
) -> None:
    """Creates a tarball from a root file system mount point."""

    files = [inode.relative_to(root) for inode in root.iterdir()]
    return bsdtar(
        tarball,
        *files,
        chdir=root,
        compression=compression,
        compression_level=compression_level,
        verbose=verbose,
    )


def extract(
    tarball: Path, target: Path | None = None, *, verbose: bool = False
) -> None:
    """Extracts an image using bsdtar."""

    command = [BSDTAR, "-x", "-p", "-f", str(tarball)]

    if verbose:
        command.append("-v")

    if target is not None:
        command += ["-C", str(target)]

    exe(command, verbose=verbose)
