# Getting Started - Back-end: Sistema de Monitoramento
Neste documento, você encontrará instruções sobre como configurar o ambiente do projeto,
executar o servidor e implementar novas features de forma segura.

## Sumário
- [Antes da instalação](#antes-da-instalação)
- [Instalação](#instalação)
- [Executando a aplicação](#executando-a-aplicação)
- [Para o desenvolvedor](#para-o-desenvolvedor)

## Antes da instalação
Certifique-se que o `makefile` esteja instalado em sua máquina. Caso contrário, você pode instalá-lo seguindo os tutoriais para [Linux](https://ioflood.com/blog/install-make-command-linux/) ou [Windows](https://leangaurav.medium.com/how-to-setup-install-gnu-make-on-windows-324480f1da69).

Você deve possuir algum Sistema de Gerenciamento de Banco de Dados (SGBD) rodando localmente ou remotamente, como MySQL, PostgreSQL, SQLite, etc. Mais detalhes [aqui](https://docs.sqlalchemy.org/en/20/dialects/index.html).

Você também deve possuir uma conta no [SendGrid](https://sendgrid.com/), crucial para o envio automatizado de emails.

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

> *As descrições a seguir das variáveis foram deduzidas a partir de seus nomes e também por rápida lida do código e documentações. Favor melhorem ou corrija-as para uma maior precisão.*
#### Variáveis relacionadas ao SGBD
- `DB_DRIVERNAME` - Nome do SGBD a ser utilizado. Para mais detalhes, [clique aqui](https://docs.sqlalchemy.org/en/20/core/engines.html#backend-specific-urls).
- `DB_USERNAME` e `DB_PASSWORD` - Nome de usuário e senha registrados no SGBD.
- `DB_HOST` e `DB_PORT` - Endereço e porta onde o SGBD está hospedado
- `DB_DATABASE` - Nome do banco de dados a ser utilizado pelo projeto.

#### Variáveis relacionadas ao SendGrid
- `SENDGRID_API_KEY` - Chave API da aplicação no SendGrid.
- `SENDGRID_EMAIL` - Email da sua conta no SendGrid.

#### Variáveis relacionadas a execução da aplicação
- `SECRET_KEY` - Chave aleatória a ser utilizada pela aplicação (*favor espacificar mais detalhes de como deve ser essa chave (tamanho em bits, padrão, etc)*)
- `ALGORITHM` - *Pesteíssu?*
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Duração em minutos dos tokens gerados para o sistema de login<del>, eu acho</del>.

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
make add-dependency DEPNAME="<nome_da_dependencia>"
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