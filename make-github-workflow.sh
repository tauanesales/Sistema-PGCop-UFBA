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
    poetry add mysqlclient
    poetry install --no-root

else
    prepare_shell

    if [ "$1" == "run" ]; then
        poetry run python -m src.api

    elif [ "$1" == "test" ]; then
        poetry run pytest ./src/api/tests -vv -s
        
    elif [ "$1" == "export-requirements" ]; then
        poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev
    
    elif [ "$1" == "add-dependency" ]; then
        poetry add "$2"

    fi
fi
