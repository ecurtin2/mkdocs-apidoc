signature_template = """
({% for p in params %}{{p}}, {% endfor %}) -> {{ returnval }}
"""

function_template = """

### {{ name }}

{{ signature }}

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
