# mkdocs-apidoc

A plugin for mkdocs to automatically generate api documentation
for a python library. 

## Example website

The project documentation is made using itself!

https://ecurtin2.github.io/mkdocs-apidoc/

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
    - Home: README.md
    - Auto: my_module.md

plugins:
  - mkdocs_apidoc
```

And that's it! The module docstring and docstrings for classes, methods
and functions are automatically rendered in your site documentation. We've
provided some default formatting for how the various components get rendered to markdown, 
but these can be customized using a jinja2 template in the config. 


## Installation

`pip install mkdocs-apidoc`
