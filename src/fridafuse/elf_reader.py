from __future__ import annotations

from typing import TYPE_CHECKING

from lief import ELF, parse

from fridafuse import logger

if TYPE_CHECKING:
    from pathlib import Path


def get_needed(src: Path, *, verbose: bool = False) -> list[tuple[str, str, str]]:
    dynamic_entries = parse(src).dynamic_entries
    result = []

    if len(dynamic_entries) <= 0:
        return result

    if verbose:
        logger.info('== Dynamic entries ==')
        f_title = '| {:<16} | {:<10}| {:<20}|'
        f_value = '| {:<16} | 0x{:<8}| {:<20}|'
        logger.info(f_title.format('Tag', 'Value', 'Info'))

    for entry in dynamic_entries:
        if entry.tag == ELF.DynamicEntry.TAG.NULL:
            continue

        if entry.tag not in [ELF.DynamicEntry.TAG.NEEDED, ELF.DynamicEntry.TAG.SONAME]:
            continue

        parts = [str(entry.tag).split('.')[-1], entry.value, entry.name]
        result.append(tuple(parts))

        if verbose:
            # Convert value to hex if it's a valid integer
            value = int(parts[1], 16) if parts[1] is int else parts[1]
            logger.info(f_value.format(parts[0], value, parts[2]))

    return result
