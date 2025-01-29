from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

import click

from fridafuse import cli, commands, constants


@click.command('auto')
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
@click.option(
    '--smali',
    help='Specify Smali file to inject (optional; default: main activity)',
)
@cli.processor
@click.pass_context
def auto(
    ctx: click.Context,
    manifest_file: Path,
    lib: str,
    abis: tuple[str],
    smali: str,
):
    injected = ctx.parent.invoke(commands.native_lib, lib=lib, abis=abis)(manifest_file)

    if not injected:
        injected = ctx.parent.invoke(commands.smali, smali=smali)(manifest_file)

    return injected
