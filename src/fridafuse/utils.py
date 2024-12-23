from __future__ import annotations

from subprocess import PIPE, STDOUT, CalledProcessError, CompletedProcess, Popen
from typing import TYPE_CHECKING, Callable

from fridafuse import logger

if TYPE_CHECKING:
    from pathlib import Path


def stdout_handler(line: str):
    level, message = tuple(line.split(':', 1)) if ':' in line else ('I', line)
    log_map = {
        'I': logger.info,
        'INFO': logger.info,
        'W': logger.warning,
        'WARN': logger.warning,
        'WARNING': logger.warning,
        'E': logger.error,
        'ERR': logger.error,
        'ERROR': logger.error,
        'D': logger.debug,
        'DEBUG': logger.debug,
    }
    log = log_map.get(level.upper(), logger.info)

    return log(message.lstrip())


def spawn_subprocess(args, *, check: bool = True, stdout_handler: Callable[[str], None] = stdout_handler, **kwargs):
    with Popen(args, stdout=PIPE, stderr=STDOUT, text=True, **kwargs) as process:
        for line in process.stdout:
            stdout_handler(line.strip())

    retcode = process.poll()

    if check and retcode:
        raise CalledProcessError(retcode, process.args)

    return CompletedProcess(process.args, retcode)


def find_file(file: Path, dirs: list[Path]):
    for sub_dir in dirs:
        for f in sub_dir.rglob(file.name):
            if f.is_file():
                return f

    return None
