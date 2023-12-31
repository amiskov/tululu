# Offline SciFi Library
Scripts to download SciFi books from [tululu](https://tululu.org) and create an offline library.

You can download arbitrary books by IDs or in batches from 'Science Fiction' category. Also, you can render HTML-pages with book titles, covers etc. making your own offline library and re-publish it to GitHub pages with a single command.

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
poetry run python parse_tululu_category.py --dest_folder my_scifi_books
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

## Create Offline-based Website
This command will create static HTML-pages with pagination for downloaded books:

```sh
poetry run python render_website.py
cd pages/ # see a bunch of `.html` pages here
```

For develpoment, run it in serving mode and change the `template.html` file as you need:

```sh
poetry run python render_website.py --serve
```

This will fire up a webserver in livereload mode, so you can change the design and have rendered HTML pages on the fly.

## Deploy to GitHub Pages
If you need books to be published online, run `deploy.sh` script. It will publish rendered HTML-pages to the `gh-pages` branch of your repo. Make sure to change the address of a GitHub repo and create `gh-pages` branch:

```sh
# Create `gh-pages` branch for publishing your library
git checkout --orphan gh-pages
echo "Hello, GitHub Pages!" > readme.md
git add readme.md
git commit -m "init gh-pages branch"
git push --set-upstream origin gh-pages

# Publish your library:
sh deploy.sh
```

Check `https://<YOUR-USERNAME>.github.io/tululu/pages/index1.html` URL.
