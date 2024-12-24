from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from fridafuse import manifest_utils

sample_manifest = """
<?xml version="1.0" encoding="utf-8"?>
    <manifest xmlns:android="http://schemas.android.com/apk/res/android" package="com.example.fridafuse">
        {}
    </manifest>
""".strip()
sample_path = Path('/fake/path/AndroidManifest.xml')


@pytest.fixture
def decompiled_mock(tmp_path: Path):
    decompiled_dir = tmp_path / 'test.apk_decompiled'
    decompiled_dir.mkdir(parents=True, exist_ok=True)

    manifest_file = decompiled_dir / 'AndroidManifest.xml'
    manifest_file_without_main_activity = decompiled_dir / 'AndroidManifestWithoutMainActivity.xml'

    smali_file = decompiled_dir / 'smali/com/example/fridafuse/MainActivity.smali'

    smali_file.parent.mkdir(parents=True, exist_ok=True)

    manifest_file.write_text(
        sample_manifest.format("""
    <application>
        <activity android:name="com.example.fridafuse.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
""").strip()
    )

    manifest_file_without_main_activity.write_text(
        sample_manifest.format("""
    <application>
        <activity android:name="com.example.fridafuse.SecondActivity"/>
    </application>
""").strip()
    )

    smali_file.touch(exist_ok=True)

    yield {
        'decompiled_dir': decompiled_dir,
        'manifest_file': manifest_file,
        'manifest_file_without_main_activity': manifest_file_without_main_activity,
        'smali_file': smali_file,
    }

    shutil.rmtree(decompiled_dir)


def test_get_main_activity(decompiled_mock: dict[str, Path]):
    manifest_file = decompiled_mock['manifest_file']
    manifest_file_without_main_activity = decompiled_mock['manifest_file_without_main_activity']
    main_activity = manifest_utils.get_main_activity(manifest_file)
    second_activity = manifest_utils.get_main_activity(manifest_file_without_main_activity)

    assert main_activity == 'com.example.fridafuse.MainActivity'

    manifest_file.unlink()

    main_activity = manifest_utils.get_main_activity(manifest_file)

    assert main_activity is None
    assert second_activity is None


def test_get_main_activity_path(decompiled_mock: dict[str, Path]):
    manifest_file = decompiled_mock['manifest_file']
    manifest_file_without_main_activity = decompiled_mock['manifest_file_without_main_activity']
    smali_file = decompiled_mock['smali_file']
    main_activity_path = manifest_utils.get_main_activity_path(manifest_file)
    second_activity_path = manifest_utils.get_main_activity_path(manifest_file_without_main_activity)

    assert main_activity_path == smali_file

    manifest_file.unlink()

    main_activity_path = manifest_utils.get_main_activity_path(manifest_file)

    assert main_activity_path is None
    assert second_activity_path is None


def test_get_root_manifest(mocker):
    mocker.patch.object(Path, 'is_file', return_value=True)

    mocker.patch.object(Path, 'is_file', return_value=False)
    assert manifest_utils.get_root_manifest(sample_path) is None

    mocker.patch.object(Path, 'is_file', return_value=True)

    mocker.patch('builtins.open', mocker.mock_open(read_data=sample_manifest.format('<application />')))
    assert manifest_utils.get_root_manifest(sample_path) is not None

    mocker.patch('builtins.open', mocker.mock_open(read_data=sample_manifest))
    assert manifest_utils.get_root_manifest(sample_path) is not None


def test_is_extract_native_libs_enabled(mocker):
    mocker.patch.object(Path, 'is_file', return_value=False)
    assert manifest_utils.is_extract_native_libs_enabled(sample_path) is None

    mocker.patch.object(Path, 'is_file', return_value=True)

    mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data=sample_manifest.format('<application android:extractNativeLibs="true"/>')),
    )
    assert manifest_utils.is_extract_native_libs_enabled(sample_path) is True

    mocker.patch(
        'builtins.open',
        mocker.mock_open(read_data=sample_manifest.format('<application android:extractNativeLibs="false"/>')),
    )
    assert manifest_utils.is_extract_native_libs_enabled(sample_path) is False

    mocker.patch('builtins.open', mocker.mock_open(read_data=sample_manifest.format('<application />')))
    assert manifest_utils.is_extract_native_libs_enabled(sample_path) is True

    mocker.patch('builtins.open', mocker.mock_open(read_data=sample_manifest))
    assert manifest_utils.is_extract_native_libs_enabled(sample_path) is None
