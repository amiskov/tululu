import argparse
import logging
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def main():
    logging.basicConfig(level=logging.INFO)
    args = parse_args()

    books_count, saved_books_count = args.end_id - args.start_id + 1, 0
    for book_id in range(args.start_id, args.end_id+1):
        page_url, txt_url = get_book_urls(book_id)

        try:
            book_page_html = make_request(page_url).text
            book_details = parse_book_page(book_page_html)
            saved_book = download_txt(txt_url,
                                      f'{book_id}. {book_details["title"]}',
                                      'books/')
            saved_img = download_image(book_details['cover_url'], 'images/')
            logging.info(f'Book saved to {saved_book} with cover {saved_img}.')
            saved_books_count += 1
        except requests.RequestException as e:
            logging.error(e)
        finally:
            continue
    logging.info(f'Done! Books saved: {saved_books_count} of {books_count}.')


def parse_args():
    parser = argparse.ArgumentParser(prog='Books Downloader')
    parser.add_argument('start_id', type=int, nargs='?', default=1)
    parser.add_argument('end_id', type=int, nargs='?', default=10)
    return parser.parse_args()


def make_request(url: str) -> requests.Response:
    """Return response of the request to the given `url`.

    Fails if redirect happens.
    """
    resp = requests.get(url, allow_redirects=False)
    resp.raise_for_status()

    # former `check_for_redirect` function
    if 300 <= resp.status_code < 400:
        raise requests.HTTPError('Redirects not allowed.')

    return resp


def get_book_urls(book_id: int) -> tuple[str, str]:
    """Return 2 urls: book description page and downloadable txt."""
    host = 'https://tululu.org'
    txt_url = f'{host}/txt.php?id={book_id}'
    page_url = f'{host}/b{book_id}/'
    return page_url, txt_url


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
    return download_to_file(url, image_file)


def download_txt(url: str, filename: str, folder='books/') -> Path:
    """Download text content from the given `url`.

    Args:
        url (str): link to text cntent.
        filename (str): name of the file to store the text.
        folder (str): desired directory name to store the file with text.

    Returns:
        str: path to created text file.

    Examples:
        url = 'http://tululu.org/txt.php?id=1'

        > download_txt(url, 'Алиби')
        'books/Алиби.txt'

        > download_txt(url, 'Али/би', folder='books/')
        'books/Алиби.txt'

        > download_txt(url, 'Али\\би', folder='txt/')
        'txt/Алиби.txt'
    """
    correct_filename = sanitize_filename(filename + '.txt')
    book_file = get_filepath(correct_filename, folder)
    return download_to_file(url, book_file)


def download_to_file(url: str, filepath: Path) -> Path:
    """Save resource from `url` as a file to `filepath`.
    
    Returns:
        filepath (Path): path to file with content from `url`.
    """
    resp = make_request(url)
    with open(filepath, 'wb') as file:
        file.write(resp.content)
    return filepath


def get_filepath(filename: str, foldername: str) -> Path:
    folder = Path(foldername)
    folder.mkdir(exist_ok=True)
    return folder.joinpath(filename)


if __name__ == '__main__':
    main()
