from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

from fridafuse import downloader, logger, utils


# TODO: Implement Smali injection
def inject_smali():
    pass


# TODO: Implement Native Lib injection
def inject_nativelib():
    pass


def decompile_apk(file: Path) -> tuple[Path, Callable[[Path | None], Path]]:
    logger.info('Checking Apktool...')
    apktool = downloader.get_apktool()
    decompiled_dir = downloader.CACHE_DIR / f'{file.stem}_decompiled'

    logger.info(f'Checking {file}...')
    utils.spawn_subprocess(['java', '-jar', apktool, 'd', file, '-o', decompiled_dir, '-f'])
    utils.spawn_subprocess(['java', '-jar', apktool, 'empty-framework-dir'])

    return decompiled_dir, lambda output_file=None: recompile_apk(
        decompiled_dir, f'{file.stem}_patched-unsigned.apk' if output_file is None else output_file
    )


def recompile_apk(decompiled_dir: Path, output_file: Path):
    logger.info('Checking Apktool...')
    apktool = downloader.get_apktool()
    output_file = Path.resolve(Path.cwd() / output_file)

    logger.info('Prepare to recompile apk...')
    utils.spawn_subprocess(['java', '-jar', apktool, 'b', decompiled_dir, '-o', output_file])

    return output_file


def sign_apk(file: Path, output_file: Path | None = None):
    err_message = "Couldn't sign the apk"
    temp_dir = downloader.CACHE_DIR / f'{file.stem}_signed'

    if not file.exists() or file.is_dir():
        return logger.info(f'{err_message}, {file} {"is not a file" if file.is_dir() else "is not exists"}')

    logger.info('Checking Apksigner...')
    apksigner = downloader.get_apksigner()

    logger.info('Signing the patched apk...')
    utils.spawn_subprocess(['java', '-jar', apksigner, '-a', file, '-o', temp_dir])

    files = [f for f in temp_dir.iterdir() if f.is_file() and f.suffix in ['.apk', '.idsig']]

    if len(files) < 1:
        return logger.info(f'{err_message}, please sign the {file.name} with other tool instead.')

    for item in files:
        out_file = (
            file.parent / item.name if not output_file else output_file.parent / f'{output_file.stem}{item.suffix}'
        )

        shutil.copy(item, out_file)

        if out_file.suffix == '.apk':
            output_file = out_file

    shutil.rmtree(temp_dir)

    return output_file
