from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Callable

import inquirer
import yaml

from fridafuse import apk_utils, downloader, logger, manifest_utils, utils
from fridafuse.constants import APKTOOL_CONFIG_NAME, DEST_GADGET_NAME, LIB_DIR_NAME


def inject_smali(
    manifest_file: Path,
    *,
    lib_dir: Path | None = None,
    gadget_name: str = DEST_GADGET_NAME,
    gadget_version: str = downloader.LATEST_VERSION,
):
    err_message = "Couldn't inject into Smali"
    smali_file = manifest_utils.get_main_activity_path(manifest_file)
    lib_dir = manifest_file.parent / LIB_DIR_NAME if lib_dir is None else lib_dir

    if smali_file is None:
        return logger.error(f'{err_message}, No Main Activity found.')

    if not smali_file.is_file():
        return logger.error(f'{err_message}, {smali_file.name} is not a file.')

    injection_code = f"""
    const-string v0, "{apk_utils.lib_to_base_name(gadget_name)}"
    invoke-static {{v0}}, Ljava/lang/System;->loadLibrary(Ljava/lang/String;)V
    """

    available_archs = apk_utils.get_available_archs(lib_dir)

    if len(available_archs) <= 0:
        lib_dir.mkdir(exist_ok=True)
        available_archs = [
            (arch, abi)
            for arch, abi in zip(apk_utils.ARCHITECTURES, apk_utils.ABIS)
            if (lib_dir / abi).mkdir(exist_ok=True) or (lib_dir / abi).is_dir()
        ]

    frida_installed_list = [apk_utils.is_frida(lib_dir / abi / gadget_name) for _, abi in available_archs]
    smali_injected = apk_utils.is_smali_injected(smali_file, injection_code)

    if smali_injected and all(frida_installed_list):
        return logger.warning(f'Oops the APK is already injected using {gadget_name} on {smali_file.name}. Ignored!')

    logger.info('Checking libs...')

    if not smali_injected:
        # this will avoid duplicate injection, since we already know
        # smali is already injected, and the library is known as frida on previous process
        with smali_file.open('r') as file:
            smali_lines = file.readlines()

        pattern = r'\.method (public|protected|private|\s*) (onCreate|constructor).*'
        injection_lines = injection_code.strip().splitlines()

        for line_index, line in enumerate(smali_lines):
            if re.search(pattern, line):
                logger.info(f'Injecting frida-gadget to {smali_file.name}...')

                for range_index in range(line_index + 1, len(smali_lines)):
                    if 'invoke-direct' in smali_lines[range_index]:
                        indent = smali_lines[range_index][
                            : len(smali_lines[range_index]) - len(smali_lines[range_index].lstrip())
                        ]

                        # add a newline before the injection when needed
                        if smali_lines[range_index].strip() != '':
                            smali_lines[range_index + 1 : range_index + 1] = '\n'

                        smali_lines[range_index + 2 : range_index + 2] = [
                            f'{indent}{code_line.strip()}\n' for code_line in injection_lines
                        ]

                        # add a newline after the injection when needed
                        after_index = range_index + len(injection_lines) + 2
                        if smali_lines[after_index].strip() != '':
                            smali_lines[after_index:after_index] = '\n'

                        break
                break

        # write back patched content
        with smali_file.open('w') as file:
            file.writelines(smali_lines)

        smali_injected = True

    files_to_excludes = []

    for i, (arch, abi) in enumerate(available_archs):
        compressed_gadget = downloader.get_frida_gadget(arch, gadget_version)
        dest_gadget = utils.unpack_xz(compressed_gadget, lib_dir / abi / gadget_name)
        frida_installed_list[i] = True

        if not manifest_utils.is_extract_native_libs_enabled(manifest_file):
            relative_gadget_name = '/'.join(dest_gadget.parts[-3:])
            logger.info(f'Registering {relative_gadget_name} to doNotCompress entries...')
            files_to_excludes.append(relative_gadget_name)

    if len(files_to_excludes) > 0:
        apktool_config_file = manifest_file.parent / APKTOOL_CONFIG_NAME

        with apktool_config_file.open('r') as f:
            data = yaml.safe_load(f)

        # ensure doNotCompress exists and is a list
        if 'doNotCompress' not in data or not isinstance(data['doNotCompress'], list):
            data['doNotCompress'] = []

        # add only unique new entries to doNotCompress
        existing_entries = set(data['doNotCompress'])
        new_entries = set(files_to_excludes) - existing_entries
        data['doNotCompress'].extend(new_entries)

        with apktool_config_file.open('w') as f:
            yaml.safe_dump(data, f, default_flow_style=False)

    return smali_injected and all(frida_installed_list)


def inject_nativelib(
    lib_dir: Path,
    *,
    lib_name: str | None = None,
    gadget_name: str = DEST_GADGET_NAME,
    gadget_version: str = downloader.LATEST_VERSION,
):
    err_message = "Couldn't inject into Native Library"

    if not lib_dir.is_dir():
        return logger.error(f"{err_message}, lib directory couldn't be found.")

    available_archs = apk_utils.get_available_archs(lib_dir)

    if len(available_archs) <= 0:
        return logger.error(f'{err_message}, No supported ABIs found.')

    available_native_libs = apk_utils.get_available_native_libs(lib_dir / available_archs[0][1], gadget_name)

    if len(available_native_libs) <= 0:
        return logger.error(f'{err_message}, No Native Library found.')

    lib_name = (
        inquirer.list_input('Choose Native Library to inject:', choices=available_native_libs)
        if lib_name is None
        else lib_name
    )

    logger.info('Checking libs...')
    success_list = [False] * len(available_archs)
    skip_list = [False] * len(available_archs)

    for i, (arch, abi) in enumerate(available_archs):
        dest_abi = lib_dir / abi
        dest_gadget = dest_abi / gadget_name
        dest_lib = dest_abi / lib_name
        relative_lib_name = '/'.join(dest_lib.parts[-2:])

        if apk_utils.is_lib_injected(dest_gadget, dest_lib):
            if apk_utils.is_frida(dest_gadget):
                logger.info(f'Already injected {dest_gadget.name} into {relative_lib_name}. Skiping...')
                skip_list[i] = True
                success_list[i] = True
                continue

            # TODO: suggest to change frida-gadget name due to conflicting with other native lib
            logger.error(f'{err_message}, conflicting name {dest_gadget.name} with {relative_lib_name}.')
            break

        compressed_gadget = downloader.get_frida_gadget(arch, version=gadget_version)
        gadget_file = utils.unpack_xz(compressed_gadget, dest_gadget)
        logger.info(f'Injecting frida-gadget to {relative_lib_name}')
        elf = apk_utils.elf_reader.parse(dest_lib)
        elf.add_library(gadget_file.name)
        elf.write(str(dest_lib))

        if not apk_utils.is_lib_injected(gadget_file, dest_lib, verbose=True):
            logger.error(f'{err_message}, failed to do ELF injection.')
        elif apk_utils.is_frida(dest_gadget):
            success_list[i] = True

    if all(skip_list):
        return logger.warning(f'the APK is already injected using {gadget_name} on {lib_name}. Ignored!')

    return all(success_list)


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
