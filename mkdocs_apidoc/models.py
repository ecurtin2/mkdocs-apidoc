import inspect
import logging
from dataclasses import dataclass, field, fields, is_dataclass
from enum import Enum, auto
from typing import Callable, List, Optional

from jinja2 import Template

from mkdocs_apidoc import config
from mkdocs_apidoc.parser import docstring_with_code_outputs

logger = logging.getLogger("mkdocs-apidoc")


__all__ = ["Signature", "Function", "Method", "Class", "Module"]


@dataclass
class Signature:
    """Signature information"""

    name: str
    params: List[str]
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
    """Holds information for functions, but not methods."""

    name: str
    signature: Signature
    docstring: str

    @staticmethod
    def from_callable(func) -> "Function":
        doc = inspect.getdoc(func)
        if hasattr(func, "__name__"):
            name = func.__name__
        else:
            name = str(func)
        f = Function(name=name, signature=Signature.from_callable(func), docstring=doc)
        logger.debug(f"Registered function {f}")
        return f

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.function_template)
        logger.debug(f"Rendering {self}")
        if config.execute_and_insert_examples:
            logger.debug(f"Executing code blocks in {self}")
            ds = docstring_with_code_outputs(self.docstring)
        else:
            ds = self.docstring
        return tmpl.render(
            name=self.name,
            signature=self.signature.__repr_markdown__(),
            docstring=ds,
        )


class MethodType(Enum):
    """Describes the nature of the method."""

    NORMAL = auto()
    STATIC = auto()
    CLASS = auto()
    PROPERTY = auto()
    DUNDER = auto()
    ABSTRACTPROPERTY = auto()


@dataclass
class Method:
    """Contains information about a method, including it's signature and properties."""

    name: str
    type: MethodType
    signature: Signature
    docstring: str

    @staticmethod
    def from_callable(
        func, method_type: MethodType, fname: Optional[str] = None
    ) -> "Method":
        doc = inspect.getdoc(func)

        if fname is None:
            name = func.__name__
        else:
            name = fname
        return Method(
            name=name,
            signature=Signature.from_callable(func),
            docstring=doc,
            type=method_type,
        )

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.method_template)
        return tmpl.render(
            name=self.name,
            signature=self.signature.__repr_markdown__(),
            type=self.type.name,
            docstring=self.docstring or "",
        )


class ClassType(Enum):
    """Enum for what kind of class it is. """

    NORMAL = auto()
    DATACLASS = auto()


@dataclass
class Field:
    """A field of a class"""

    name: str
    type: str


@dataclass
class Class:
    """Contains class information"""

    name: str
    docstring: str
    type: ClassType
    fields: List[Field] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)

    @staticmethod
    def from_class(cls):
        methods = inspect.getmembers(cls)

        parsed_methods = []
        for name, m in methods:
            # Skip single underscore methods
            if name.startswith("_") and not name.startswith("__"):
                continue
            if name.startswith("__"):
                continue
            if hasattr(m, "include_in_docs") and not m.include_in_docs:
                continue

            meth = inspect.getattr_static(cls, name)
            if name.startswith("__"):
                method_type = MethodType.DUNDER
            elif isinstance(meth, staticmethod):
                method_type = MethodType.STATIC
            elif isinstance(meth, property):
                method_type = MethodType.PROPERTY
            elif isinstance(meth, classmethod):
                method_type = MethodType.CLASS
            elif isinstance(meth, (bool, float, int, str)):
                method_type = MethodType.ABSTRACTPROPERTY
            else:
                method_type = MethodType.NORMAL

            parsed_methods.append(Method.from_callable(m, method_type=method_type))

        if is_dataclass(cls):
            cls_type = ClassType.DATACLASS
            class_fields = [
                Field(f.name, getattr(f.type, "__name__", f.type)) for f in fields(cls)
            ]
        else:
            cls_type = ClassType.NORMAL
            class_fields = []

        instance = Class(
            name=cls.__name__,
            docstring=inspect.getdoc(cls),
            methods=parsed_methods,
            fields=class_fields,
            type=cls_type,
        )
        logger.debug(f"Parsed {instance}")
        return instance

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.class_template)

        formatted_methods = [m.__repr_markdown__() for m in self.methods]
        return tmpl.render(
            name=self.name,
            docstring=self.docstring,
            methods=formatted_methods,
            class_fields=self.fields,
            type=self.type,
        )


@dataclass
class Enumeration:
    name: str
    levels: List[str]
    docstring: str

    def __repr_markdown__(self):
        tmpl = Template(config.enum_template)
        return tmpl.render(
            name=self.name, levels=self.levels, docstring=self.docstring or ""
        )


@dataclass
class Module:
    """Holds module contents"""

    name: str
    docstring: str
    functions: List[Function]
    classes: List[Class]
    enums: List[Enumeration]

    @staticmethod
    def from_module(m) -> "Module":
        module_docstring = inspect.getdoc(m)
        module_name = m.__name__.split(".")[-1]

        funcs = {name: f for name, f in m.__dict__.items() if inspect.isfunction(f)}
        if hasattr(m, "__all__"):
            funcs = [f for name, f in funcs.items() if name in m.__all__]
        else:
            logger.warning(
                f"Module {module_name} does not define __all__. You probably want do to that."
            )

        class_dict = {k: v for k, v in m.__dict__.items() if isinstance(v, type)}
        if hasattr(m, "__all__"):
            classes = [v for k, v in class_dict.items() if k in m.__all__]
        else:
            classes = list(class_dict.values())

        def is_enum(x):
            try:
                return issubclass(x, Enum)
            except TypeError:
                return False

        def falsey_if_exception(f):
            def wrapped(*args, **kwargs):
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    logger.exception(e)
                    return False

            return wrapped

        make_func = falsey_if_exception(Function.from_callable)
        return Module(
            name=module_name,
            docstring=module_docstring or "",
            functions=[y for f in funcs if (y := make_func(f))],
            classes=[Class.from_class(c) for c in classes],
            enums=[
                Enumeration(name=k, levels=[l.name for l in v], docstring=v.__doc__)
                for k, v in m.__dict__.items()
                if is_enum(v) and not k == "Enum"
            ],
        )

    def __repr_markdown__(self) -> str:
        tmpl = Template(config.module_template)
        return tmpl.render(
            name=self.name,
            docstring=self.docstring,
            classes=[c.__repr_markdown__() for c in self.classes],
            functions=[f.__repr_markdown__() for f in self.functions],
            enums=[e.__repr_markdown__() for e in self.enums],
        )
