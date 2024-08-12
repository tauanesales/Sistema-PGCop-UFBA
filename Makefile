ifneq ("$(wildcard .env)","")
	include .env
	export
endif

ifeq ($(OS),Windows_NT)
	INSTALL_SCRIPT=powershell -ExecutionPolicy bypass .\make-windows.ps1
else
#	ifdef GITHUB_ACTIONS
#		INSTALL_SCRIPT=bash make-github-workflow.sh
#	else
#		INSTALL_SCRIPT=bash make-linux.sh
#	endif
	INSTALL_SCRIPT=bash make-linux.sh
endif

.SILENT: run run-only test install add-dependency export-requirements up-db down rm-containers clean
.SILENT: start-docker revision migrate downgrade db-full-clean db-reset pre-commit patch minor

run: start-docker up-db run-only ## Run the project.

run-only: ## Only run the project, without start the docker and the database. Use if docker and database already started.
	${INSTALL_SCRIPT} run

test: ## Run tests.
	${INSTALL_SCRIPT} test

install: ## Install the project.
	${INSTALL_SCRIPT} install

add-dependency: ## Add a new dependency to the project. Use DEPNAME="dependency_name" to specify the dependency.
	${INSTALL_SCRIPT} add-dependency ${DEPNAME}

export-requirements: ## Export requirements to requirements.txt, so it can be used by Vercel.
	${INSTALL_SCRIPT} export-requirements

.PHONY: up-mysql
up-mysql: ## Start local MySQL database using docker.
	docker compose -f docker-compose.yml up -d db

.PHONY: up-postgres
up-postgres: ## Start database container.
	docker compose up -d postgres --force-recreate

.PHONY: down
down: ## Stop all docker services from this project.
	${INSTALL_SCRIPT} down

rm-containers: ## Remove all docker containers.
	${INSTALL_SCRIPT} rm-containers

start-docker: ## Start the docker. WSL needs to manually start docker.
	${INSTALL_SCRIPT} start-docker

revision: ## Create a new revision of the database using alembic. Use MESSAGE="your message" to add a message.
	${INSTALL_SCRIPT} revision ${MESSAGE}

migrate: ## Apply the migrations to the database.
	${INSTALL_SCRIPT} migrate

downgrade: ## Undo the last migration.
	${INSTALL_SCRIPT} downgrade

db-full-clean: ## Drop and recreate the database.
	${INSTALL_SCRIPT} db-full-clean ${DB_USERNAME} ${DB_PASSWORD} ${DB_DATABASE}

db-reset: db-full-clean migrate ## Drop, recreate and apply all migrations to the database.

pre-commit: ## Run pre-commit checks.
	${INSTALL_SCRIPT} pre-commit

patch: ## Bump project version to next patch (bugfix release/chores).
	${INSTALL_SCRIPT} patch

minor: ## Bump project version to next minor (feature release).
	${INSTALL_SCRIPT} minor

clean: ## Clean project's temporary files.
	${INSTALL_SCRIPT} clean

.DEFAULT_GOAL := help
help:
ifeq ($(OS),Windows_NT)
	@${INSTALL_SCRIPT} help
else
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' "Makefile" | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
endif
