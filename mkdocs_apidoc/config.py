import logging
from os import getenv


__all__ = [
    "logger",
    "signature_template",
    "execute_and_insert_examples",
    "function_template",
    "method_template",
    "class_template",
    "module_template",
    "dataclass_template",
]

logging.basicConfig(
    level=logging.INFO,
    format="[%(name)s] %(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
)
log_level = getenv("MKDOCS_APIDOC_LOG_LEVEL", "INFO")

logger = logging.getLogger("mkdocs-apidoc")
logger.setLevel(log_level)

logger.debug("Set log level")


signature_template = (
    """({{params|join(', ')}}){% if returnval %} -> {{ returnval }}{% endif %}"""
)

execute_and_insert_examples = False

function_template = """

### {{ name }}

```python
def {{name}}{{ signature }}:
```

{{ docstring }}


"""

method_template = """

##### {{ name }}

{{ signature }}

{{ docstring }}


"""

class_template = """
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
"""


module_template = """

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

"""

dataclass_template = """

#### {{name}}

{% for f in fields %}
- {{f.name}}: {{f.type}}
{% endfor %}
"""
