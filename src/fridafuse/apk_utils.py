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


def mask_dynamic_registers(snippet: str, as_mask: str = '<dynamic-register>') -> str:
    # replace matches any register name (e.g., v0, p0, a0, etc.)
    return re.sub(r'\{+[a-zA-Z]+\d+\}', f'{{{as_mask}}}', re.sub(r'\s+[a-zA-Z]+\d+\,', f' {as_mask},', snippet))


def is_smali_injected(content: str | Path, snippet: str):
    resolved_content = content.read_text(encoding='utf-8') if content is not str else content

    normalized_content = '\n'.join([line.strip() for line in resolved_content.splitlines() if line.strip()])

    snippet_lines = [line.strip() for line in mask_dynamic_registers(snippet).splitlines() if line.strip()]
    snippet_pattern = r'\s*'.join(
        re.escape(line).replace(r'<dynamic\-register>', r'[a-zA-Z]+\d+') for line in snippet_lines
    )

    return bool(re.search(snippet_pattern, normalized_content, re.DOTALL))


def is_lib_injected(src: Path, target: Path, *, verbose: bool = False):
    return src.name in [info for (_, _, info) in elf_reader.get_needed(src=target, verbose=verbose)]


def is_frida(file: Path):
    if not file.is_file():
        return False

    return 'frida' in ' '.join(
        [info for (tag, _, info) in elf_reader.get_needed(file, verbose=False) if tag == 'SONAME']
    )
