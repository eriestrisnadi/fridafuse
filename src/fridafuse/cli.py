import argparse
from typing import Sequence

from .__about__ import __description__, __name__, __version__

RED: str = '\033[0;91m'
GREEN: str = '\033[0;92m'
GRAY: str = '\033[0;90m'
STOP: str = '\033[0m'

logo: str = f'''
{RED}┌─┐┬─┐┬┌┬┐┌─┐{GREEN}┌─┐┬ ┬┌─┐┌─┐
{RED}├┤ ├┬┘│ ││├─┤{GREEN}├┤ │ │└─┐├┤
{RED}└  ┴└─┴─┴┘┴ ┴{GREEN}└  └─┘└─┘└─┘{STOP}
{GRAY}(v{__version__}){STOP}
'''

def create_parser(
    prog: str = None,
    description: str = None,
    **kwargs
):
    prog = prog if prog is not None else __name__
    description = description if description is not None else __description__

    return argparse.ArgumentParser(
        prog=prog,
        description=description,
        **kwargs
    )

def parse_args(args: Sequence[str] | None, **kwargs):
    parser = create_parser()

    return parser.parse_args(args, **kwargs)

def print_logo(): print(logo)