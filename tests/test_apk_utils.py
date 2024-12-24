from pathlib import Path
from unittest.mock import MagicMock

import pytest

from fridafuse import apk_utils


@pytest.fixture
def mock_lib_dir():
    lib_dir = MagicMock(spec=Path, is_dir=MagicMock(return_value=True), iterdir=MagicMock(return_value=[]))

    for abi in ['x86', 'x86_64', 'armeabi-v7a', 'arm64-v8a']:
        sub_dir = MagicMock(spec=Path, is_dir=MagicMock(return_value=True))
        sub_dir.name = abi
        lib_dir.iterdir.return_value.append(sub_dir)

    return lib_dir


def test_get_available_abis(mock_lib_dir):
    mock_lib_dir.is_dir.return_value = False
    assert apk_utils.get_available_abis(mock_lib_dir) == []

    mock_lib_dir.is_dir.return_value = True
    mock_lib_dir.iterdir.return_value = [
        filtered for filtered in mock_lib_dir.iterdir.return_value if '64' in filtered.name
    ]
    assert apk_utils.get_available_abis(mock_lib_dir) == ['x86_64', 'arm64-v8a']


def test_get_available_archs(mock_lib_dir):
    mock_lib_dir.is_dir.return_value = False
    assert apk_utils.get_available_abis(mock_lib_dir) == []

    mock_lib_dir.is_dir.return_value = True
    mock_lib_dir.iterdir.return_value = [
        filtered
        for filtered in mock_lib_dir.iterdir.return_value
        if '64' in filtered.name or 'armeabi-v7a' in filtered.name
    ]
    available_archs = apk_utils.get_available_archs(mock_lib_dir)

    for expected_arch in [('x86_64', 'x86_64'), ('arm', 'armeabi-v7a'), ('arm64', 'arm64-v8a')]:
        assert expected_arch in available_archs


def test_get_available_native_libs(mock_lib_dir):
    arch_dir = mock_lib_dir / 'x86_64'

    arch_dir.is_dir.return_value = False
    assert apk_utils.get_available_native_libs(arch_dir) == []

    arch_dir.is_dir.return_value = True
    assert apk_utils.get_available_native_libs(arch_dir) == []

    arch_dir.iterdir.return_value = []

    libs = ['libc.so', 'libgcc.so', 'there_is_subdir', 'libmain.so']

    for lib in libs:
        lib_file = MagicMock(spec=Path, is_file=MagicMock(return_value=(lib != libs[2])))
        lib_file.name = lib
        arch_dir.iterdir.return_value.append(lib_file)

    assert apk_utils.get_available_native_libs(arch_dir) == [lib for lib in libs if lib != libs[2]]
    assert libs[1] not in apk_utils.get_available_native_libs(arch_dir, excludes=[libs[1]])
