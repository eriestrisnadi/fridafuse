from typing import Sequence

from . import cli, logger


def main(args: Sequence[str] | None = None, **kwargs):
    cli.print_logo()
    cli.parse_args(args, **kwargs)
    logger.info('Starting...')

    # TODO: Implement the main functionality here
    # raise NotImplementedError('Not implemented yet')

    logger.info('Done.')
