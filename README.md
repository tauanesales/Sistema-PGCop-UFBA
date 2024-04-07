# Back-End: Sistema de Monitoramento de Alunos do PGCOMP-UFBA
Projeto da disciplina: MATE85 - Tópicos em Sistemas de Informação e Web I
 
## Tabela de Conteúdos:
- [Sobre o Projeto](#sobre-o-projeto)
- [Autores](#autores)
- [Linguagem e Tecnologias](#linguagem-e-tecnologias)
- [Arquitetura do Back-End](#arquitetura-do-back-end)
- [Getting Started](#getting-started)
- [Links](#links)

<hr>

## Sobre o Projeto:
Repositório com o back-end da aplicação do sistema de monitoramento de alunos do PGCOMP-UFBA — projeto relacionado à disciplina Tópicos em Sistemas de Informação Web I.

### Autores:
- Alex Lima
- Izak Alves Gama
- Jean Loui Bernard
- Mário Augusto
- Pedro Harzer
- Tauane Sales 

### Linguagem e Tecnologias:
- Python 3
- FastAPI
- SendGrid

### [Arquitetura do Back-End](./arquitetura_sistema.jpg)
A imagem abaixo mostra a arquitetura do lado back-end da aplicação. 
<img src="./arquitetura_sistema.jpg" width="80%"/>

## Getting Started:

1. **Clone o repositório do projeto**
```bash
git clone git@github.com:tauanesales\BACK-MATE85-Topicos-em-sistemas-de-informacao-e-web-i.git
```

2. **Acesse a pasta do projeto**
```bash
cd BACK-MATE85-Topicos-em-sistemas-de-informacao-e-web-i
```

3. **Instale as bibliotecas necessárias para rodar o projeto**
```bash
make install
```

4. **Crie um arquivo `.env` na raiz do projeto e adicione as variáveis de ambiente do `.env.sample`.**

5. **Inicialize o servidor com o comando**
```bash
make run
```

### Para o desenvolvedor

- **Para adicionar novas dependências ao projeto, rode o comando**
```bash
poetry add <nome_da_dependencia>
```

- **Sempre que adicionar novas dependencias, rode o comando abaixo**
```bash
make export-requirements
```

- **O deploy da aplicação é feito automaticamente pelo Vercel, após o merge na branch `main`.**

### Links:
- [Aplicação em Produção](https://back-mate-85-topicos-em-sistemas-de-informacao-e-web-i.vercel.app/)
- [Gestão do Projeto (Jira)](https://taysales6.atlassian.net/jira/software/projects/KAN/boards/1?atlOrigin=eyJpIjoiNTY5MGQyZmVhOTMwNDJiYjhkMmJjY2NjNjhmYWYwYmIiLCJwIjoiaiJ9)
- [Repositório do Front-End do Projeto](https://github.com/tauanesales/FRONT-MATE85-Topicos-em-sistemas-de-informacao-e-web-i)
