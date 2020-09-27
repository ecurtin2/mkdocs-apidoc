from importlib import metadata

try:
    __version__ = metadata.version(__name__)
except:
    __version__ = "unknown"

from . import example_module
