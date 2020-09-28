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

#### {{ name }}

```python
{% if type == "STATIC" %}@staticmethod{% endif %}{% if type == "CLASS" %}@classmethod{% endif %}{% if type == "PROPERTY" %}@property{% endif %}{% if type == "ABSTRACTPROPERTY" %}@staticmethod
@property{% endif %}
def {{name}}{{ signature }}:
```

{{ docstring }}


"""

class_template = """
### {{ name }}

{{ docstring }}

{% if class_fields %}
#### Fields 
| Name | Type |
|------|------|
{% for field in class_fields %}| {{ field.name }} | {{ field.type }} |
{% endfor %}
{% endif %}

{% for m in methods %}
{{ m }}
{% endfor %}

"""


module_template = """

# {{ name }}

{{ docstring }}

{% if enums %}
## Enums
------------
{% for enum in enums %}
{{ enum }}
---------------------------
{% endfor %}
{% endif %}

{% if classes %}
## Classes
-----------

{% for c in classes %}
{{ c }}
---------------------------
{% endfor %}
{% endif %}

{% if functions %}
## Functions
-------------

{% for f in functions %}
{{ f }}
---------------------------
{% endfor %}
{% endif %}

"""

enum_template = """

### {{ name }}

{{ docstring }}

| {{name}} |
|-------|
{% for level in levels %}| {{ level }} |
{% endfor %}

"""
