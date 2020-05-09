from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin
from mkdocs_apidoc.auto import render_page


from mkdocs_apidoc import config


class ApiDocPlugin(BasePlugin):
    config_scheme = (
        ("function_template", Type(str, default=config.function_template)),
        ("method_template", Type(int, default=config.method_template)),
        ("signature_template", Type(bool, default=config.signature_template)),
        ("module_template", Type(bool, default=config.module_template)),
        ("class_template", Type(bool, default=config.class_template)),
    )

    def on_config(self, conf):
        config.function_template = self.config["function_template"]
        config.method_template = self.config["method_template"]
        config.signature_template = self.config["signature_template"]
        config.module_template = self.config["module_template"]
        config.class_template = self.config["class_template"]
        return conf

    def on_page_markdown(self, markdown: str, config, **kwargs):

        return render_page(markdown)
