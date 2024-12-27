import logging
import sys
from importlib import reload

import pytest

from fridafuse import logger, main


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


def test_main(capsys):
    with pytest.raises(SystemExit):
        main.main([])

    captured = capsys.readouterr()

    assert main.cli.logo in captured.out
    assert main.cli.__version__ in captured.out
    assert f'{main.cli.__title__}: error:' in captured.err
    assert f'usage: {main.cli.__title__}' in captured.err
    assert '-h' in captured.err

    for method in ['smali','native-lib','auto']:
        assert method in captured.err
