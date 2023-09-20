import argparse
import json
import logging
from urllib.parse import urljoin

import requests

from book import download_image, download_txt, parse_book_page
from category import get_category_links
from fetch import make_request

LIBRARY_HOST = 'https://tululu.org'
CATEGORY_ID = 55


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('backoff').addHandler(logging.StreamHandler())

    args = parse_args()

    category_base_url = urljoin(LIBRARY_HOST, f'l{CATEGORY_ID}')
    category_books = get_category_links(category_base_url, 1, 2)
    print(category_books)

    saved_books_count = 0
    books_meta = []
    for book_id in category_books:
        try:
            book_page_html = make_request(f'{LIBRARY_HOST}/b{book_id}/').text
            book_details = parse_book_page(book_page_html)

            saved_book = download_txt(
                f'{LIBRARY_HOST}/txt.php', int(book_id), book_details["title"], 'books/')
            img_url = f'{LIBRARY_HOST}/{book_details["img_src"]}'
            saved_img = download_image(img_url, 'images/')
            logging.info(f'Book saved to {saved_book} with cover {saved_img}.')

            books_meta.append(book_details)

            saved_books_count += 1
        except requests.HTTPError as e:
            logging.error(f'Book {book_id} is not saved: {e}')

    with open("books.json", "w") as books:
        json.dump(books_meta, books, ensure_ascii=False)
    logging.info(f'Done! {saved_books_count} saved.')



def parse_args():
    desc = """
    Download books from tululu.org in batches.
    Use start_id and end_id to specify the beginning and the end of the
    books range to download.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'start_id', type=int, nargs='?', default=1,
        help='Book ID at the beginning of the downloading range.')
    parser.add_argument(
        'end_id', type=int, nargs='?', default=10,
        help='Book ID at the end of the downloading range (included).')
    return parser.parse_args()


if __name__ == '__main__':
    main()
