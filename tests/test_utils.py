from __future__ import annotations

import logging
from unittest.mock import MagicMock
from random import choice
from subprocess import CalledProcessError, CompletedProcess
from typing import TYPE_CHECKING

import pytest

from fridafuse import utils

from pathlib import Path


def test_stdout_handler(caplog):
    caplog.set_level(logging.DEBUG)
    levels = ['I', 'WARN', 'Error', 'debug', 'unknown']
    messages = ['lorem', 'ipsum', 'dolor', 'sit', 'amet']
    normal_message = choice(messages)

    with caplog.at_level(logging.DEBUG):
        assert utils.stdout_handler(normal_message) is None

        for level, message in zip(levels, messages):
            assert utils.stdout_handler(f'{level}: {message}') is None

    assert caplog.records[0].levelname == 'INFO'
    assert caplog.records[0].message == normal_message

    for i, (level, message) in enumerate(zip(levels, messages)):
        log = caplog.records[i + 1]

        assert log.levelname[0].upper() == level[0].upper() if level[0] in 'IWED' else 'I'
        assert log.message == message


def test_spawn_subprocess():
    sub_process = utils.spawn_subprocess(['echo', 'Test message'])

    assert sub_process.args == ['echo', 'Test message']
    assert isinstance(sub_process, CompletedProcess)
    assert sub_process.returncode == 0

    with pytest.raises(CalledProcessError):
        utils.spawn_subprocess(['false'])


def test_find_file(tmp_path: Path):
    file = tmp_path / 'file.txt'
    file.touch()

    assert utils.find_file(file, [tmp_path]) == file
    assert utils.find_file(file, [tmp_path / 'sub_dir']) is None
    assert utils.find_file(file, [tmp_path / 'sub_dir', tmp_path]) == file
    assert utils.find_file(file, [tmp_path / 'sub_dir', tmp_path / 'sub_dir']) is None
    assert utils.find_file(file, [tmp_path / 'sub_dir', tmp_path / 'sub_dir', tmp_path]) == file

    file.unlink()


def test_unpack_xz(mocker):
    src = MagicMock(spec=Path)
    dest = MagicMock(spec=Path)
    src.name = "archive.xz"
    src.open.return_value = mocker.mock_open(read_data=b"compressed data").return_value
    dest.exists.return_value = False
    dest.open.return_value = mocker.mock_open().return_value

    # successful extraction
    mock_lzma_open = mocker.patch("lzma.open", return_value=mocker.mock_open(read_data=b"decompressed data").return_value)

    utils.unpack_xz(src, dest)

    mock_lzma_open.assert_called_once_with(src, "rb")
    dest.open.assert_called_once_with(mode="wb")
    dest.open.return_value.write.assert_called_once_with(b"decompressed data")

    # behavior when destination exists as a file
    dest.exists.return_value = True
    dest.is_file.return_value = True
    mock_unlink = mocker.patch.object(dest, "unlink")

    utils.unpack_xz(src, dest)
    mock_unlink.assert_called_once()

    # behavior when destination exists as a directory
    dest.is_file.return_value = False
    mock_rmtree = mocker.patch("shutil.rmtree")

    utils.unpack_xz(src, dest)
    mock_rmtree.assert_called_once_with(dest)