import click

from fridafuse import cli, patcher


@click.command('smali')
@click.option(
    '--smali',
    help='Specify Smali file to inject (optional; default: main activity)',
)
@cli.processor
@click.pass_context
def smali(
    ctx: click.Context,
    manifest_file: str,
    smali: str,  # noqa: ARG001
):
    return patcher.inject_smali(manifest_file, gadget_version=ctx.parent.params.get('gadget_version'))
