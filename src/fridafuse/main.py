from __future__ import annotations

import sys
from pathlib import Path
from typing import Sequence

from fridafuse import cli, constants, logger, patcher


def main(args: Sequence[str] | None = None, **kwargs):
    cli.print_logo()
    args = cli.parse_args(args, **kwargs)
    logger.info('Starting...')
    input_file = Path(args.input)
    output_file = None if not args.output else Path(args.output)

    decompiled_dir, recompile_apk = patcher.decompile_apk(input_file)
    manifest_file = decompiled_dir / constants.ANDROID_MANIFEST_NAME

    if args.method == 'smali':
        if not patcher.inject_smali(manifest_file):
            sys.exit(1)
    elif args.method == 'native-lib':
        if not patcher.inject_nativelib(lib_dir=manifest_file.parent / constants.LIB_DIR_NAME, lib_name=args.lib):
            sys.exit(1)
    elif not patcher.inject_nativelib(lib_dir=manifest_file.parent / constants.LIB_DIR_NAME, lib_name=args.lib):
        logger.warning('Native Library injection failed, trying smali...')
        if not patcher.inject_smali(manifest_file):
            sys.exit(1)

    if decompiled_dir.is_dir():
        patched_file = recompile_apk(output_file)

        if patched_file.is_file and args.sign:
            patcher.sign_apk(patched_file)

    logger.info('Done.')
