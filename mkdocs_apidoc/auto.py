from jinja2 import Template

from mkdocs_apidoc.collect import obj_from_string
from mkdocs_apidoc.docstring import doc_from_obj
from mkdocs_apidoc.inspections import autodoc_module


def register_template_function(t: Template, f):
    t.globals[f.__name__] = f


def auto_object(s: str) -> str:
    """Automatically create a string from an object's name

    This will take the fully qualified name of the object from the
    project root, and instantiate it.

    Parameters
    -----------
    s
        The name of an object.
        This is second line
    """
    obj = obj_from_string(s)
    return doc_from_obj(obj)


def auto_module(s: str) -> str:
    """Automatically document a module"""
    obj = obj_from_string(s)
    return autodoc_module(obj)


def render_page(page: str) -> str:
    """render the page

    Parameters
    -----------
    page
        The page to render

    """
    t = Template(page)
    register_template_function(t, auto_object)
    register_template_function(t, auto_module)
    return t.render()
