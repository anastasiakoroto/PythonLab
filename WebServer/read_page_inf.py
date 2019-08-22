from jinja2 import Environment, FileSystemLoader


def read_page(name, **context):
    file_loader = FileSystemLoader('pages')
    env = Environment(loader=file_loader)
    tmpl = env.get_template(name)
    return tmpl.render(**context).encode()
