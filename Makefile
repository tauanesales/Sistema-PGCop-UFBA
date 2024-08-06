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

run_: 
	${INSTALL_SCRIPT} run

run: start-docker up-db run_ down

test:
	${INSTALL_SCRIPT} test

install:
	${INSTALL_SCRIPT} install

add-dependency:
	${INSTALL_SCRIPT} add-dependency ${DEPNAME}

export-requirements:
	${INSTALL_SCRIPT} export-requirements

up-db:
	${INSTALL_SCRIPT} up-db

down:
	${INSTALL_SCRIPT} down

rm-containers:
	${INSTALL_SCRIPT} rm-containers

start-docker:
	${INSTALL_SCRIPT} start-docker

revision:
	${INSTALL_SCRIPT} revision

migrate:
	${INSTALL_SCRIPT} migrate

downgrade:
	${INSTALL_SCRIPT} downgrade

db-full-clean: 
	${INSTALL_SCRIPT} db-full-clean

db-reset:
	${INSTALL_SCRIPT} db-reset

pre-commit:
	${INSTALL_SCRIPT} pre-commit

patch:
	${INSTALL_SCRIPT} patch

minor:
	${INSTALL_SCRIPT} minor

clean:
	${INSTALL_SCRIPT} clean