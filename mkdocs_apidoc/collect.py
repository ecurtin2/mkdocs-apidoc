import sys
from importlib import import_module
from pathlib import Path

SOURCE_ROOT = Path()


def set_root(path: Path):
    """Set the root directory for imported modules

    The path will be added to the pythonpath so that modules
    can be imported
    """
    global SOURCE_ROOT
    if not path.is_dir():
        raise ValueError(f"Project root must be directory, got {path}")

    SOURCE_ROOT = path
    sys.path.append(str(SOURCE_ROOT.absolute()))


def obj_from_string(s: str) -> object:
    """Given a string for an object, return the actual object

    f = obj_from_string('mymodule.myfunc')

    """
    mod_name, *rest = s.split(".")
    mod = import_module(mod_name)
    current = mod
    for attr in rest:
        current = getattr(current, attr)
    return current
