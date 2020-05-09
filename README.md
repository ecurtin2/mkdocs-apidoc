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

## Customization

```yaml
site_name: MkLorum
nav:
    - Home: index.md
    - Auto: my_module.md

plugins:
  - mkdocs_apidoc:
      function_template: |
        ### {{ name }}

        {{ signature }}

        {{ docstring }}
```

All functions will then be rendered via this jinja2 template instead of the provided 
default. The available arguments can be seen in `models.py`

### Template Configuration

#### signature_template
```
({% for p in params %}{{p}}, {% endfor %}) -> {{ returnval }}
```

#### function_template
```

### {{ name }}

{{ signature }}

{{ docstring }}

```

#### method_template
```

##### {{ name }}

{{ signature }}

{{ docstring }}


```

#### class_template
```
### {{ name }}

{{ docstring }}

-----------------

{% if normal_methods %}
#### Methods

{% for m in normal_methods %}
{{m}}
{% endfor %}
{% endif %}

{% if staticmethods %}
#### Staticmethods

{% for m in staticmethods %}
{{m}}
{% endfor %}
{% endif %}

{% if classmethods %}
#### ClassMethods
{% for m in classmethods %}
{{m}}
{% endfor %}
{% endif %}

{% if dunder_methods %}
#### Dunder Methods

{% for m in dunder_methods %}
{{m}}
{% endfor %}
{% endif %}
```


#### module_template
```
# {{ name }}

{{ docstring }}

{% if classes %}
## Classes
-----------

{% for c in classes %}
{{ c }}
{% endfor %}
{% endif %}

{% if functions %}
## Functions
-------------

{% for f in functions %}
{{ f }}
{% endfor %}
{% endif %}
```


## Reference

### auto_object

```
{{ auto_object("package.module.object") }}
```
Automatically render a class or function object using the normal logic. 

### auto_module

```
{{ auto_module("package.module") }}
```
Insert the parsed documentation for a module, including it's name, docstring, 
functions and classes. 

### markdown

```
{{ markdown("package.module.object") }}
```

This will call the object's `__repr_markdown__` and embed
the result. Can be used to do anything you want to, really. 