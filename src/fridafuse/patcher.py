from __future__ import annotations

from pathlib import Path

from fridafuse import downloader, logger, utils


def decompile_apk(file: Path):
    logger.info('Checking Apktool...')
    apktool = downloader.get_apktool()
    decompiled_dir = downloader.CACHE_DIR / f'{file}_decompiled'

    def recompile_apk(output_file: Path | None = None):
        recompiled_file = Path.cwd() / f'{file.stem}_patched-unsigned.apk' if output_file is None else output_file

        logger.info('Prepare to recompile apk...')
        utils.spawn_subprocess(['java', '-jar', apktool, 'b', decompiled_dir, '-o', recompiled_file])

        return recompiled_file

    logger.info(f'Checking {file}...')
    utils.spawn_subprocess(['java', '-jar', apktool, 'd', file, '-o', decompiled_dir, '-f'])
    utils.spawn_subprocess(['java', '-jar', apktool, 'empty-framework-dir'])

    return decompiled_dir, recompile_apk
