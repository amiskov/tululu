# Download Books
There are a couple of scripts to download books from [tululu](https://tululu.org) library. You can download arbitrary books by IDs or in batches from 'Science Fiction' category.

## Install
Add deps using [Poetry](https://python-poetry.org):

```sh
poetry install
```

## Fetch Arbitrary Books
Load first 10 books (book IDs from 1 to 10 including 10):

```sh
poetry run python parse_tululu_books.py
```

You can download books passing IDs range as an argument. For example, this will load books from 10 to 20 (including 20):

```sh
poetry run python parse_tululu_books.py 10 20
```

## Fetch Science Fiction Category Books
Check all available options (help):

```sh
poetry run python parse_tululu_category.py -h
```

By default, book texts, covers and metadata will be saved to the current directory. Texts to `books/` folder, covers to `images/` and metadata to `books.json` file. Books metadata includes book's title, author, cover, genres and comments. If you want to store the data elsewhere, use `--dest_folder` to specify the desired folder:

```sh
poetry run python parse_tululu_category.py --dest_folder my_scify_books
```

There are a lot of books in 'Science Fiction' category. If you don't need all of them, you can specify only the desired range of pages using `--start_page` and `--end_age` options. E.g. this command will fetch books texts, covers and metadata from pages 1 and 2:

```sh
# Fetch books from page 1 to 3 (not included):
poetry run python parse_tululu_category.py --start_page 1 --end_page 3
```

If you don't need texts or images, use `--skip_txt` and `--skip_imgs` respectively:

```sh
# Fetch only texts from the 1st page:
poetry run python parse_tululu_category.py --skip_imgs \
    --start_page 1 --end_page 2

# Fetch only 1st page metadata skipping texts and covers:
poetry run python parse_tululu_category.py --skip_imgs --skip_txt \
    --start_page 1 --end_page 2
```

To download all the books with texts, covers and metadata from the 'Science Fiction' category to the current folder, run the script without any arguments. Be careful, there are really lots of books!

```sh
poetry run python parse_tululu_category.py
```
