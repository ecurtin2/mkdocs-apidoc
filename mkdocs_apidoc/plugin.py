from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin

from mkdocs_apidoc.auto import render_page


class ApiDocPlugin(BasePlugin):
    config_scheme = (
        ("foo", Type(str, default="a default value")),
        ("bar", Type(int, default=0)),
        ("baz", Type(bool, default=True)),
    )

    def on_page_markdown(self, markdown: str, config, **kwargs):
        return render_page(markdown)
