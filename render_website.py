import os
import math
import json

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload(db_filename: str, target_dir: str):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = env.get_template('template.html')

    with open(db_filename, 'r') as books_db_file:
        books_db = books_db_file.read()
    books = json.loads(books_db)
    total_pages = math.ceil(len(books) / 10)
    print(total_pages, )
    books_pages = chunked(books, 10)

    for (page_num, books) in enumerate(books_pages, start=1):
        rendered_page = template.render(
            books=chunked(books, 2),
            total_pages=total_pages
        )
        with open(f'{target_dir}/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    target_dir = 'pages'
    os.makedirs(target_dir, exist_ok=True)
    server = Server()
    on_reload('books.json', target_dir)
    server.watch('template.html', lambda: on_reload('books.json', target_dir), delay='forever')
    server.serve(root='.')


if __name__ == '__main__':
    main()
