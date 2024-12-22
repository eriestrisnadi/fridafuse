from pathlib import Path

# default values
GH_BASE_URL = 'https://github.com'
LATEST_VERSION = 'latest'
CACHE_DIR = Path.cwd() / '.cache'

# colors
RED: str = '\033[0;91m'
GREEN: str = '\033[0;92m'
GRAY: str = '\033[0;90m'
STOP: str = '\033[0m'
