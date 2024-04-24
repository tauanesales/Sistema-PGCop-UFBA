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
	poetry lock
	poetry install --no-root

    deactivate

} else {
    & ".\Scripts\activate"

    if ($Args[0] -eq "run") {
        poetry run python -m src.api

    } elseif ($Args[0] -eq "test") {
        poetry run pytest ./src/api/tests -vv -s

    } elseif ($Args[0] -eq "export-requirements") {
        poetry export -f requirements.txt --output requirements.txt --without-hashes --without dev
    } else {
        Write-Output "Erro!"
    }
    deactivate
}