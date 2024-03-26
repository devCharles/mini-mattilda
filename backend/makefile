.DEFAULT_GOAL := all

dev: 
	poetry run uvicorn app.main:app --reload 

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