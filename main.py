import argparse
import json
import logging
from urllib.parse import urljoin

import requests

from book import download_image, download_txt, parse_book_page
from category import get_book_ids
from fetch import make_request

LIBRARY_HOST = 'https://tululu.org'
CATEGORY_ID = 55


def main():
    logging.basicConfig(level=logging.INFO)
    logging.getLogger('backoff').addHandler(logging.StreamHandler())

    args = parse_args()

    books_count, saved_books_count = args.end_id - args.start_id + 1, 0
    for book_id in range(args.start_id, args.end_id+1):
        try:
            book_page_html = make_request(f'{LIBRARY_HOST}/b{book_id}/').text
            book_details = parse_book_page(book_page_html)
            saved_book = download_txt(LIBRARY_HOST, book_id, book_details["title"], 'books/')
            img_url = f'{LIBRARY_HOST}/{book_details["img_src"]}'
            saved_img = download_image(img_url, 'images/')
            logging.info(f'Book saved to {saved_book} with cover {saved_img}.')
            saved_books_count += 1
        except requests.HTTPError as e:
            logging.error(f'Book {book_id} is not saved: {e}')

    logging.info(f'Done! Books saved: {saved_books_count} of {books_count}.')




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
