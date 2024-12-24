from __future__ import annotations

import re
from typing import TYPE_CHECKING

from fridafuse import elf_reader
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


def get_available_native_libs(arch_dir: Path, excludes: list[str] | None = None):
    if not arch_dir.is_dir():
        return []

    if excludes is None:
        excludes = []

    return [file.name for file in arch_dir.iterdir() if file.is_file() and file.name not in excludes]


def lib_to_base_name(lib_name: str):
    return re.sub(r'^(lib)?(.*?)(\.[^.]+)?$', r'\2', lib_name)


def is_smali_injected(injection_code: str, smali_file: Path):
    injection_lines = [line.strip() for line in str(injection_code).strip().splitlines()]

    with smali_file.open('r') as file:
        smali_content = file.read()

    smali_lines = [line.strip() for line in smali_content.splitlines()]

    return all(line in smali_lines for line in injection_lines)


def is_lib_injected(src: Path, target: Path, *, verbose: bool = False):
    return src.name in [info for (_, _, info) in elf_reader.get_needed(src=target, verbose=verbose)]


def is_frida(file: Path):
    if not file.is_file():
        return False

    return 'frida' in ' '.join(
        [info for (tag, _, info) in elf_reader.get_needed(file, verbose=False) if tag == 'SONAME']
    )
