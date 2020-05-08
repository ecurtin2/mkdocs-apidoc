from inspect import Signature, getattr_static, getdoc, getmembers, isfunction, signature
from typing import Any, Callable, Dict, List

try:
    import attr

    ENABLE_ATTRS = True
except ImportError:
    ENABLE_ATTRS = False


def markdown_table(d: Dict[str, List[Any]], width: int = 10, none: str = "-") -> str:
    print(d)

    def cstr(x):
        if x is not None:
            return str(x).center(width)
        else:
            return none.center(width)

    header = "|" + "|".join(map(cstr, d)) + "|"
    br = "|" + "|".join("-" * width for _ in d) + "|"
    rows = ["|" + "|".join(map(cstr, row)) + "|" for row in zip(*d.values())]
    return "\n".join([header, br] + rows)


def formatted_signature(f: Callable, fname: str = None) -> str:
    if isfunction(f):
        sig = signature(f)
    elif isinstance(f, type):
        sig = signature(f.__init__)

    else:
        raise TypeError(f"Cant get sig for {f}")

    params = [str(v) for v in sig.parameters.values()]
    # get rid of self if class
    if isinstance(f, type):
        params = params[1:]
        ret = ")"
    else:
        if sig.return_annotation is Signature.empty:
            ret = ")"
        elif hasattr(sig.return_annotation, "__name__"):
            ret = f") -> {sig.return_annotation.__name__}"
        else:
            ret = f") -> {sig.return_annotation}"
    param_s = ", ".join(params) + ret
    if len(param_s) > 60:
        param_s = "\n    " + ",\n    ".join(params) + "\n" + ret

    if fname is None:
        fname = f.__name__
    sig = f"def {fname}({param_s}"

    return "```\n" + sig + "\n```\n"


def attrs_docs_from_module(m) -> str:
    attrs_class_dict = {
        k: v for k, v in m.__dict__.items() if attr.has(v) and isinstance(v, type)
    }
    if hasattr(m, "__all__"):
        attrs_classes = [v for k, v in attrs_class_dict.items() if k in m.__all__]
    else:
        attrs_classes = list(attrs_class_dict.values())

    docs = [getdoc(cls) for cls in attrs_classes]
    sigs = [formatted_signature(cls) for cls in attrs_classes]
    headers = [f"###{cls.__name__}\n\n" for cls in attrs_classes]
    member_docs = [get_member_docs(cls) for cls in attrs_classes]
    doc_sigs = [h + s + d + m for h, d, s, m in zip(headers, docs, sigs, member_docs)]
    if doc_sigs:
        return "\n\n --- \n\n".join(doc_sigs) + "\n\n"
    else:
        return ""


def get_method_sigs(methods, cls) -> List[str]:
    sigs = []
    for x in sorted(methods, key=lambda x: x[0]):
        name = x[0]
        doc = getdoc(x[1])
        try:
            try:
                c = cls.__name__
            except AttributeError:
                c = cls
            sig = formatted_signature(x[1], fname=f"{c}.{name}")
        except TypeError:
            sig = ""
        escaped_name = name.replace("_", r"\_")
        sigs.append(f"#####{escaped_name}\n{sig}\n\n{doc or ''}")
    return sigs


def get_member_docs(cls) -> str:
    methods = getmembers(cls)
    staticmethods = []
    classmethods = []
    normal_methods = []
    properties = []
    dunder_methods = []
    abstractprops = []
    for name, m in methods:
        # Skip single underscore methods
        if name.startswith("_") and not name.startswith("__"):
            continue
        if name.startswith("__") and not hasattr(m, "include_in_docs"):
            continue
        if hasattr(m, "include_in_docs") and not m.include_in_docs:
            continue

        meth = getattr_static(cls, name)
        if name.startswith("__"):
            dunder_methods.append((name, m))
        elif isinstance(meth, staticmethod):
            staticmethods.append((name, m))
        elif isinstance(meth, property):
            properties.append((name, m))
        elif isinstance(meth, classmethod):
            classmethods.append((name, m))
        # AbstractProperties
        elif isinstance(meth, (bool, float, int, str)):
            abstractprops.append((name, m))
        else:
            normal_methods.append((name, m))

    if normal_methods:
        method_str = "\n\n####Methods\n\n" + "\n".join(
            get_method_sigs(normal_methods, cls)
        )
    else:
        method_str = ""

    if properties:
        prop_str = "\n\n####Properties\n\n" + "\n".join(
            get_method_sigs(properties, cls)
        )
    else:
        prop_str = ""

    if abstractprops:
        if properties:
            prefix = "\n\n"
        else:
            prefix = "\n\n####Properties\n\n"
        aprop_str = prefix + "\n".join(f"#####{n} = {v}" for n, v in abstractprops)
    else:
        aprop_str = ""

    if staticmethods:
        static_str = "\n\n####Static Methods\n\n" + "\n".join(
            get_method_sigs(staticmethods, cls)
        )
    else:
        static_str = ""

    if dunder_methods:
        dunder_str = "\n\n####Dunder Methods\n\n" + "\n".join(
            get_method_sigs(dunder_methods, cls)
        )
    else:
        dunder_str = ""

    return (
        method_str
        + "\n\n"
        + prop_str
        + "\n\n"
        + aprop_str
        + "\n\n"
        + static_str
        + "\n\n"
        + dunder_str
    )


def func_docs_from_module(m) -> str:

    funcs = [v for k, v in m.__dict__.items() if isfunction(v)]
    if hasattr(m, "__all__"):
        funcs = [f for f in funcs if f in m.__all__]
    sigs = [formatted_signature(f) for f in funcs]
    docstrings = [getdoc(f) for f in funcs]
    return "\n\n".join(
        f"###{f.__name__}\n\n{s}\n\n{d}" for f, d, s in zip(funcs, docstrings, sigs)
    )


def autodoc_module(m) -> str:
    module_docstring = getdoc(m)
    if module_docstring is None:
        module_docstring = ""
    else:
        module_docstring += "\n\n"

    components = [f"# {m.__name__.split('.')[-1]}", module_docstring]

    if ENABLE_ATTRS:
        cdocs = attrs_docs_from_module(m)
        if cdocs:
            components += ["## Classes", "---", cdocs]

    fdocs = func_docs_from_module(m)
    if fdocs:
        components += ["## Functions", "----", fdocs]

    return "\n\n".join(components)
