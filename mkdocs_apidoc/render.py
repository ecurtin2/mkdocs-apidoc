"""
Module for automate the generation of markdown docs. Documenting
individual functions, objects, and classes is supported, as well
as modules.

"""
from typing import Any, Callable, Dict, Tuple, TypeVar
from operator import attrgetter

from jinja2 import Template

from mkdocs_apidoc.config import logger
from mkdocs_apidoc.models import Module

__all__ = ["render_page", "make_converter", "markdown"]

from mkdocs_apidoc.parser import obj_from_string


def identity(s):
    return s


def markdown(obj):
    """Return object's `__repr_markdown__`

    This is useful as a function that can be passed around to
    get the markdown representation of various objects.

    #### Parameters
    obj
    :   An object implementing `__repr_markdown__`


    #### Returns
    :   The result of calling `__repr_markdown__`

    #### Examples

    ```python
    from mkdocs_apidoc.render import markdown

    class A:
        def __repr_markdown__(self):
            return "# I am the **markdown** representation of A!"

    print(markdown(A()))
    ```

    """
    return obj.__repr_markdown__()


registry: Dict[str, Tuple[Callable, Callable]] = {
    "auto_module": (Module.from_module, Module.__repr_markdown__),
    "auto_object": (attrgetter("__doc__"), identity),
    "raw_object": (identity, identity),
    "markdown": (identity, markdown),
    "typeof": (type, attrgetter("__name__")),
}

T = TypeVar("T")


def make_converter(
    structure: Callable[[Any], T], unstructure: Callable[[T], str]
) -> Callable[[str], str]:
    """Create a conversion function

    The resulting function will take a string, the name of an object
    and structure it. Structured object will then be unstructured.

    The Return type of structure must match the input type of unstructure.

    #### Parameters
    structure
    :   A function which takes a python object, and structures it
        to a known type.

    unstructure
    :   A function which converts an object to a markdown representation.


    #### Returns
    :   A conversion function

    #### Example
    ```python
    from mkdocs_apidoc.render import make_converter

    def parse_docstring(s: str) -> str:
        return s.__doc__

    def charcount(s: str) -> str:
        return f"Docstring is {len(s)} lines long, here it is ---> {s}"

    converter = make_converter(parse_docstring, charcount)
    print(converter("itertools.count"))
    ```

    """

    def f(x):
        logger.debug(
            f"Doing: {x} with structure={structure} and unstructure={unstructure}"
        )
        obj = obj_from_string(x)
        return unstructure(structure(obj))

    return f


def render_page(page: str) -> str:
    """render the page

    #### Parameters
    page
    :   The page to be rendered


    #### Returns
    :   The rendered page

    #### Example
    ```python
    from mkdocs_apidoc.render import render_page

    page = '''
    # Hi i'm an example markdown file
    {{ auto_object('collections.deque') }}

    ## you can keep doing stuff here too

    Did you know the type of `collections.namedtuple` is {{ typeof('collections.namedtuple') }} ???
    '''
    print(render_page(page))
    ```

    """
    t = Template(page)
    for name, funcs in registry.items():
        t.globals[name] = make_converter(*funcs)
    return t.render()
