import tabulate
from mkdocs.config.base import Config
from mkdocs.config.config_options import Type
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation

from mkdocs_apidoc import config
from mkdocs_apidoc.render import render_page


class ApiDocPlugin(BasePlugin):
    config_scheme = (
        ("function_template", Type(str, default=config.function_template)),
        ("method_template", Type(str, default=config.method_template)),
        ("signature_template", Type(str, default=config.signature_template)),
        ("module_template", Type(str, default=config.module_template)),
        ("class_template", Type(str, default=config.class_template)),
        ("log_level", Type(str, default=config.log_level)),
        (
            "execute_and_insert_examples",
            Type(bool, default=config.execute_and_insert_examples),
        ),
    )

    def on_config(self, conf: Config) -> Config:
        config.function_template = self.config["function_template"]
        config.method_template = self.config["method_template"]
        config.signature_template = self.config["signature_template"]
        config.module_template = self.config["module_template"]
        config.class_template = self.config["class_template"]
        config.logger.setLevel(self.config["log_level"])
        config.execute_and_insert_examples = self.config["execute_and_insert_examples"]
        return conf

    def on_page_markdown(self, markdown: str, config: Config, **kwargs) -> str:
        return render_page(markdown)

    def on_nav(self, nav: Navigation, config: Config, files: Files) -> Navigation:
        # TODO: I think adding links/references has to happen here
        return nav


_schema_markdown = tabulate.tabulate(
    [[name, t._type.__name__] for name, t in ApiDocPlugin.config_scheme],
    headers=["Name", "type"],
    tablefmt="github",
)
