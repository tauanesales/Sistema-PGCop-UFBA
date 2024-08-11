#!/usr/bin/env bash

function prepare_shell () {
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
}

if [ "$1" == "install" ]; then
    if [ "$(dpkg -s libffi-dev 2> /dev/null)" == "" ]; then
        sudo apt install libffi-dev
    fi

    if [ "$(dpkg -s libssl-dev 2> /dev/null)" == "" ]; then
        sudo apt install libssl-dev
    fi

    if [ ! -d "$HOME/.pyenv" ]; then
        curl https://pyenv.run | bash
    fi

    prepare_shell
    pyenv install -s
    pip install poetry
    poetry lock --no-update
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
            sudo docker compose -f docker-compose.yml up -d db
            ;;

        "down")
            sudo docker compose -f docker-compose.yml down
            ;;
        
        "rm-containers")
            sudo docker rm -f "$(docker ps -aq)"
            ;;

        "start-docker")
            sudo service docker start
            ;;
            
        "revision")
            poetry run alembic revision --autogenerate -m "$2"
            ;;

        "migrate")
            poetry run alembic upgrade head
            ;;

        "downgrade")
            poetry run alembic downgrade -1
            ;;

        "db-full-clean")
            sudo docker compose exec db mysql -u "$2" -p"$3" -e "DROP DATABASE IF EXISTS $4; CREATE DATABASE $4;"
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
