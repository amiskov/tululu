run:
	poetry run python main.py
run2:
	poetry run python main.py 1 2
repl:
	poetry run ipython
test:
	poetry run python -m doctest main.py
