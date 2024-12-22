from pathlib import Path

import requests

from fridafuse import logger
from fridafuse.constants import GH_BASE_URL, LATEST_VERSION


def get_latest_version(repo: str):
    url = f'{GH_BASE_URL}/{repo}/releases/{LATEST_VERSION}'
    response = requests.get(url, allow_redirects=False, timeout=30)
    return response.headers['Location'].split('/')[-1]


def download_release_asset(repo: str, version: str, asset_name: str, output_path: Path):
    url = f'{GH_BASE_URL}/{repo}/releases/download/{version}/{asset_name}'
    output_file = output_path / asset_name
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
