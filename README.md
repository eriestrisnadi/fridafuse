# Fridafuse

[<img src="https://github.com/eriestrisnadi/fridafuse/blob/main/ext/logo.svg?raw=true" width="300"/>](https://github.com/eriestrisnadi/fridafuse)

Automatically patch APK with frida-gadget into Smali or Native Library.

[![Test & Coverage](https://github.com/eriestrisnadi/fridafuse/actions/workflows/test-and-coverage.yml/badge.svg)](https://github.com/eriestrisnadi/fridafuse/actions/workflows/test-and-coverage.yml)
[![PyPI - Version](https://img.shields.io/pypi/v/fridafuse.svg)](https://pypi.org/project/fridafuse)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fridafuse.svg)](https://pypi.org/project/fridafuse)

-----

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install fridafuse
```

## Usage
```
fridafuse [OPTIONS] INPUT COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...
```

The following are the main flags that can be used with fridafuse:

```
Options:
  -o, --output PATH
  --gadget-version TEXT  Specify frida gadget version
  --skip-sign            Skip to create signed APK
  --edit                 Edit the APK after patched
  --help                 Show this message and exit.

Commands:
  auto
  native-lib
  smali
```

*Check with help command for more information.*

## License

`Fridafuse` is distributed under the terms of the [GPL-3.0](https://github.com/eriestrisnadi/fridafuse/blob/main/LICENSE) license.
