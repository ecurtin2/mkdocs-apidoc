
Templates can be customized my modifying the config

{% raw %}
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
{% endraw %}

All functions will then be rendered via this jinja2 template instead of the provided 
default. The available arguments can be seen in `models`


## Default configuration

#### Options

{{ raw_object("mkdocs_apidoc.plugin._schema_markdown")}}



#### function_template
````
{{raw_object("mkdocs_apidoc.config.function_template")}}
````

#### signature_template
````
{{raw_object("mkdocs_apidoc.config.signature_template")}}
````

#### method_template
````
{{raw_object("mkdocs_apidoc.config.method_template")}}
````

#### class_template
````
{{raw_object("mkdocs_apidoc.config.class_template")}}
````

#### module_template
````
{{raw_object("mkdocs_apidoc.config.module_template")}}
````

