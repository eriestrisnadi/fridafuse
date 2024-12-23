from __future__ import annotations

from typing import TYPE_CHECKING

from fridafuse.constants import ABIS, ARCHITECTURES

if TYPE_CHECKING:
    from pathlib import Path


def get_available_abis(lib_dir: Path):
    if not lib_dir.is_dir():
        return []

    return [subdir.name for subdir in lib_dir.iterdir() if subdir.is_dir()]


def get_available_archs(lib_dir: Path):
    pairs = zip(ARCHITECTURES, ABIS)

    return [(arch, abi) for arch, abi in pairs if abi in get_available_abis(lib_dir)]


def get_available_native_libs(lib_dir: Path, arch: str, excludes: list[str] | None = None):
    target_dir = lib_dir / arch

    if not target_dir.is_dir():
        return []

    if excludes is None:
        excludes = []

    return [file.name for file in target_dir.iterdir() if file.is_file() and file.name not in excludes]
