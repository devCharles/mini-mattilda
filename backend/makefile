.DEFAULT_GOAL := all

dev: 
	cd app && poetry run uvicorn main:app --reload && cd ..

isort:
	poetry run isort .

black:
	poetry run black .

flake8:
	poetry run flake8 .

pylint:
	poetry run pylint .

test:
	poetry run pytest

lint-fix: isort black flake8

lint: pylint

tests: test

all: lint tests