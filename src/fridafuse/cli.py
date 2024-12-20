import argparse

from .__about__ import __description__, __name__, __version__

RED = '\033[0;91m'
GREEN = '\033[0;92m'
GRAY = '\033[0;90m'
STOP = '\033[0m'

def logo():
    banner = f'''
{RED}┌─┐┬─┐┬┌┬┐┌─┐{GREEN}┌─┐┬ ┬┌─┐┌─┐
{RED}├┤ ├┬┘│ ││├─┤{GREEN}├┤ │ │└─┐├┤
{RED}└  ┴└─┴─┴┘┴ ┴{GREEN}└  └─┘└─┘└─┘{STOP}
{GRAY}(v{__version__}){STOP}
'''

    return banner

def parse_args():
    parser = argparse.ArgumentParser(
        prog=__name__,
        description=__description__,
    )

    return parser.parse_args()
