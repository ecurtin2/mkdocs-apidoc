from jinja2 import Template

from mkdocs_apidoc.collect import obj_from_string
from mkdocs_apidoc.docstring import doc_from_obj
from mkdocs_apidoc.models import Module


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
    return Module.from_module(obj).__repr_markdown__()


def markdown(s: str) -> str:
    obj = obj_from_string(s)
    try:
        return obj.__repr_markdown__()
    except AttributeError:
        raise AttributeError(
            f"Could not get markdown for {s}: Needs to implement __repr_markdown__"
        )


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
    register_template_function(t, markdown)
    return t.render()
