from datetime import datetime
from typing import List

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy import and_, not_
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.tarefa import Tarefa
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.exceptions.http_service_exception import (
    AlunoNaoEncontradoException,
    CPFJaRegistradoException,
    MatriculaJaRegistradaException,
    NumeroJaRegistradoException,
    OrientadorNaoEncontradoException,
)
from src.api.entrypoints.alunos.schema import AlunoBase, AlunoNovo, AlunoInDB, AlunoAtualizado
from src.api.services.auth import ServiceAuth, oauth2_scheme
from src.api.services.solicitacao import ServicoSolicitacao
from src.api.services.usuario import ServiceUsuario
from src.api.services.usuario_tipo_base import ServicoBase
from src.api.services.validador import ServicoValidador

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoAluno(ServicoBase):
    @staticmethod
    async def buscar_atual(db: AsyncSession, token: str = Depends(oauth2_scheme)) -> AlunoInDB:
        logger.info("Buscando aluno atual.")
        email = ServiceAuth.verificar_token(token)
        logger.info("Token verificado com sucesso.")
        db_aluno: Aluno = await ServicoAluno.obter_por_email(db, email)
        logger.info("Aluno encontrado com sucesso.")
        return ServicoAluno.de_aluno_para_aluno_in_db(db_aluno)

    @staticmethod
    async def validar_novo_aluno(db: AsyncSession, aluno: AlunoBase) -> None:
        logger.info("Validando novo aluno.")
        if await PGCopRepository.buscar_aluno_por_cpf(db, aluno.cpf):
            raise CPFJaRegistradoException()
        if await PGCopRepository.buscar_aluno_por_telefone(db, aluno.telefone):
            raise NumeroJaRegistradoException()
        if (
            not aluno.orientador_id
            or not db.query(Professor).filter_by(id=aluno.orientador_id).first()
        ):
            raise OrientadorNaoEncontradoException()
        if db.query(Aluno).filter_by(matricula=aluno.matricula).first():
            raise MatriculaJaRegistradaException()



    @staticmethod
    async def criar(db: AsyncSession, novo_aluno: AlunoNovo) -> AlunoInDB:
        await ServicoAluno.validar_novo_aluno(db, novo_aluno)

        db_usuario_aluno: Usuario = ServiceUsuario.criar(db, novo_aluno)
        logger.info("Criando aluno.")
        db_aluno = Aluno(
            cpf=novo_aluno.cpf,
            telefone=novo_aluno.telefone,
            matricula=novo_aluno.matricula,
            lattes=novo_aluno.lattes,
            curso=novo_aluno.curso,
            data_ingresso=novo_aluno.data_ingresso,
            data_qualificacao=novo_aluno.data_qualificacao,
            data_defesa=novo_aluno.data_defesa,
            orientador_id=novo_aluno.orientador_id,
            usuario=db_usuario_aluno,
        )
        await db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)
        logger.info("Aluno criado com sucesso.")
        await ServicoSolicitacao.criar(db, db_aluno.id, db_aluno.orientador_id)
        return ServicoAluno.de_aluno_para_aluno_in_db(db_aluno)

    def de_aluno_para_aluno_in_db(db_aluno: Aluno) -> AlunoInDB:
        return AlunoInDB(
            nome=db_aluno.usuario.nome,
            email=db_aluno.usuario.email,
            tipo_usuario=db_aluno.usuario.tipo_usuario.titulo,
            id=db_aluno.id,
            cpf=db_aluno.cpf,
            telefone=db_aluno.telefone,
            matricula=db_aluno.matricula,
            lattes=db_aluno.lattes,
            curso=db_aluno.curso,
            data_ingresso=db_aluno.data_ingresso,
            data_qualificacao=db_aluno.data_qualificacao,
            data_defesa=db_aluno.data_defesa,
            orientador_id=db_aluno.orientador_id,
        )

    @staticmethod
    async def obter_aluno(db: AsyncSession, aluno_id: int) -> AlunoInDB:
        aluno: Aluno = await PGCopRepository.buscar_por_id(db, aluno_id, Aluno)
        ServicoValidador.validar_aluno_existe(aluno)
        return ServicoAluno.de_aluno_para_aluno_in_db(aluno)

    @staticmethod
    async def atualizar_aluno(db: AsyncSession, aluno_id: int, aluno_atualizado: AlunoAtualizado) -> AlunoInDB:
        db_aluno: Aluno = await PGCopRepository.buscar_por_id(db, aluno_id, Aluno)
        await ServicoValidador.validar_atualizacao_de_aluno(db, aluno_id, aluno_atualizado, db_aluno)
        
        db_aluno.cpf = aluno_atualizado.cpf or db_aluno.cpf
        db_aluno.telefone = aluno_atualizado.telefone or db_aluno.telefone
        db_aluno.matricula = aluno_atualizado.matricula or db_aluno.matricula
        db_aluno.lattes = aluno_atualizado.lattes or db_aluno.lattes
        db_aluno.curso = aluno_atualizado.curso or db_aluno.curso
        db_aluno.data_ingresso = aluno_atualizado.data_ingresso or db_aluno.data_ingresso
        db_aluno.data_qualificacao = aluno_atualizado.data_qualificacao or db_aluno.data_qualificacao
        db_aluno.data_defesa = aluno_atualizado.data_defesa or db_aluno.data_defesa
        db_aluno.orientador_id = aluno_atualizado.orientador_id or db_aluno.orientador_id
        db_aluno.usuario.nome = aluno_atualizado.nome or db_aluno.usuario.nome
        db_aluno.usuario.email = aluno_atualizado.email or db_aluno.usuario.email
        db_aluno.usuario.senha_hash = (
            pwd_context.hash(aluno_atualizado.senha)
            if aluno_atualizado.senha
            else db_aluno.usuario.senha_hash
        )
        db.commit()
        db.refresh(db_aluno)
        return ServicoAluno.de_aluno_para_aluno_in_db(db_aluno)

    @staticmethod
    async def deletar(db: AsyncSession, aluno_id: int) -> None:
        aluno: Aluno = await PGCopRepository.buscar_por_id(db, aluno_id, Aluno)
        tarefas: list[Tarefa] = aluno.tarefas or []
        for tarefa in tarefas:
            tarefa.deleted_at = datetime.now()
        aluno.deleted_at = datetime.now()
        aluno.usuario.deleted_at = datetime.now()
        db.commit()

    @staticmethod
    async def obter_alunos_por_orientador(db: AsyncSession, orientador_id: int) -> List[AlunoInDB]:
        alunos: List[Aluno] = await PGCopRepository.buscar_todos_orientandos_de_um_professor(
            db, orientador_id
        )
        return [ServicoAluno.de_aluno_para_aluno_in_db(aluno) for aluno in alunos]

    @staticmethod
    async def obter_por_email(db: AsyncSession, email: str) -> Aluno:
        db_aluno: Aluno = await PGCopRepository.buscar_aluno_por_email(db, email)
        ServicoValidador.validar_aluno_existe(db_aluno)
        return db_aluno

    @staticmethod
    async def obter_aluno_por_cpf(db: AsyncSession, cpf: str) -> AlunoInDB:
        db_aluno = await PGCopRepository.buscar_aluno_por_cpf(db, cpf)
        ServicoValidador.validar_aluno_existe(db_aluno)
        return ServicoAluno.de_aluno_para_aluno_in_db(db_aluno)
