from dataclasses import dataclass, field
import inspect
from jinja2 import Template
from typing import Callable, List, Optional
from mkdocs_apidoc import config

import logging

logger = logging.getLogger("mkdocs-apidoc")


@dataclass
class Signature:
    name: str
    params: list
    returnval: str

    @staticmethod
    def from_callable(f: Callable, fname: str = None) -> "Signature":
        logger.debug(f"Getting Signature from {f}")
        logger.debug(f"type: {type(f)}")

        if isinstance(f, type):
            sig = inspect.signature(f.__init__)
        else:
            sig = inspect.signature(f)

        params = [str(v) for v in sig.parameters.values()]
        # get rid of self if class
        if isinstance(f, type):
            params = params[1:]

        if sig.return_annotation is inspect.Signature.empty:
            ret = ""
        elif hasattr(sig.return_annotation, "__name__"):
            ret = sig.return_annotation.__name__
        else:
            ret = sig.return_annotation

        if fname is None:
            fname = f.__name__

        sig = Signature(name=fname, params=params, returnval=ret)
        logger.debug(f"Register signature: {sig}")
        return sig

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.signature_template)
        escaped_name = self.name.replace("_", r"\_")
        return tmpl.render(
            name=escaped_name, params=self.params, returnval=self.returnval
        )


@dataclass
class Function:
    name: str
    signature: Signature
    docstring: str

    @staticmethod
    def from_callable(func) -> "Function":
        doc = inspect.getdoc(func)
        f = Function(
            name=func.__name__, signature=Signature.from_callable(func), docstring=doc
        )
        logger.debug(f"Registered function {f}")
        return f

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.function_template)
        return tmpl.render(
            name=self.name,
            signature=self.signature.__repr_markdown__(),
            docstring=self.docstring,
        )


@dataclass
class Method:
    name: str
    signature: Signature
    docstring: str

    @staticmethod
    def from_callable(func, fname: Optional[str] = None) -> "Method":
        doc = inspect.getdoc(func)

        if fname is None:
            name = func.__name__
        else:
            name = fname
        return Method(name=name, signature=Signature.from_callable(func), docstring=doc)

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.method_template)
        return tmpl.render(
            name=self.name,
            signature=self.signature.__repr_markdown__(),
            docstring=self.docstring,
        )


@dataclass
class Class:
    name: str
    docstring: str
    methods: list = field(default_factory=list)
    staticmethods: list = field(default_factory=list)
    classmethods: list = field(default_factory=list)
    normal_methods: list = field(default_factory=list)
    properties: list = field(default_factory=list)
    dunder_methods: list = field(default_factory=list)
    abstractprops: list = field(default_factory=list)

    @staticmethod
    def from_class(cls):
        methods = inspect.getmembers(cls)
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

            meth = inspect.getattr_static(cls, name)
            if name.startswith("__"):
                dunder_methods.append(m)
            elif isinstance(meth, staticmethod):
                staticmethods.append(m)
            elif isinstance(meth, property):
                properties.append(m)
            elif isinstance(meth, classmethod):
                classmethods.append(m)
            # AbstractProperties
            elif isinstance(meth, (bool, float, int, str)):
                abstractprops.append(m)
            else:
                normal_methods.append(m)

        instance = Class(
            name=cls.__name__,
            docstring=inspect.getdoc(cls),
            # methods=[m[1] for m in methods],/
            dunder_methods=[
                Method.from_callable(m, fname=f"{m.__name__}".replace("_", r"\_"))
                for m in dunder_methods
            ],
            staticmethods=[Method.from_callable(m) for m in staticmethods],
            classmethods=[Method.from_callable(m) for m in classmethods],
            normal_methods=[Method.from_callable(m) for m in normal_methods],
            # properties=[Method.from_callable(m) for m in properties],
            # abstractprops=[Method.from_callable(m) for m in abstractprops],
        )

        logger.debug(f"Parsed {instance}")
        return instance

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.class_template)

        attrs = [
            "methods",
            "staticmethods",
            "classmethods",
            "normal_methods",
            # "properties",
            "dunder_methods",
            # "abstractprops",
        ]

        sigs = {}
        for a in attrs:
            methods = getattr(self, a)
            formatted_methods = [m.__repr_markdown__() for m in methods]
            sigs[a] = formatted_methods

        return tmpl.render(name=self.name, docstring=self.docstring, **sigs)


@dataclass
class Module:
    name: str
    docstring: str
    functions: List[Function]
    classes: List[Class]

    @staticmethod
    def from_module(m) -> "Module":
        module_docstring = inspect.getdoc(m)
        module_name = m.__name__.split(".")[-1]

        funcs = {name: f for name, f in m.__dict__.items() if inspect.isfunction(f)}
        if hasattr(m, "__all__"):
            funcs = [f for name, f in funcs.items() if name in m.__all__]

        class_dict = {k: v for k, v in m.__dict__.items() if isinstance(v, type)}
        if hasattr(m, "__all__"):
            classes = [v for k, v in class_dict.items() if k in m.__all__]
        else:
            classes = list(class_dict.values())

        return Module(
            name=module_name,
            docstring=module_docstring,
            functions=[Function.from_callable(f) for f in funcs],
            classes=[Class.from_class(c) for c in classes],
        )

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.module_template)
        return tmpl.render(
            name=self.name,
            docstring=self.docstring,
            classes=[c.__repr_markdown__() for c in self.classes],
            functions=[f.__repr_markdown__() for f in self.functions],
        )
