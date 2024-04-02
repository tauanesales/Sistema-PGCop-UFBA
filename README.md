﻿# Back-End: Sistema de Monitoramento de Alunos do PGCOMP-UFBA
Projeto da disciplina: MATE85 - Tópicos em Sistemas de Informacao e Web I
 
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

**Instale as bibliotecas necessárias para rodar o projeto**
```bash
pip install -r requirements.txt 
```

**Inicialize o servidor API com o comando**
```bash
uvicorn src.api.app:get_app
```

### Links:
- [Aplicação em Produção](https://back-mate-85-topicos-em-sistemas-de-informacao-e-web-i.vercel.app/)
- [Gestão do Projeto (Jira)](https://taysales6.atlassian.net/jira/software/projects/KAN/boards/1?atlOrigin=eyJpIjoiNTY5MGQyZmVhOTMwNDJiYjhkMmJjY2NjNjhmYWYwYmIiLCJwIjoiaiJ9)
