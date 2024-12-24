from __future__ import annotations

from pathlib import Path
from typing import Sequence

from fridafuse import cli, logger, patcher


def main(args: Sequence[str] | None = None, **kwargs):
    cli.print_logo()
    args = cli.parse_args(args, **kwargs)
    logger.info('Starting...')
    input_file = Path(args.input)
    output_file = None if not args.output else Path(args.output)

    decompiled_dir, recompile_apk = patcher.decompile_apk(input_file)

    # TODO: Implement the main functionality here
    # raise NotImplementedError('Not implemented yet')
    if args.method == 'smali':
        'Smali method'
    elif args.method == 'native-lib':
        'Native Library method'
    else:
        'Auto method'

    if decompiled_dir.is_dir():
        patched_file = recompile_apk(output_file)

        if patched_file.is_file and args.sign:
            patcher.sign_apk(patched_file)

    logger.info('Done.')
