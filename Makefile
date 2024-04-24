ifneq ("$(wildcard .env)","")
	include .env
	export
endif

ifeq ($(OS),Windows_NT)
	INSTALL_SCRIPT=powershell .\make-windows.ps1
else
	INSTALL_SCRIPT=bash make-linux.sh
endif

run:
	${INSTALL_SCRIPT} run

test:
	${INSTALL_SCRIPT} test

install:
	${INSTALL_SCRIPT} install

export-requirements:
	${INSTALL_SCRIPT} export-requirements
