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


def test_main(caplog):
    caplog.set_level(logging.INFO)
    main.main([])

    assert caplog.records[0].message == 'Starting...'
    assert caplog.records[-1].message == 'Done.'
