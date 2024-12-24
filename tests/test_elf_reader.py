from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from fridafuse.elf_reader import ELF, get_needed


@pytest.fixture
def mock_lief():
    with patch('fridafuse.elf_reader.lief') as lief:
        yield lief


def test_get_needed_no_dynamic_entries(mock_lief):
    mock_lief.parse.return_value.dynamic_entries = []
    src = Path('/fake/path')

    result = get_needed(src)

    assert result == []
    mock_lief.parse.assert_called_once_with(src)


def test_get_needed_with_entries(mock_lief):
    mock_entry_1 = MagicMock(tag=ELF.DynamicEntry.TAG.NEEDED, value='libc.so.6')
    mock_entry_1.name = 'libc.so.6'
    mock_entry_2 = MagicMock(tag=ELF.DynamicEntry.TAG.SONAME, value='libtest.so')
    mock_entry_2.name = 'libtest.so'
    mock_entry_3 = MagicMock(tag=ELF.DynamicEntry.TAG.NULL, value='', name='')

    mock_lief.parse.return_value.dynamic_entries = [mock_entry_1, mock_entry_2, mock_entry_3]
    src = Path('/fake/path')

    result = get_needed(src)

    expected = [
        ('NEEDED', 'libc.so.6', 'libc.so.6'),
        ('SONAME', 'libtest.so', 'libtest.so'),
    ]
    assert result == expected
    mock_lief.parse.assert_called_once_with(src)


def test_get_needed_verbose(mock_lief, caplog):
    mock_entry = MagicMock(tag=ELF.DynamicEntry.TAG.NEEDED, value='libc.so.6', name='libc.so.6')
    mock_entry.name = 'libc.so.6'
    mock_lief.parse.return_value.dynamic_entries = [mock_entry]
    src = Path('/fake/path')

    with caplog.at_level('INFO'):
        result = get_needed(src, verbose=True)

    assert result == [('NEEDED', 'libc.so.6', 'libc.so.6')]
    assert '== Dynamic entries ==' in caplog.text
    assert 'Tag' in caplog.text
    assert 'Value' in caplog.text
    assert 'Info' in caplog.text
    assert 'NEEDED' in caplog.text
    mock_lief.parse.assert_called_once_with(src)
