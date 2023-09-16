# Download Books
Script to download books from [tululu](https://tululu.org) library. Saves texts as `.txt` files to `books/` folder alongside with book covers in `images/`.

## Install
Add deps using [Poetry](https://python-poetry.org):

```sh
poetry install
```

## Run
Load first 10 books (book IDs from 1 to 10 including 10):

```sh
poetry run python main.py
```

You can download arbitrary amount of books passing book IDs range as an argument. For example, this will load books from 10 to 20 (including 20):

```sh
poetry run python main.py 10 20
```
