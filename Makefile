ifneq ("$(wildcard .env)","")
	include .env
	export
endif

ifeq ($(OS),Windows_NT)
	INSTALL_SCRIPT=powershell -ExecutionPolicy bypass .\make-windows.ps1
else
	ifdef GITHUB_ACTIONS
		INSTALL_SCRIPT=bash make-github-workflow.sh
	else
		INSTALL_SCRIPT=bash make-linux.sh
	endif
endif

.PHONY: run-only
run-only: ## Only run the project, without start the docker and the database. Use if docker and database already started.
	${INSTALL_SCRIPT} run

.PHONY: run
run: start-docker up-db run-only ## Run the project.

.PHONY: test
test: ## Run tests.
	${INSTALL_SCRIPT} test

.PHONY: install
install: ## Install the project.
	${INSTALL_SCRIPT} install

.PHONY: add-dependency
add-dependency: ## Add a new dependency to the project. Use DEPNAME="dependency_name" to specify the dependency.
	${INSTALL_SCRIPT} add-dependency ${DEPNAME}

.PHONY: export-requirements
export-requirements: ## Export requirements to requirements.txt, so it can be used by Vercel.
	${INSTALL_SCRIPT} export-requirements

.PHONY: up-db
up-db: ## Start local MySQL database using docker.
	${INSTALL_SCRIPT} up-db

.PHONY: down
down: ## Stop all docker services from this project.
	${INSTALL_SCRIPT} down

.PHONY: rm-containers
rm-containers: ## Remove all docker containers.
	${INSTALL_SCRIPT} rm-containers

.PHONY: start-docker
start-docker: ## Start the docker. WSL needs to manually start docker.
	${INSTALL_SCRIPT} start-docker

.PHONY: revision
revision: ## Create a new revision of the database using alembic. Use MESSAGE="your message" to add a message.
	${INSTALL_SCRIPT} revision ${MESSAGE}

.PHONY: migrate
migrate: ## Apply the migrations to the database.
	${INSTALL_SCRIPT} migrate

.PHONY: downgrade
downgrade: ## Undo the last migration.
	${INSTALL_SCRIPT} downgrade

.PHONY: db-full-clean
db-full-clean: ## Drop and recreate the database.
	${INSTALL_SCRIPT} db-full-clean ${DB_USERNAME} ${DB_PASSWORD} ${DB_DATABASE}

.PHONY: db-reset
db-reset: db-full-clean migrate ## Drop, recreate and apply all migrations to the database.

.PHONY: pre-commit
pre-commit: ## Run pre-commit checks.
	${INSTALL_SCRIPT} pre-commit

.PHONY: patch
patch: ## Bump project version to next patch (bugfix release/chores).
	${INSTALL_SCRIPT} patch

.PHONY: minor
minor: ## Bump project version to next minor (feature release).
	${INSTALL_SCRIPT} minor

.PHONY: clean
clean: ## Clean project's temporary files.
	${INSTALL_SCRIPT} clean

.DEFAULT_GOAL := help
help:
ifeq ($(OS),Windows_NT)
	@${INSTALL_SCRIPT} help
else
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' "Makefile" | sed 's/Makefile://g' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
endif
