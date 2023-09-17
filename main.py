import argparse
import logging
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

LIBRARY_HOST = 'https://tululu.org'


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    books_count, saved_books_count = args.end_id - args.start_id + 1, 0
    for book_id in range(args.start_id, args.end_id+1):
        try:
            book_page_html = make_request(f'{LIBRARY_HOST}/b{book_id}/').text
            book_details = parse_book_page(book_page_html)
            saved_book = download_txt(book_id, book_details["title"], 'books/')
            saved_img = download_image(book_details['cover_url'], 'images/')
            logging.info(f'Book saved to {saved_book} with cover {saved_img}.')
            saved_books_count += 1
        except requests.RequestException as e:
            logging.error(e)
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


def make_request(url: str, params=None) -> requests.Response:
    """Return response of the request to the given `url`.

    Fails if redirect happens.
    """
    resp = requests.get(url, params=params)
    resp.raise_for_status()

    # former `check_for_redirect` function
    if resp.history:
        raise requests.HTTPError('Redirects not allowed.')

    return resp


def parse_book_page(page_html: str) -> dict:
    """Extract book details from HTML soup."""
    soup = BeautifulSoup(page_html, 'lxml')
    content = soup.find('div', {'id': 'content'})

    h1 = content.find('h1').text
    title, author = [part.strip() for part in h1.split('::')]

    img_path = content.find('table', class_='d_book').find(
        'div', class_='bookimage').find('img')['src']

    genres = []
    genre_tags = content.find('span', class_='d_book').find_all('a')
    for genre_tag in genre_tags:
        genres.append(genre_tag.text)

    comments = []
    comment_tags = content.find_all('div', class_='texts')
    for comment_tag in comment_tags:
        comments.append(comment_tag.find('span', class_='black').text)

    return {
        'title': title,
        'author': author,
        'cover_url': f'https://tululu.org{img_path}',
        'genres': genres,
        'comments': comments,
    }


def get_filename_from_url(url: str) -> str:
    """Return filename with extension from `url`.

    >>> get_filename_from_url('https://example.com/images/test.png')
    'test.png'
    """
    url_path = urlsplit(url).path
    _, filename = os.path.split(unquote(url_path))
    return filename


def download_image(url: str, folder: str) -> Path:
    """Save an image from `url` to the given `folder`."""
    image_name = get_filename_from_url(url)
    image_file = get_filepath(image_name, folder)
    resp = make_request(url)
    with open(image_file, 'wb') as file:
        file.write(resp.content)
    return image_file


def download_txt(book_id: int, book_title: str, folder='books/') -> Path:
    """Download text content from the given `url`.

    Args:
        book_id (int): book ID to download.
        book_title (str): the title of the book.
        folder (str): desired directory name to store the book content.

    Returns:
        Path: path to created text file.

    Examples:
        > download_txt(1, 'Алиби')
        'books/1.Алиби.txt'

        > download_txt(1, 'Али/би', folder='books/')
        'books/1.Алиби.txt'

        > download_txt(1, 'Али\\би', folder='txt/')
        'txt/1.Алиби.txt'
    """
    correct_filename = sanitize_filename(f'{book_id}.{book_title}' + '.txt')
    book_file = get_filepath(correct_filename, folder)
    resp = make_request(f'{LIBRARY_HOST}/txt.php', {'id': book_id})
    with open(book_file, 'wb') as file:
        file.write(resp.content)
    return book_file


def get_filepath(filename: str, foldername: str) -> Path:
    folder = Path(foldername)
    folder.mkdir(exist_ok=True)
    return folder.joinpath(filename)


if __name__ == '__main__':
    main()
