from importlib import metadata

from . import render
from . import config
from . import models
from . import parser
from . import plugin

try:
    __version__ = metadata.version(__name__)
except:
    __version__ = "unknown"
