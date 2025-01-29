from __future__ import annotations

from functools import update_wrapper
from pathlib import Path
from typing import Callable

import click

from fridafuse import logger, patcher
from fridafuse.__about__ import __title__, __version__
from fridafuse.constants import (
    ANDROID_MANIFEST_NAME,
    COMMANDS_DIR,
    GRAY,
    GREEN,
    LATEST_VERSION,
    RED,
    STOP,
)


class FridaFuseCLI(click.Group):
    def list_commands(self, _):
        click.echo(logo, color=True)
        rv = [
            path.stem.replace('_', '-')
            for path in COMMANDS_DIR.iterdir()
            if path.is_file() and not path.name.startswith('__') and path.name.endswith('.py')
        ]

        rv.sort()

        return rv

    def get_command(self, _, name):
        if isinstance(name, str):
            name = name.replace('-', '_')

        try:
            mod = __import__(f'{__title__}.commands', None, None, [name])
        except ImportError:
            return

        return mod.__dict__[name]


@click.command(name=__title__, cls=FridaFuseCLI, chain=True)
@click.argument(
    'file_path',
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
    metavar='INPUT',
    required=True,
)
@click.option('-o', '--output', type=click.Path(writable=True, path_type=Path))
@click.option('--gadget-version', help='Specify frida gadget version', default=LATEST_VERSION)
@click.option('--skip-sign', help='Skip to create signed APK', is_flag=True)
@click.option('--edit', help='Edit the APK after patched', is_flag=True)
def cli(file_path, output, gadget_version, skip_sign, edit):  # noqa: ARG001
    pass


@cli.result_callback()
@click.pass_context
def process_commands(
    ctx: click.Context,
    processors: list[Callable],
    file_path: Path,
    output: Path | None,
    gadget_version,  # noqa: ARG001
    skip_sign,
    edit,
):
    decompiled_dir, recompile_apk = patcher.decompile_apk(file_path)
    manifest_file = decompiled_dir / ANDROID_MANIFEST_NAME
    injected = False

    # Pipe it through all stream processors.
    for processor in processors:
        injected = processor(manifest_file)

    if not injected:
        ctx.exit(1)

    if edit:
        click.pause(
            f'Please edit decompiled APK on the following directory: {decompiled_dir}\nAfter editing, press any key to continue...'
        )

    if decompiled_dir.is_dir():
        patched_file = recompile_apk(output)

        if patched_file.is_file and not skip_sign:
            patcher.sign_apk(patched_file)

    logger.info('Done.')


def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """

    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        def processor(manifest_file):
            return ctx.invoke(f, manifest_file, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)


logo: str = f"""
{RED}┌─┐┬─┐┬┌┬┐┌─┐{GREEN}┌─┐┬ ┬┌─┐┌─┐
{RED}├┤ ├┬┘│ ││├─┤{GREEN}├┤ │ │└─┐├┤
{RED}└  ┴└─┴─┴┘┴ ┴{GREEN}└  └─┘└─┘└─┘{STOP}
{GRAY}(v{__version__}){STOP}
"""
