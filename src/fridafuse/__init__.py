# ┌─┐┬─┐┬┌┬┐┌─┐┌─┐┬ ┬┌─┐┌─┐
# ├┤ ├┬┘│ ││├─┤├┤ │ │└─┐├┤
# └  ┴└─┴─┴┘┴ ┴└  └─┘└─┘└─┘

import logging
import sys

from fridafuse.__about__ import __title__, __version__

# helper containing a python 3 related warning
# if this is run with python 2
if sys.version_info < (3,):
    error_msg = f"""
You are running {__title__} {__version__} on Python 2
Unfortunately {__title__} {__version__} and above are not compatible with Python 2.
That's a bummer; sorry about that.  Make sure you have Python 3, pip and
setuptools to avoid these kinds of issues in the future:

    $ pip install pip setuptools --upgrade

You could also setup a virtual Python 3 environment.

    $ pip install pip setuptools --upgrade
    $ pip install virtualenv
    $ virtualenv --python=python3 ~/virt-python3
    $ source ~/virt-python3/bin/activate

This will make an isolated Python 3 installation available and active, ready
to install and use {__title__}.
"""
    raise ImportError(error_msg)

logging.basicConfig(
    level=logging.INFO, format='%(levelname)s: %(message)s', handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)
