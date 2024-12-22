from __future__ import annotations

import argparse
from typing import Sequence

from fridafuse.__about__ import __description__, __title__, __version__
from fridafuse.constants import GRAY, GREEN, RED, STOP

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

    return parser.parse_args(args, **kwargs)


def print_logo():
    print(logo)
