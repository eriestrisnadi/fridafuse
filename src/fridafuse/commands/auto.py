from pathlib import Path

import click

from fridafuse import cli, commands


@click.command('auto')
@click.option(
    '--lib',
    '-l',
    '-so',
    help='Specify Native Library to inject (optional; default: questionnaire)',
)
@click.option('--abi', help='Specify ABI to inject (optional; default: all)')
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
    abi: str,
    smali: str,
):
    injected = ctx.parent.invoke(commands.native_lib, lib=lib, abi=abi)(manifest_file)

    if not injected:
        injected = ctx.parent.invoke(commands.smali, smali=smali)(manifest_file)

    return injected
