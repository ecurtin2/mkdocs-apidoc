# Mkdocs-Apidoc

### Version: {{ raw_object("mkdocs_apidoc.__version__") }}

## Installation

`pip install mkdocs-apidoc`

## Usage

`mkdocs-apidoc` exposes a set of [jinja2](https://jinja.palletsprojects.com/en/2.11.x/) templates
for use in your `mkdocs` project. The most basic usage is to include a markdown file for 
each module you want to document

In `docs/my_module.md`
{% raw %}
```
# Some markdown text can do here

{{ auto_module("my-package.my-module") }}

## and more markdown can follow, but neither are needed
```
{% endraw %}

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

## auto_object

{% raw %}
`{{ auto_object("package.module.object") }}`
{% endraw %}

Automatically render a class or function object using the normal logic. 

## auto_module

{% raw %}
`{{ auto_module("package.module") }}`
{% endraw %}

Insert the parsed documentation for a module, including it's name, docstring, 
functions and classes. 

## markdown

{% raw %}
`{{ markdown("package.module.object") }}`
{% endraw %}

This will call the object's `__repr_markdown__` and embed
the result. Can be used to do anything you want to, really. 