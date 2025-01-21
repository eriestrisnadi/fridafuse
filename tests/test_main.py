import logging
import sys
from importlib import reload

import pytest
from click.testing import CliRunner

from fridafuse import cli, logger


def test_python_version_3(mocker):
    mocker.patch('sys.version_info', (3, 7))
    reload(sys.modules['fridafuse'])

    assert True


def test_python_version_2(mocker):
    mocker.patch('sys.version_info', (2, 7))
    with pytest.raises(ImportError) as excinfo:
        reload(sys.modules['fridafuse'])

    assert 'You are running' in str(excinfo.value)
    assert 'Unfortunately' in str(excinfo.value)
    assert 'not compatible with Python 2' in str(excinfo.value)


def test_logging_configuration(caplog):
    with caplog.at_level(logging.INFO):
        logger.info('Test log message')

    assert 'Test log message' in caplog.text


def test_main():
    result = CliRunner().invoke(cli.cli, color=True)

    assert cli.logo in result.output
    assert cli.__version__ in result.output
    assert f'Usage: {cli.__title__}' in result.output
    assert '-h' in result.output

    for method in ['smali', 'native-lib', 'auto']:
        assert method in result.output
