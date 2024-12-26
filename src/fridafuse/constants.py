from pathlib import Path

from fridafuse.__about__ import __title__

# default values
GH_BASE_URL = 'https://github.com'
LATEST_VERSION = 'latest'
CACHE_DIR = Path.cwd() / f'.{__title__}_cache'
MANIFEST_NAMESPACE = {'android': 'http://schemas.android.com/apk/res/android'}
ARCHITECTURES = ['arm', 'arm64', 'x86', 'x86_64']
ABIS = ['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64']
ANDROID_MANIFEST_NAME = 'AndroidManifest.xml'
LIB_DIR_NAME = 'lib'
DEST_GADGET_NAME = 'libgadget.so'
APKTOOL_CONFIG_NAME = 'apktool.yml'

# colors
RED: str = '\033[0;91m'
GREEN: str = '\033[0;92m'
GRAY: str = '\033[0;90m'
STOP: str = '\033[0m'
