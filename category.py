import logging

from bs4 import BeautifulSoup
import requests

from fetch import make_request


def get_category_links(category_base_url: str, start_page: int = 1, end_page: int = 10) -> list[str]:
    """Return list of book links from the given category."""
    # total_pages = 0
    category_books = []
    for page in range(start_page, end_page+1):
        try:
            page_url = f'{category_base_url}/{page}'
            logging.info(f'fetching {page_url}...')
            page_html = make_request(page_url)
            soup = BeautifulSoup(page_html.text, 'lxml')
            content = soup.select_one('div#content')

            if not content:
                logging.error(f'Category HTML not found in {page_url}')
                continue

            # if not total_pages:
            #     paging = content.select_one('div#content p:last-child a:last-child')
            #     if not paging:
            #         return 'Paging not found'
            #     total_pages = int(paging.getText())

            book_link_tags = content.select('table.d_book tr td .bookimage a')
            page_books = [link['href'][2:-1] for link in book_link_tags]
            category_books.extend(page_books)
            print(f'Added {len(page_books)} book links.')
        except requests.HTTPError:
            logging.error(f'page {page} not found')
    return category_books
