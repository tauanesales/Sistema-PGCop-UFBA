# Getting Started - Back-end: Sistema de Monitoramento
Neste documento, você encontrará instruções sobre como configurar o ambiente do projeto,
executar o servidor e implementar novas features de forma segura.

## Sumário
- [Antes da instalação](#antes-da-instalação)
- [Instalação](#instalação)
- [Executando a aplicação](#executando-a-aplicação)
- [Para o desenvolvedor](#para-o-desenvolvedor)

## Antes da instalação
Certifique-se que o `git` esteja instalado e configurado em sua máquina. Caso contrário, você pode instalá-lo seguindo os tutoriais para [Linux](https://diolinux.com.br/tutoriais/instalar-e-usar-git-no-linux-2.html) ou [Windows](https://phoenixnap.com/kb/how-to-install-git-windows).

Certifique-se também que que o `makefile` esteja instalado. Caso contrário, você pode instalá-lo seguindo os tutoriais para [Linux](https://ioflood.com/blog/install-make-command-linux/) ou [Windows](https://leangaurav.medium.com/how-to-setup-install-gnu-make-on-windows-324480f1da69).

Você deve possuir algum Sistema de Gerenciamento de Banco de Dados (SGBD) rodando localmente ou remotamente, como MySQL, PostgreSQL, SQLite, etc. Mais detalhes [aqui](https://docs.sqlalchemy.org/en/20/dialects/index.html). Se desejar subir o banco via docker, você pode seguir [este tutorial](https://gist.github.com/martinsam16/4492957e3bbea34046f2c8b49c3e5ac0) para instalar o docker.

Você também deve possuir uma conta no [SendGrid](https://sendgrid.com/), necessário para o envio automatizado de emails.

Por fim, você deve possuir o Python 3.9.13 instalado em sua máquina. Recomenda-se utilizar o pyenv para gerenciar as versões do Python em sua máquina. Mais detalhes [aqui](https://github.com/pyenv/pyenv?tab=readme-ov-file#simple-python-version-management-pyenv)


## Instalação

### 1. Clone o repositório do projeto

```sh
git clone https://github.com/tauanesales/BACK-MATE85-Topicos-em-sistemas-de-informacao-e-web-i.git
```

### 2. Acesse a pasta do projeto

```sh
cd BACK-MATE85-Topicos-em-sistemas-de-informacao-e-web-i
```

### 3. Instale as dependências

```sh
make install
```
<br>

> **Atenção:** Se você estiver instalando o projeto no Windows e tiver problemas com as políticas de execução de scripts do Powershell, altere-as para que scripts Powershell possam ser executados (você pode seguir [esse tutorial](https://lazyadmin.nl/powershell/running-scripts-is-disabled-on-this-system/) ou ler mais na [página oficial do Windows](https://learn.microsoft.com/pt-br/powershell/module/microsoft.powershell.core/about/about_execution_policies)).

### 4. Configure as variáveis de ambiente
Na pasta do projeto há um arquivo chamado `.env.sample`. Renomeie-o para `.env`, abra-o como arquivo de texto e preencha as seguintes variáveis:

#### Variáveis relacionadas ao SGBD
A URL de um banco de dados costuma seguir o seguinte formato: `<dialect>+<driver>://<username>:<password>@<host>:<port>/<database>`. A partir disso, seguem as seguintes variáveis:
- `DB_DRIVERNAME` - Nome do SGBD a ser utilizado. O valor dessa variável depende de qual SGBD você vai utilizar neste projeto. É o mesmo valor que teria `<dialect>+<driver>` na URL. Para mais detalhes, [clique aqui](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls).
- `DB_USERNAME` e `DB_PASSWORD` - Nome de usuário e senha, respectivamente, registrados no SGBD. São os mesmos valores que `<username>` e `<password>` teriam na URL, respectivamente.
- `DB_HOST` e `DB_PORT` - Endereço e porta, respectivamente, onde o SGBD está hospedado. São os mesmos valores que `<host>` e `<port>` teriam na URL, respectivamente.
- `DB_DATABASE` - Nome do banco de dados no SGBD a ser utilizado pelo projeto. É o mesmo valor que teria `<database>` na URL.

#### Variáveis relacionadas ao SendGrid
- `SENDGRID_API_KEY` - Chave API da aplicação no SendGrid.
- `SENDGRID_EMAIL` - Email da sua conta no SendGrid.

#### Variáveis relacionadas ao sistema de segurança da aplicação
- `ALGORITHM` - Algoritmo de assinatura a ser utilizado. O valor padrão é `HS256`. Todos os algorítmos suportados estão listados [aqui](https://python-jose.readthedocs.io/en/latest/jws/index.html#supported-algorithms).
- `SECRET_KEY` - Chave secreta e aleatória a ser utilizada pela aplicação. É recomendado que o tamanho em bits dessa chave seja o mesmo (ou maior) utilizado pelo algoritmo especificado em `ALGORITHM` (por exemplo, se o algoritmo é o `HS256`, então é preferível que a chave tenha 256 bits de tamanho).
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Duração em minutos em que os tokens gerados para os usuários irão expirar. O padrão é 30.

## Executando a aplicação
Depois de instalado, insira o seguinte comando dentro da pasta do projeto para executá-lo:
```sh
make run
```

## Para o desenvolvedor
Os seguintes comandos foram feitos para serem usados durante o desenvolvimento deste projeto. Após o merge na branch **master**, o deploy da aplicação é feito automaticamente pelo Vercel.

### Adicionando novas dependências ao projeto
Para adicionar novas dependências, utilize o seguinte comando:
```sh
poetry add nome_da_dependencia
```

Sempre que novas dependências forem adicionadas, o seguinte comando deve ser executado:
```sh
make export-requirements
```

### Executando testes unitários
Para executar os testes unitários do projeto, utilize o seguinte comando:
```sh
make test
```
