ifneq ("$(wildcard .env)","")
	include .env
	export
endif

.PHONY: run
run: ## Run the project.
	poetry run python -m src.api

.PHONY: install
install: ## Install Python requirements.
	python -m pip install --upgrade pip setuptools wheel poetry
	poetry lock
	poetry install --no-root
	poetry run pre-commit install

.PHONY: test
test: ## Run tests.
	poetry run python -m pytest . -vv -s

.PHONY: export-requirements
export-requirements: ## Export requirements to requirements.txt, so it can be used by Vercel.
	poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev

.PHONY: up-db
up-db: ## Start local MySQL database using docker.
	docker compose -f docker-compose.yml up -d db

.PHONY: down
down: ## Stop all docker services from this project.
	docker compose -f docker-compose.yml down

rm-containers: ## Remove all docker containers.
	docker rm -f $$(docker ps -aq)

.PHONY: start-docker
start-docker: ## WSL needs to manually start docker.
	sudo service docker start

.PHONY: revision
revision: ## Create a new revision of the database using alembic. Use MESSAGE="your message" to add a message.
	poetry run alembic revision --autogenerate -m "$(MESSAGE)"

.PHONY: migrate
migrate: ## Apply the migrations to the database.
	poetry run alembic upgrade head

.PHONY: downgrade
downgrade: ## Undo the last migration.
	poetry run alembic downgrade -1

.PHONY: db-full-clean
db-full-clean:
	docker compose exec db mysql -u ${DB_USERNAME} -p${DB_PASSWORD} -e "DROP DATABASE IF EXISTS ${DB_DATABASE}; CREATE DATABASE ${DB_DATABASE};"

.PHONY: db-regenerate
db-regenerate: db-full-clean migrate ## Regenerate the database.
	docker compose exec db mysql -u ${DB_USERNAME} -p${DB_PASSWORD} -e "\
		USE ${DB_DATABASE}; \
		INSERT INTO tipo_usuario (titulo, descricao, created_at, updated_at) \
		VALUES ('ALUNO', 'Aluno description', UTC_TIMESTAMP(), UTC_TIMESTAMP()), \
				('PROFESSOR', 'Professor description', UTC_TIMESTAMP(), UTC_TIMESTAMP()), \
				('COORDENADOR', 'Coordenador description', UTC_TIMESTAMP(), UTC_TIMESTAMP());"

.PHONY: pre-commit
pre-commit: ## Run pre-commit checks.
	poetry run pre-commit run --config ./.pre-commit-config.yaml --all-files

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release/chores).
	poetry version patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	poetry version minor

.PHONY: clean
clean: ## Clean project's temporary files.
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.log' -exec rm -f {} +

.DEFAULT_GOAL := help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
