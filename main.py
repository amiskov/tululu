from pathlib import Path
import logging

import requests


def main():
    for book_id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={book_id}'
        books_dir = Path('books')
        books_dir.mkdir(exist_ok=True)
        book_name = f'id{book_id}.txt'
        download_book(books_dir, url, book_name)


def download_book(dir: Path, url: str, book_name: str) -> Path:
    """Download book by `url` to `dir`.

    `url` must have a file extension at the end (`.png`, `.jpg`, etc).
    """
    response = requests.get(url)
    response.raise_for_status()

    with open(dir.joinpath(book_name), 'wb') as file:
        file.write(response.content)
    logging.info(f'{book_name} has been saved.')
    return dir / book_name 


if __name__ == '__main__':
    main()
