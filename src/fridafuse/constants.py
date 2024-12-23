from pathlib import Path

from fridafuse.__about__ import __title__

# default values
GH_BASE_URL = 'https://github.com'
LATEST_VERSION = 'latest'
CACHE_DIR = Path.cwd() / f'.{__title__}_cache'
MANIFEST_NAMESPACE = {'android': 'http://schemas.android.com/apk/res/android'}

# colors
RED: str = '\033[0;91m'
GREEN: str = '\033[0;92m'
GRAY: str = '\033[0;90m'
STOP: str = '\033[0m'
