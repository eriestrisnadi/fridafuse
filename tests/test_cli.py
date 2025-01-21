from pathlib import Path

import click
from click.testing import CliRunner

from fridafuse import cli
from fridafuse.__about__ import __title__, __version__


def test_cli():
    assert isinstance(cli.cli, click.Group)
    assert CliRunner().get_default_prog_name(cli.cli) is __title__
    assert CliRunner().invoke(cli.cli, color=True).exit_code == 0

    demo_apk = Path('tests/test_files/demo.apk')

    result = CliRunner().invoke(cli.cli, [demo_apk.as_posix()])

    assert result.exit_code
    assert result.exception
    assert 'Usage:' in result.output
    assert 'Error: Missing command.' in result.output

    result = CliRunner().invoke(cli.cli, [demo_apk.as_posix(), 'auto'])

    assert result.exit_code
    assert 'Choose Native Library' in result.output


def test_print_logo(capsys):
    click.echo(cli.logo, color=True)
    captured = capsys.readouterr()

    assert cli.logo in captured.out
    assert __version__ in captured.out
