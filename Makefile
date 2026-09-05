.PHONY: install run debug clean lint lint-strict

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ mazegen/__pycache__
	rm -rf .mypy_cache .pytest_cache
	rm -rf build dist *.egg-info
	rm -rf maze.txt
	find . -type f -name "*.pyc" -delete

build:
	python3 -m build

lint:
	flake8 --exclude=venv .
	mypy --exclude venv . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 --exclude=venv .
	mypy --exclude venv . --strict