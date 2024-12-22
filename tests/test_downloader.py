import re
import shutil

from fridafuse import downloader


def version_tuple(v):
    return tuple(map(int, (re.search(r'\d+(?:\.\d+){1,2}', v).group().split('.'))))


shutil.rmtree(downloader.CACHE_DIR, ignore_errors=True)
downloader.CACHE_DIR.mkdir(exist_ok=True)


def test_get_latest_version(requests_mock):
    version = 'v2.5.0'
    repo = 'test/test'
    release_url = '{}/{}/releases/{}'.format(downloader.GH_BASE_URL, repo, '{}')

    requests_mock.get(
        release_url.format(downloader.LATEST_VERSION),
        headers={'Location': release_url.format('tag/' + version)},
    )

    assert downloader.get_latest_version(repo) == version


def test_download_release_asset(requests_mock, tmp_path):
    repo = 'test/test'
    version = 'v2.5.0'
    asset_name = 'test-2.5.0.txt'
    output_path = tmp_path / 'test'
    output_path.mkdir(exist_ok=True)
    asset_url = f'{downloader.GH_BASE_URL}/{repo}/releases/download/{version}/{asset_name}'

    requests_mock.get(asset_url, content=b'test content')

    asset_file = downloader.download_release_asset(repo, version, asset_name, output_path)
    already_downloaded_file = downloader.download_release_asset(repo, version, asset_name, output_path)

    assert asset_file.parent == output_path
    assert asset_file.is_file()
    assert asset_file.name == asset_name
    assert asset_file.read_text() == 'test content'
    assert already_downloaded_file.is_file()
    assert already_downloaded_file == asset_file


def test_get_apktool():
    old_version = '2.2.1'
    apktool = downloader.get_apktool()
    apktool_old_version = downloader.get_apktool(old_version)

    assert apktool.is_file()
    assert 'apktool' in apktool.name

    assert apktool_old_version.is_file()
    assert 'apktool' in apktool_old_version.name
    assert old_version in apktool_old_version.name

    assert version_tuple(apktool.name) > version_tuple(apktool_old_version.name)


def test_get_frida_gadget():
    old_version = '15.2.2'
    frida_gadget = downloader.get_frida_gadget('arm64')
    frida_gadget_old_version = downloader.get_frida_gadget('arm64', old_version)

    assert frida_gadget.is_file()
    assert 'frida-gadget' in frida_gadget.name
    assert 'arm64' in frida_gadget.name

    assert frida_gadget_old_version.is_file()
    assert 'frida-gadget' in frida_gadget_old_version.name
    assert 'arm64' in frida_gadget_old_version.name
    assert old_version in frida_gadget_old_version.name

    assert version_tuple(frida_gadget.name) > version_tuple(frida_gadget_old_version.name)


def test_get_apksigner():
    old_version = '0.8.4'
    apksigner = downloader.get_apksigner()
    apksigner_old_version = downloader.get_apksigner(old_version)

    assert apksigner.is_file()
    assert 'uber-apk-signer' in apksigner.name

    assert apksigner_old_version.is_file()
    assert 'uber-apk-signer' in apksigner_old_version.name
    assert old_version in apksigner_old_version.name

    assert version_tuple(apksigner.name) > version_tuple(apksigner_old_version.name)
