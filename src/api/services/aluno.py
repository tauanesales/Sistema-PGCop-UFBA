from datetime import datetime
from typing import List

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.tarefa import Tarefa
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.alunos.schema import AlunoAtualizado, AlunoInDB, AlunoNovo
from src.api.entrypoints.professores.schema import ProfessorInDB
from src.api.services.auth import ServicoAuth, oauth2_scheme
from src.api.services.servico_base import ServicoBase
from src.api.services.solicitacao import ServicoSolicitacao
from src.api.services.usuario import ServicoUsuario

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoAluno(ServicoBase):
    _repo: PGCopRepository

    async def buscar_atual(self, token: str = Depends(oauth2_scheme)) -> AlunoInDB:
        logger.info("Buscando aluno atual.")
        email = await ServicoAuth(self._repo).verificar_token(token)
        logger.info("Token verificado com sucesso.")
        db_aluno: Aluno = await self.buscar_por_email(email)
        logger.info(f"{db_aluno.id=} | Aluno encontrado com sucesso.")
        return self.tipo_usuario_in_db(db_aluno)

    async def criar(self, novo_aluno: AlunoNovo) -> AlunoInDB:
        logger.info("Início do processo de criação de novo aluno.")
        await self._validador.validar_novo_aluno(novo_aluno)

        db_usuario_aluno: Usuario = await ServicoUsuario(self._repo).criar(novo_aluno)
        logger.info(f"{db_usuario_aluno.id=} | Usuário criado com sucesso.")
        db_orientador: Professor = await self._repo.buscar_por_id(
            novo_aluno.orientador_id, Professor
        )

        # logger.info(f"{db_orientador.id=} | Atribuição sem orientador realizada.")

        db_aluno = Aluno(
            cpf=novo_aluno.cpf,
            telefone=novo_aluno.telefone,
            matricula=novo_aluno.matricula,
            lattes=novo_aluno.lattes,
            curso=novo_aluno.curso,
            data_ingresso=novo_aluno.data_ingresso,
            data_qualificacao=novo_aluno.data_qualificacao,
            data_defesa=novo_aluno.data_defesa,
            orientador_id=db_orientador.id,
            orientador=db_orientador,
            usuario=db_usuario_aluno,
            usuario_id=db_usuario_aluno.id,
        )
        await self._repo.criar(db_aluno)
        logger.info(f"{db_aluno.id=} {db_orientador.id=} | Aluno criado com sucesso.")
        await ServicoSolicitacao(self._repo).criar(db_aluno, novo_aluno.orientador_id)
        return self.tipo_usuario_in_db(db_aluno)

    def tipo_usuario_in_db(self, db_aluno: Aluno) -> AlunoInDB:
        return AlunoInDB(
            id=db_aluno.id,
            usuario_id=db_aluno.usuario_id,
            nome=db_aluno.usuario.nome,
            email=db_aluno.usuario.email,
            tipo_usuario=db_aluno.usuario.tipo_usuario.titulo,
            cpf=db_aluno.cpf,
            telefone=db_aluno.telefone,
            matricula=db_aluno.matricula,
            lattes=db_aluno.lattes,
            curso=db_aluno.curso,
            data_ingresso=db_aluno.data_ingresso,
            data_qualificacao=db_aluno.data_qualificacao,
            data_defesa=db_aluno.data_defesa,
            orientador=ProfessorInDB(
                nome=db_aluno.orientador.usuario.nome,
                email=db_aluno.orientador.usuario.email,
                tipo_usuario=db_aluno.orientador.usuario.tipo_usuario.titulo,
                id=db_aluno.orientador.id,
            ),
        )

    async def buscar_aluno_por_id(self, aluno_id: int) -> Aluno:
        db_aluno: Aluno = await self._repo.buscar_por_id(aluno_id, Aluno)
        self._validador.validar_aluno_existe(db_aluno)
        return db_aluno

    async def atualizar(
        self, aluno_id: int, aluno_atualizado: AlunoAtualizado
    ) -> AlunoInDB:
        db_aluno: Aluno = await self._repo.buscar_por_id(aluno_id, Aluno)
        await self._validador.validar_atualizacao_de_aluno(
            aluno_id, aluno_atualizado, db_aluno
        )

        db_aluno.cpf = aluno_atualizado.cpf or db_aluno.cpf
        db_aluno.telefone = aluno_atualizado.telefone or db_aluno.telefone
        db_aluno.matricula = aluno_atualizado.matricula or db_aluno.matricula
        db_aluno.lattes = aluno_atualizado.lattes or db_aluno.lattes
        db_aluno.curso = aluno_atualizado.curso or db_aluno.curso
        db_aluno.data_ingresso = (
            aluno_atualizado.data_ingresso or db_aluno.data_ingresso
        )
        db_aluno.data_qualificacao = (
            aluno_atualizado.data_qualificacao or db_aluno.data_qualificacao
        )
        db_aluno.data_defesa = aluno_atualizado.data_defesa or db_aluno.data_defesa
        db_aluno.orientador_id = (
            aluno_atualizado.orientador_id or db_aluno.orientador_id
        )
        db_aluno.usuario.nome = aluno_atualizado.nome or db_aluno.usuario.nome
        db_aluno.usuario.email = aluno_atualizado.email or db_aluno.usuario.email
        db_aluno.usuario.senha_hash = (
            pwd_context.hash(aluno_atualizado.senha)
            if aluno_atualizado.senha
            else db_aluno.usuario.senha_hash
        )
        return self.tipo_usuario_in_db(db_aluno)

    async def deletar(self, aluno_id: int) -> None:
        logger.info(f"Deletando aluno {aluno_id=}")
        aluno: AlunoInDB = await self.buscar_aluno_por_id(aluno_id)
        tarefas: list[Tarefa] = aluno.tarefas or []
        logger.info(f"{aluno.id=} | Deleteando tarefas do aluno")
        for tarefa in tarefas:
            tarefa.deleted_at = datetime.utcnow()
        aluno.deleted_at = datetime.utcnow()
        aluno.usuario.deleted_at = datetime.utcnow()
        logger.info(f"{aluno.id=} | Aluno deletado com sucesso.")

    async def buscar_alunos_por_orientador(self, orientador_id: int) -> List[AlunoInDB]:
        alunos: List[Aluno] = await self._repo.buscar_todos_orientandos_de_um_professor(
            orientador_id
        )
        return [self.tipo_usuario_in_db(aluno) for aluno in alunos]

    async def buscar_por_email(self, email: str) -> Aluno:
        db_aluno: Aluno = await self._repo.buscar_aluno_por_email(email)
        self._validador.validar_aluno_existe(db_aluno)
        return db_aluno

    async def buscar_aluno_por_cpf(self, cpf: str) -> AlunoInDB:
        db_aluno = await self._repo.buscar_aluno_por_cpf(cpf)
        self._validador.validar_aluno_existe(db_aluno)
        return self.tipo_usuario_in_db(db_aluno)

    async def buscar_aluno_por_matricula(self, matricula: str) -> AlunoInDB:
        db_aluno = await self._repo.buscar_aluno_por_matricula(matricula)
        self._validador.validar_aluno_existe(db_aluno)
        return self.tipo_usuario_in_db(db_aluno)

    async def buscar_dados_in_db_por_id(self, aluno_id: int) -> AlunoInDB:
        return self.tipo_usuario_in_db(await self.buscar_aluno_por_id(aluno_id))

    async def buscar_dados_in_db_por_email(self, email: str) -> AlunoInDB:
        return self.tipo_usuario_in_db(await self.buscar_por_email(email))

    async def remover_orientador(self, aluno_id: int) -> AlunoInDB:
        db_aluno: Aluno = await self._repo.buscar_por_id(aluno_id, Aluno)
        db_aluno.orientador_id = 1

        return self.tipo_usuario_in_db(db_aluno)
