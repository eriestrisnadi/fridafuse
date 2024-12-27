from __future__ import annotations

import argparse
from typing import Sequence

from fridafuse.__about__ import __description__, __title__, __version__
from fridafuse.constants import GRAY, GREEN, LATEST_VERSION, RED, STOP

logo: str = f"""
{RED}┌─┐┬─┐┬┌┬┐┌─┐{GREEN}┌─┐┬ ┬┌─┐┌─┐
{RED}├┤ ├┬┘│ ││├─┤{GREEN}├┤ │ │└─┐├┤
{RED}└  ┴└─┴─┴┘┴ ┴{GREEN}└  └─┘└─┘└─┘{STOP}
{GRAY}(v{__version__}){STOP}
"""


def create_parser(prog: str | None = None, description: str | None = None, **kwargs):
    prog = prog if prog is not None else __title__
    description = description if description is not None else __description__

    return argparse.ArgumentParser(prog=prog, description=description, **kwargs)


def parse_args(args: Sequence[str] | None, **kwargs):
    parser = create_parser()

    # Shared arguments
    shared_parser = argparse.ArgumentParser(add_help=False)
    shared_parser.add_argument('input', metavar='INPUT_FILE', help='Input file (e.g., APK)')
    shared_parser.add_argument('output', metavar='OUTPUT_FILE', help='Output file', nargs='?')
    shared_parser.add_argument('--gadget-version', help='Specify frida gadget version', default=LATEST_VERSION)
    shared_parser.add_argument(
        '--skip-sign', help='Skip to create signed APK', default=True, action='store_false', dest='sign'
    )

    # Methods (Subcommands)
    subparsers = parser.add_subparsers(title='methods', dest='method', required=True)
    parser_nativelib = subparsers.add_parser('native-lib', parents=[shared_parser], help='Inject into Native Library')
    parser_smali = subparsers.add_parser('smali', parents=[shared_parser], help='Inject into Smali')
    parser_auto = subparsers.add_parser(
        'auto', parents=[shared_parser], help='Auto inject using native-lib method first, fallback to smali method'
    )

    # Native Lib Method additional arguments
    parser_nativelib.add_argument(
        '--lib', '-l', '-so', help='Specify Native Library to inject (optional; default: questionnaire)', dest='lib'
    )
    parser_nativelib.add_argument('--abi', help='Specify ABI to inject (optional; default: all)')

    # Smali Method additional arguments
    parser_smali.add_argument(
        '--smali', metavar='PATH', help='Specify Smali file to inject (optional; default: main activity)'
    )

    # Auto Method additional arguments
    for action in [*parser_nativelib._actions, *parser_smali._actions]:  # noqa: SLF001
        if action.dest not in {
            existing_action.dest
            for existing_action in [*shared_parser._actions, *parser_auto._actions]  # noqa: SLF001
        }:
            parser_auto.add_argument(
                *action.option_strings,
                **{key: value for key, value in vars(action).items() if key not in {'container'}},
            )

    return parser.parse_args(args, **kwargs)


def print_logo():
    print(logo)
