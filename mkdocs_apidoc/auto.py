from jinja2 import Template

from mkdocs_apidoc.collect import obj_from_string
from mkdocs_apidoc.docstring import doc_from_obj


def register_template_function(t: Template, f):
    t.globals[f.__name__] = f


def auto_object(s: str) -> str:
    obj = obj_from_string(s)
    return doc_from_obj(obj)


def render_page(page: str) -> str:
    """render the page"""
    t = Template(page)
    register_template_function(t, auto_object)
    return t.render()
