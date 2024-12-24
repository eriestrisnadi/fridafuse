from pathlib import Path

import requests

from fridafuse import logger
from fridafuse.constants import CACHE_DIR, GH_BASE_URL, LATEST_VERSION


def get_latest_version(repo: str):
    url = f'{GH_BASE_URL}/{repo}/releases/{LATEST_VERSION}'
    response = requests.get(url, allow_redirects=False, timeout=30)
    return response.headers['Location'].split('/')[-1]


def download_release_asset(repo: str, version: str, asset_name: str, output_path: Path):
    url = f'{GH_BASE_URL}/{repo}/releases/download/{version}/{asset_name}'
    output_file = output_path / asset_name

    if not output_file.parent.is_dir():
        output_file.parent.mkdir(exist_ok=True, parents=True)

    is_already_downloaded = output_file.is_file()

    if is_already_downloaded:
        return output_file

    logger.info(f'Downloading {asset_name}...')
    response = requests.get(url, stream=True, timeout=30)
    response.raise_for_status()

    with output_file.open('wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

    logger.info('Download complete')
    return output_file


def get_apktool(version: str = LATEST_VERSION):
    repo = 'iBotPeaches/Apktool'
    version = f'v{version}' if version != LATEST_VERSION else get_latest_version(repo)
    asset_name = f'apktool_{version[1:]}.jar'

    return download_release_asset(repo, version, asset_name, CACHE_DIR)


def get_frida_gadget(arch: str, version: str = LATEST_VERSION):
    repo = 'frida/frida'
    target_os = 'android'
    version = version if version != LATEST_VERSION else get_latest_version(repo)
    asset_name = f'frida-gadget-{version}-{target_os}-{arch}.so.xz'

    return download_release_asset(repo, version, asset_name, CACHE_DIR)


def get_apksigner(version: str = LATEST_VERSION):
    repo = 'patrickfav/uber-apk-signer'
    version = f'v{version}' if version != LATEST_VERSION else get_latest_version(repo)
    asset_name = f'uber-apk-signer-{version[1:]}.jar'

    return download_release_asset(repo, version, asset_name, CACHE_DIR)
