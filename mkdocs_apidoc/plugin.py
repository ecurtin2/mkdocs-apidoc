from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin
from mkdocs_apidoc.auto import render_page


from mkdocs_apidoc import config


class ApiDocPlugin(BasePlugin):
    config_scheme = (
        ("function_template", Type(str, default=config.function_template)),
        ("bar", Type(int, default=0)),
        ("baz", Type(bool, default=True)),
    )

    def on_config(self, conf):
        config.function_template = self.config["function_template"]

        return conf

    def on_page_markdown(self, markdown: str, config, **kwargs):

        return render_page(markdown)
