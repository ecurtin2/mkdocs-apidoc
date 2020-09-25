# mkdocs-apidoc

---

A plugin for mkdocs to automatically generate api documentation
for a python library. 

## Contents

[Installation](#installation)

[Usage](#usage)

[Customization](#customization)

[Template Configuration](#template-configuration)

- [signature-template](#signature_template)
- [function-template](#function_template)
- [method-template](#method_template)
- [class-template](#class_template)
- [module-template](#module_template)

## Installation

`pip install mkdocs-apidoc`


## Usage

`mkdocs-apidoc` exposes a set of [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates
for use in your `mkdocs` project. The most basic usage is to include a markdown file for 
each module you want to document

In `docs/my_module.md`
```markdown
{{ auto_module("my-package.my-module") }}
```

And in your `mkdocs.yaml`
```yaml
site_name: MkLorum
nav:
    - Home: index.md
    - Auto: my_module.md

plugins:
  - mkdocs_apidoc
```

And that's it! The module docstring and docstrings for classes, methods
and functions are automatically rendered in your site documentation. We've
provided some default formatting for how the various components get rendered to markdown, 
but these can be customized using a jinja2 template in the config. 
