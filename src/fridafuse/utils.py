from __future__ import annotations

from subprocess import PIPE, STDOUT, CalledProcessError, CompletedProcess, Popen
from typing import Callable

from fridafuse import logger


def stdout_handler(line: str):
    line_parts = line.split(':', 1)
    log_map = {'I': logger.info, 'Error': logger.error}
    log = log_map.get(line_parts[0], logger.info)
    message = (line if line_parts[0] not in log_map else line_parts[1]).lstrip()

    return log(message)


def spawn_subprocess(args, *, check: bool = True, stdout_handler: Callable[[str], None] = stdout_handler, **kwargs):
    with Popen(args, stdout=PIPE, stderr=STDOUT, text=True, **kwargs) as process:
        for line in process.stdout:
            stdout_handler(line.strip())

    retcode = process.poll()

    if check and retcode:
        raise CalledProcessError(retcode, process.args)

    return CompletedProcess(process.args, retcode)
