from pathlib import Path

from mkdocs_apidoc import __version__
from mkdocs_apidoc.auto import auto_object, render_page
from mkdocs_apidoc.collect import set_root

set_root(Path(__file__).parent)


def test_auto_object():
    s = auto_object("example_module.example_function")
    print(s)


def test_render_page():
    page = Path(__file__).with_name("example_doc.md").read_text()
    rendered = render_page(page)
    print(rendered)
