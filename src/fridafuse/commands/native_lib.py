from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import click

from fridafuse import cli, constants, patcher


@click.command('native-lib')
@click.option(
    '--lib',
    '-l',
    '-so',
    help='Specify Native Library to inject (default: questionnaire)',
)
@click.option(
    '--abis',
    type=click.Choice(constants.ABIS, case_sensitive=False),
    multiple=True,
    help='Specify ABIs to inject',
    default=constants.ABIS,
)
@cli.processor
@click.pass_context
def native_lib(
    ctx: click.Context,
    manifest_file: Path,
    lib: str,
    abis: tuple[str],
):
    return patcher.inject_nativelib(
        lib_dir=manifest_file.parent / constants.LIB_DIR_NAME,
        lib_name=lib,
        gadget_version=ctx.parent.params.get('gadget_version'),
        abis=list(abis) if abis else None,
    )
