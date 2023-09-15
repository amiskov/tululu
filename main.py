from pathlib import Path
import logging
from pathvalidate import sanitize_filename

import requests


def main():
    for book_id in range(1, 11):
        url = f'https://tululu.org/txt.php?id={book_id}'
        try:
            download_txt(url, 'books', book_id)
        except requests.HTTPError as e:
            logging.error(e)
            continue


def check_for_redirect(resp: requests.Response):
    if resp.history and 'txt.php?id=' not in resp.url:
        raise requests.HTTPError('Bad book URL.')


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
