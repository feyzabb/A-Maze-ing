.PHONY: install lint clean

install:
	pip install -e .
	pip install flake8 mypy

lint:
	flake8 mazegen
	mypy mazegen --strict

clean:
	rm -rf __pycache__ mazegen/__pycache__ .mypy_cache
	rm -rf *.egg-info