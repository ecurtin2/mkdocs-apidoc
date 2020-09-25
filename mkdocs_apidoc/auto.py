"""
Module for automate the generation of markdown docs. Documenting
individual functions, objects, and classes is supported, as well
as modules.

"""

from typing import Callable

from jinja2 import Template

from mkdocs_apidoc.collect import obj_from_string
from mkdocs_apidoc.docstring import doc_from_obj
from mkdocs_apidoc.models import Module, DataClass


__all__ = ["register_template_function", "auto_object", "auto_module", "markdown", "render_page"]


def register_template_function(t: Template, f: Callable):
    """Register the function to be used in the jinja template.

    - t: A jinja Template to register the function to
    - f: A callable which wil be registered for use in the template.
        The name of the template-function will be the `__name__` attribute.

    ```python
    from jinja2 import Template
    from mkdocs_apidoc.auto import auto_object, auto_module, markdown

    t = Template("here is some {{text}}")
    register_template_function(t, auto_object)
    register_template_function(t, auto_module)
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

    ```python
    >>> docs = auto_object("mkdocs_apidoc.auto.auto_object")
    >>> print(docs)

    ## auto_object


    Automatically create a string from an object's name

    This will take the fully qualified name of the object from the project
    ...
    ```
    """
    obj = obj_from_string(s)
    if isinstance(obj, str):
        return obj
    return doc_from_obj(obj)


def auto_module(s: str) -> str:
    """Automatically document a module

    Template usage:
    ```
    ## my_mkdocs_file.md
    {{ auto_module("mkdocs_apidoc.auto") }}
    ```

    Python usage:
    ```python
    >>> auto_module("mkdocs_apidoc.auto")
    ```

    """
    obj = obj_from_string(s)
    return Module.from_module(obj).__repr_markdown__()


def markdown(s: str) -> str:
    """Get the markdown representation of the object represented by the string.

    Template usage:
    ```
    ## my_mkdocs_file.md
    {{ markdown("mypackage.mymodule.my_object") }}
    ```

    Python usage:
    ```python
    >>> class A:
    >>>    def __repr_markdown__(self):
    >>>        return "# hi I'm markdown"
    >>>
    >>>my_object = A()
    >>> markdown("mymodule.my_object")
    "# hi I'm markdown"
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
    cls = obj_from_string(dataclass)
    return DataClass.from_class(cls).__repr_markdown__()


def render_page(page: str) -> str:
    """render the page

    - page: The page to render as a template.

    """
    t = Template(page)
    register_template_function(t, auto_object)
    register_template_function(t, auto_module)
    register_template_function(t, markdown)
    register_template_function(t, auto_dataclass)
    return t.render()
