all: test

test: unif aunif

unif:
				python3 unif-tests.py

aunif:
				python3 aunif-tests.py
