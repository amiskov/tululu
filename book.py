from pathlib import Path
import os
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from fetch import make_request


def download_txt(base_url: str, book_id: int, book_title: str, folder='books/') -> Path:
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
    book_filename = sanitize_filename(f'{book_id}.{book_title}' + '.txt')
    book_path = get_filepath(book_filename, folder)
    if book_path.is_file(): # book already exists
        return book_path
    resp = make_request(base_url, {'id': book_id})
    with open(book_path, 'wb') as book:
        book.write(resp.content)
    return book_path


def download_image(url: str, folder: str) -> Path:
    """Save an image from `url` to the given `folder`."""
    image_filename = get_filename_from_url(url)
    image_path = get_filepath(image_filename, folder)

    if image_path.is_file(): # image already exists
        return image_path

    resp = make_request(url)
    with open(image_path, 'wb') as image:
        image.write(resp.content)
    return image_path


def parse_book_page(page_html: str) -> dict:
    """Extract book details from HTML soup."""
    soup = BeautifulSoup(page_html, 'lxml')
    content = soup.select_one('div#content')

    if not content:
        raise ValueError('HTML unparseable.')

    h1 = content.select_one('h1').text
    title, author = [part.strip() for part in h1.split('::')]

    cover = content.select_one('table.d_book div.bookimage img')

    genres = []
    genre = content.select_one('span.d_book')
    genre_tags = genre.select('a')
    for genre_tag in genre_tags:
        genres.append(genre_tag.text)

    comments = []
    comment_tags = content.select('div.texts')
    for comment_tag in comment_tags:
        comments.append(comment_tag.select_one('span.black').text)

    return {
        'title': title,
        'author': author,
        'img_src': cover['src'] if cover else '',
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


def get_filepath(filename: str, foldername: str) -> Path:
    folder = Path(foldername)
    folder.mkdir(exist_ok=True)
    return folder.joinpath(filename)
