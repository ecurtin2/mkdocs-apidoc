from mkdocs_apidoc.parse_numpy import from_numpy


def doc_from_obj(x: object) -> str:
    """Return the markdown formatted docstring from the object"""

    s = from_numpy(x)

    try:
        header = f"## {x.__name__}\n"
    except AttributeError:
        header = ""
    return header + "\n\n" + str(s) + "\n\n"
