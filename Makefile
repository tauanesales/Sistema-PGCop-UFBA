ifneq ("$(wildcard .env)","")
	include .env
	export
endif

run:
	poetry run python -m src.api

install:
	pip install poetry
	poetry lock
	poetry install --no-root

export-requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
