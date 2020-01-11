# Created: 26.12.2019
# Copyright (c) 2019-2020, Manfred Moitzi
# License: MIT License
import sys
from .version import version, __version__

VERSION = __version__
__author__ = "mozman <me@mozman.at>"

PYPY = hasattr(sys, 'pypy_version_info')
PYPY_ON_WINDOWS = sys.platform.startswith('win') and PYPY
