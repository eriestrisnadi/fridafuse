import shutil
from pathlib import Path

import pytest

from fridafuse import downloader, patcher


@pytest.fixture
def apk_mock(mocker, tmp_path):
    mocker.patch('fridafuse.downloader.CACHE_DIR', tmp_path)
    mocker.patch('builtins.open', mocker.mock_open())
    repo = 'httptoolkit/android-ssl-pinning-demo'
    version = 'v1.4.1'
    apk_file = downloader.download_release_asset(repo, version, 'pinning-demo.apk', tmp_path)

    yield apk_file

    apk_file.unlink()


def test_decompile_recompile_apk(apk_mock: Path, tmp_path: Path):
    file = apk_mock
    decompiled_dir, recompile_apk = patcher.decompile_apk(file)

    assert decompiled_dir.is_dir()
    assert decompiled_dir.name == f'{file.name}_decompiled'

    recompiled_file = recompile_apk(tmp_path / f'{file.stem}_patched-unsigned.apk')

    assert recompiled_file.is_file()
    assert 'patched-unsigned' in recompiled_file.name

    recompiled_file.unlink()
    shutil.rmtree(decompiled_dir)
