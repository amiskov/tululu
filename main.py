import os
import logging
from pathlib import Path
from urllib.parse import urlsplit, unquote

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def main():
    for book_id in range(1, 11):
        # get title & author
        resp = requests.get(f'https://tululu.org/b{book_id}/')
        resp.raise_for_status()
        try:
            soup = BeautifulSoup(resp.text, 'lxml')
            content = soup.find('div', {'id': 'content'})

            genres = []
            genre_tags = content.find('span', class_='d_book').find_all('a')
            for tag in genre_tags:
                genres.append(tag.text)

            comments = []
            comment_tags = content.find_all('div', class_='texts')
            for tag in comment_tags:
                comments.append(tag.find('span', class_='black').text)

            h1 = content.find('h1').text
            title, author = [part.strip() for part in h1.split('::')]

            img_path = content.find('table', class_='d_book').find(
                'div', class_='bookimage').find('img')['src']
            img_url = f'https://tululu.org{img_path}'
            download_image(img_url, 'images/')

        except Exception as e:
            logging.error(
                f'Failed to find title and author for {book_id}: {e}')
            continue

        url = f'https://tululu.org/txt.php?id={book_id}'
        try:
            download_txt(url, f'{book_id}. {title}', 'books')
        except requests.HTTPError as e:
            logging.error(e)
            continue


def check_for_redirect(resp: requests.Response):
    if resp.history and 'txt.php?id=' not in resp.url:
        raise requests.HTTPError('Bad book URL.')


def download_image(url: str, folder: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    url_path = urlsplit(url).path
    _, filename = os.path.split(unquote(url_path))

    images_dir = Path(folder)
    images_dir.mkdir(exist_ok=True)

    image_file = images_dir.joinpath(filename)

    with open(image_file, 'wb') as file:
        file.write(response.content)
    logging.info(f'{filename} has been saved.')
    return str(image_file)


def download_txt(url: str, filename: str, folder='books/') -> str:
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Returns:
        str: Путь до файла, куда сохранён текст.

    Examples:
        url = 'http://tululu.org/txt.php?id=1'

        filepath = download_txt(url, 'Алиби')
        print(filepath)  # Выведется books/Алиби.txt

        filepath = download_txt(url, 'Али/би', folder='books/')
        print(filepath)  # Выведется books/Алиби.txt

        filepath = download_txt(url, 'Али\\би', folder='txt/')
        print(filepath)  # Выведется txt/Алиби.txt
    """
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    books_dir = Path(folder)
    books_dir.mkdir(exist_ok=True)

    book_file = books_dir.joinpath(sanitize_filename(filename + '.txt'))

    with open(book_file, 'wb') as file:
        file.write(response.content)
    logging.info(f'{filename} has been saved.')
    return str(book_file)


if __name__ == '__main__':
    main()
