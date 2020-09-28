import contextlib
import sys
from importlib import import_module
from io import StringIO
from textwrap import dedent
from typing import List, Tuple


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old


def parse_code_blocks(
    input: str, start: str = "```python", end: str = "```"
) -> List[Tuple[bool, str]]:
    """Split input into list of strings, the boolean indicates if the string is code."""

    header, *blocks = input.split(start)
    result = [(False, header)]
    for block in blocks:
        end_idx = block.find(end)
        code, rest = block[:end_idx], block[end_idx + len(end) :]
        result.append((True, dedent(code)))
        result.append((False, rest))
    return result


def docstring_with_code_outputs(text: str) -> str:
    blocks = parse_code_blocks(text)

    output = []
    for is_code, block in blocks:
        if is_code:
            with stdoutIO() as s:
                exec(block)

            stdout = s.getvalue()
            if stdout != "":
                stdout = f"```\n{stdout}```"
            output.append(f"```python{block}```\n{stdout}")
        else:
            output.append(block)

    return "".join(output)


def obj_from_string(s: str) -> object:
    """Given a string for an object, return the actual object

    ```
    f = obj_from_string('mymodule.myfunc')
    ```
    """
    mod_name, *rest = s.split(".")
    mod = import_module(mod_name)
    current = mod
    for attr in rest:
        current = getattr(current, attr)
    return current
