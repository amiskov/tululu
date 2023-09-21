import logging

from bs4 import BeautifulSoup
import requests

from utils import make_request


def get_last_pagenum(category_base_url: str) -> int:
    """
    Returns:
        The last page number from category pagination or 1 if pagination not found.
    """
    page_html = make_request(f'{category_base_url}/1')
    soup = BeautifulSoup(page_html.text, 'lxml')
    last_page_tag = soup.select_one('div#content p:last-child a:last-child')
    if not last_page_tag:
        return 1
    total_pages = int(last_page_tag.getText())
    logging.info(f'Category has {total_pages} pages in total.')
    return total_pages


def get_book_ids(category_base_url: str, start_page: int, end_page: int) -> list[str]:
    """Return list of book links from the given category."""
    category_books = []
    for page in range(start_page, end_page):
        try:
            page_url = f'{category_base_url}/{page}'
            logging.info(f'fetching {page_url}...')
            page_html = make_request(page_url)
            soup = BeautifulSoup(page_html.text, 'lxml')
            content = soup.select_one('div#content')

            if not content:
                logging.error(f'Category HTML not found in {page_url}')
                continue

            book_link_tags = content.select('table.d_book tr td .bookimage a')
            page_books = [link['href'][2:-1] for link in book_link_tags]
            category_books.extend(page_books)
            logging.info(f'Found {len(page_books)} books in {category_base_url}.')
        except requests.HTTPError:
            logging.error(f'page {page} not found')
    return category_books
