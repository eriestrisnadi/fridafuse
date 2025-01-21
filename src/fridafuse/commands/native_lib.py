from pathlib import Path

import click

from fridafuse import cli, constants, patcher


@click.command('native-lib')
@click.option(
    '--lib',
    '-l',
    '-so',
    help='Specify Native Library to inject (optional; default: questionnaire)',
)
@click.option('--abi', help='Specify ABI to inject (optional; default: all)')
@cli.processor
@click.pass_context
def native_lib(
    ctx: click.Context,
    manifest_file: Path,
    lib: str,
    abi: str,  # noqa: ARG001
):
    return patcher.inject_nativelib(
        lib_dir=manifest_file.parent / constants.LIB_DIR_NAME,
        lib_name=lib,
        gadget_version=ctx.parent.params.get('gadget_version'),
    )
