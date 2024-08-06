#!/usr/bin/env bash

function prepare_shell () {
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
}

if [ "$1" == "install" ]; then
    if [ ! -d "$HOME/.pyenv" ]; then
        curl https://pyenv.run | bash
    fi

    prepare_shell
    dpkg -s libffi-dev > /dev/null 2> /dev/null

    if [ ! $? ]; then
        sudo apt install libffi-dev
    fi

    pyenv install -s
    pip install poetry
    poetry lock
    poetry remove mysqlclient
    poetry add mysqlclient
    poetry install --no-root

else
    prepare_shell

    case "$1" in
        "run")
            poetry run python -m src.api
            ;;
        
        "test")
            poetry run python -m pytest ./src/tests -vv -s
            ;;

        "export-requirements")
            poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev
            ;;
        
        "add-dependency")
            poetry add "$2"
            ;;
        
        "up-db")
            docker compose -f docker-compose.yml up -d db
            ;;

        "down")
            docker compose -f docker-compose.yml down
            ;;
        
        "rm-containers")
            docker rm -f "$(docker ps -aq)"
            ;;

        "start-docker")
            sudo service docker start
            ;;
            
        "revision")
            poetry run alembic revision --autogenerate -m "$(MESSAGE)"
            ;;

        "migrate")
            poetry run alembic upgrade head
            ;;

        "downgrade")
            poetry run alembic downgrade -1
            ;;

        "db-full-clean")
            db-full-clean
            ;;

        "db-reset")
            db-full-clean migrate
            ;;

        "pre-commit")
            poetry run pre-commit run --config ./.pre-commit-config.yaml --all-files
            ;;

        "patch")
            poetry version patch
            ;;

        "minor")
            poetry version minor
            ;;

        "clean")
            find . -name '__pycache__' -exec rm -rf {} +
	        find . -name '*.pyc' -exec rm -f {} +
	        find . -name '*.log' -exec rm -f {} +
            ;;

    esac
fi
