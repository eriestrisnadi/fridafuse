from fridafuse import downloader, patcher


def test_decompile_recompile_apk():
    repo = 'httptoolkit/android-ssl-pinning-demo'
    version = 'v1.4.1'
    file = downloader.download_release_asset(repo, version, 'pinning-demo.apk', downloader.CACHE_DIR)
    decompiled_dir, recompile_apk = patcher.decompile_apk(file)

    assert decompiled_dir.is_dir()
    assert decompiled_dir.name == f'{file.name}_decompiled'

    recompiled_file = recompile_apk()

    assert recompiled_file.is_file()
    assert recompiled_file.name == f'{file.stem}_patched-unsigned.apk'

    recompiled_file.unlink()
