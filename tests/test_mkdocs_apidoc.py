from mkdocs_apidoc.render import render_page


def test_render_page():
    page = """
# Here is some markdown

{{ auto_object("mkdocs_apidoc.render.markdown") }}
    
    """
    rendered = render_page(page)
    print(rendered)
