run:
	poetry run python parse_tululu_books.py
run2:
	poetry run python parse_tululu_books.py 1 2
runcat:
	poetry run python parse_tululu_category.py --start_page=700 --end_page=701
repl:
	poetry run ipython
test:
	poetry run python -m doctest utils.py
serve:
	poetry run python render_website.py
deploy:
	sh deploy.sh