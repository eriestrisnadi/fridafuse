import logging

from . import cli


def main():
    print(cli.logo())
    args = cli.parse_args()

    logging.info('Done.')
