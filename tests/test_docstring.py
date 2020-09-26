from mkdocs_apidoc.parser import docstring_with_code_outputs


def test_parse_code_block_no_op_if_no_code():
    text = """This looks like a docstring

    Here is some arbitrary text


    Here is more stuff

    and even more.
    """
    new = docstring_with_code_outputs(text)
    print(new)


def test_parse_code_block():
    text = """This looks like a docstring
    
    Here is some arbitrary text
    
    ```python
    x = 2
    y = 5
    print(x + y)
    ```
    
    ought to be able to go in between too.
    
    ```python
    print("world")
    ```
    
    Here is more stuff
    
    and even more.
    """
    new = docstring_with_code_outputs(text)
    print(new)
