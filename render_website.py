import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server


def on_reload():
    books = []
    with open('books.json', 'r') as my_file:
        books = json.loads(my_file.read())
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    server = Server()
    on_reload()
    server.watch('template.html', on_reload, delay='forever')
    server.serve(root='.')


if __name__ == '__main__':
    main()
