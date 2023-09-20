run:
	poetry run python main.py
run2:
	poetry run python main.py 1 2
runcat:
	poetry run python parse_tululu_category.py
repl:
	poetry run ipython
test:
	poetry run python -m doctest main.py
