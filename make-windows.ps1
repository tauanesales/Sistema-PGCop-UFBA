$env:PYENV="$HOME\.pyenv\pyenv-win\"
$env:PYENV_HOME=$env:PYENV
$env:PYENV_ROOT=$env:PYENV
$env:PATH=$env:PYENV+"bin;"+$env:PATH

if ($Args[0] -eq "install") {
    if (!(Get-Command pyenv -errorAction SilentlyContinue)) {
        Invoke-WebRequest -Uri "https://github.com/pyenv-win/pyenv-win/archive/master.zip" -OutFile "$HOME\pyenv-win.zip"
        Expand-Archive -Force "$HOME\pyenv-win.zip" "$HOME\.pyenv"
        Get-ChildItem -Path "$HOME\.pyenv\pyenv-win-master\*" -Recurse | Move-Item -Destination "$HOME\.pyenv\"
        Remove-Item "$HOME\pyenv-win.zip"
        Remove-Item "$HOME\.pyenv\pyenv-win-master\"
    }

    pyenv install -s
    $pyversion = pyenv local
    $pypath = "$env:PYENV\versions\$pyversion"
    & "$pypath\Scripts\pip.exe" install virtualenv
    & "$pypath\python.exe" -m virtualenv -p="$pypath\python.exe" .
    & ".\Scripts\activate"

    pip install poetry
	poetry lock --no-update
	poetry install --no-root

    deactivate

} elseif ($Args[0] -eq "help") {
    foreach ($ln in (Get-Content -Path .\Makefile)) {
        if ($ln -match '(.+):(.*) ## (.+)') {
            Write-Host ("{0,-31}" -f $Matches[1]) -NoNewline -ForegroundColor DarkCyan
            Write-Host $Matches[3]
        }
    }
} else {
    & ".\Scripts\activate"

    switch ($Args[0]) {
        "run" {
            poetry run python -m src.api
            Break
        }

        "test" {
            poetry run python -m pytest ./src/tests -vv -s
            Break
        }

        "export-requirements" {
            poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev
            Break
        }

        "add-dependency" {
            poetry add $Args[1]
        }

        "up-db" {
            docker ps 2>&1 | Out-Null

            while ($LASTEXITCODE -gt 0) {
                docker ps 2>&1 | Out-Null
                Start-Sleep -Seconds 0.5
            }

            docker compose -f docker-compose.yml up -d db
            Break
        }

        "down" {
            docker compose -f docker-compose.yml down
            Break
        }
        
        "rm-containers" {
            $psaq = docker ps -aq
            docker rm -f "$psaq"
            Break
        }

        "start-docker" {
            Start-Process -FilePath "C:\Program Files\Docker\Docker\Docker Desktop.exe"
            Break
        }
            
        "revision" {
            poetry run alembic revision --autogenerate -m $Args[1]
            Break
        }

        "migrate" {
            poetry run alembic upgrade head
            Break
        }

        "downgrade" {
            poetry run alembic downgrade -1
            Break
        }

        "db-full-clean" {
            $database = $Args[3]
            docker compose exec db mysql -u $Args[1] -p$Args[2] -e "DROP DATABASE IF EXISTS $database; CREATE DATABASE $database;"
            Break
        }

        "pre-commit" {
            poetry run pre-commit run --config ./.pre-commit-config.yaml --all-files
            Break
        }

        "patch" {
            poetry version patch
            Break
        }

        "minor" {
            poetry version minor
            Break
        }

        "clean" {
            foreach ($item in ("pycache", "*.pyc", "*.log")) {
                Get-ChildItem -Recurse -Name -Include $item | Remove-Item -Recurse -Confirm:$false -Force
            }
            Break
        }
    }

    deactivate
}
