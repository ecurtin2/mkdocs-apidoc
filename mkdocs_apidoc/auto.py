"""
Module for automate the generation of markdown docs. Documenting
individual functions, objects, and classes is supported, as well
as modules.

"""
import sys
from importlib import import_module
from pathlib import Path
from typing import Callable

from jinja2 import Template

from mkdocs_apidoc.models import DataClass, Module

__all__ = [
    "auto_dataclass",
    "auto_object",
    "auto_module",
    "markdown",
    "register_template_function",
    "render_page",
    "obj_from_string",
    "set_root",
    "plustwo",
]


SOURCE_ROOT = Path()


def set_root(path: Path):
    """Set the root directory for imported modules

    The path will be added to the pythonpath so that modules
    can be imported. This is mostly used for testing.
    """
    global SOURCE_ROOT
    if not path.is_dir():
        raise ValueError(f"Project root must be directory, got {path}")

    SOURCE_ROOT = path
    sys.path.append(str(SOURCE_ROOT.absolute()))


def obj_from_string(s: str) -> object:
    """Given a string for an object, return the actual object

    ```
    f = obj_from_string('mymodule.myfunc')
    ```
    """
    mod_name, *rest = s.split(".")
    mod = import_module(mod_name)
    current = mod
    for attr in rest:
        current = getattr(current, attr)
    return current


def register_template_function(t: Template, f: Callable):
    """Register the function to be used in the jinja template.

    - t: A jinja Template to register the function to
    - f: A callable which wil be registered for use in the template.
        The name of the template-function will be the `__name__` attribute.


    ### Examples

    ```python
    from jinja2 import Template
    from mkdocs_apidoc.auto import markdown, register_template_function

    t = Template("here is some {{text}}")
    register_template_function(t, markdown)
    ```


    """
    t.globals[f.__name__] = f


def auto_object(s: str) -> str:
    """Automatically create a string from an object's name

    This will take the fully qualified name of the object from the
    project root, and instantiate it, then convert the object
    to it's documented format.

    - s: The name of an object, fully qualified.


    Automatically create a string from an object's name

    This will take the fully qualified name of the object from the project
    """
    obj = obj_from_string(s)
    if isinstance(obj, str):
        return obj
    return obj.__doc__


def auto_module(s: str) -> str:
    """Automatically document a module

    Template usage:
    ```
    ## my_mkdocs_file.md
    {{ auto_module("mkdocs_apidoc.auto") }}
    ```

    """
    obj = obj_from_string(s)
    return Module.from_module(obj).__repr_markdown__()


def markdown(s: str) -> str:
    """Get the markdown representation of the object represented by the string.

    #### Parameters
    s
    : The name of an object, which may be namespaced, i.e `"itertools.islice"`

    #### Returns
    :    The loaded objects's `__repr_markdown__`

    #### Template usage
    ```
    # my_mkdocs_file.md
    {{ markdown("mypackage.mymodule.my_object") }}
    ```

    """
    obj = obj_from_string(s)
    try:
        return obj.__repr_markdown__()
    except AttributeError:
        raise AttributeError(
            f"Could not get markdown for {s}: Needs to implement __repr_markdown__"
        )


def auto_dataclass(dataclass: str) -> str:
    """Generate the markdown for a dataclass, showing the fields."""
    cls = obj_from_string(dataclass)
    return DataClass.from_class(cls).__repr_markdown__()


def render_page(page: str) -> str:
    """render the page

    **page**
    :   The page to be rendered


    **returns**
    :   The rendered page

    """
    t = Template(page)
    register_template_function(t, auto_object)
    register_template_function(t, auto_module)
    register_template_function(t, markdown)
    register_template_function(t, auto_dataclass)
    return t.render()


def plustwo(x: int) -> int:
    """Add two to x

    #### Parameters
    x
    : a thing

    #### Returns
    :    x plus 2

    #### Examples

    You can run it on positive numbers

    ```python
    from mkdocs_apidoc.auto import plustwo
    print(plustwo(5))
    ```

    It works on negative numbers, too!

    ```python
    from mkdocs_apidoc.auto import plustwo
    print(plustwo(-10))
    ```

    """
    return x + 2
