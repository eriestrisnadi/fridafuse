from fridafuse import downloader


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
