from datetime import datetime
from typing import List

from fastapi import Depends
from loguru import logger
from passlib.context import CryptContext
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.tarefa import Tarefa
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.alunos.errors import (
    AlunoNaoEncontradoException,
    CPFAlreadyRegisteredException,
    MatriculaJaRegistradaException,
    NumeroJaRegistradoException,
    OrientadorNaoEncontradoException,
)
from src.api.entrypoints.alunos.schema import AlunoBase, AlunoCreate, AlunoInDB
from src.api.services.auth import ServiceAuth, oauth2_scheme
from src.api.services.solicitacao import ServicoSolicitacao
from src.api.services.usuario import ServiceUsuario
from src.api.services.usuario_tipo_base import ServicoBase

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ServicoAluno(ServicoBase):
    @staticmethod
    def buscar_atual(db: Session, token: str = Depends(oauth2_scheme)) -> AlunoInDB:
        logger.info("Buscando aluno atual.")
        email = ServiceAuth.verificar_token(token)
        logger.info("Token verificado com sucesso.")
        db_aluno: Aluno = ServicoAluno.obter_por_email(db, email)
        logger.info("Aluno encontrado com sucesso.")
        return ServicoAluno.de_aluno_para_aluno_in_db(db_aluno)

    @staticmethod
    def validar_novo_aluno(db: Session, aluno: AlunoBase) -> None:
        logger.info("Validando novo aluno.")
        if db.query(Aluno).filter_by(cpf=aluno.cpf).first():
            raise CPFAlreadyRegisteredException()
        if db.query(Aluno).filter_by(telefone=aluno.telefone).first():
            raise NumeroJaRegistradoException()
        if (
            not aluno.orientador_id
            or not db.query(Professor).filter_by(id=aluno.orientador_id).first()
        ):
            raise OrientadorNaoEncontradoException()
        if db.query(Aluno).filter_by(matricula=aluno.matricula).first():
            raise MatriculaJaRegistradaException()

    @staticmethod
    def validar_atualizar_aluno(db: Session, aluno_id: int, aluno):
        if (
            aluno.get("orientador_id")
            and not db.query(Professor).filter_by(id=aluno.get("orientador_id")).first()
        ):
            raise OrientadorNaoEncontradoException()

        if (
            aluno.get("telefone")
            and db.query(Aluno)
            .filter(
                and_(
                    not_(Aluno.id == aluno_id), Aluno.telefone == aluno.get("telefone")
                )
            )
            .one_or_none()
        ):
            raise NumeroJaRegistradoException()

    @staticmethod
    def criar(db: Session, novo_aluno: AlunoCreate) -> AlunoInDB:
        ServicoAluno.validar_novo_aluno(db, novo_aluno)

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
        db.add(db_aluno)
        db.commit()
        db.refresh(db_aluno)
        logger.info("Aluno criado com sucesso.")
        ServicoSolicitacao.criar(db, db_aluno.id, db_aluno.orientador_id)
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
    def obter_aluno(db: Session, aluno_id: int) -> AlunoInDB:
        aluno: Aluno = PGCopRepository.obter_por_id(db, aluno_id, Aluno)
        if not aluno:
            raise AlunoNaoEncontradoException()
        return ServicoAluno.de_aluno_para_aluno_in_db(aluno)

    @staticmethod
    def atualizar_aluno(db: Session, aluno_id: int, updates) -> AlunoInDB:
        ServicoAluno.validar_atualizar_aluno(db, aluno_id, updates)
        db_aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not db_aluno:
            raise AlunoNaoEncontradoException()

        db_aluno = db.query(Aluno).filter_by(id=aluno_id).one_or_none()
        if not db_aluno:
            raise AlunoNaoEncontradoException()
        for key, value in updates.items():
            setattr(db_aluno, key, value)
        db.commit()
        db.refresh(db_aluno)
        return AlunoInDB(**db_aluno.__dict__)

    @staticmethod
    def deletar(db: Session, aluno_id: int) -> None:
        aluno: Aluno = PGCopRepository.obter_por_id(db, aluno_id, Aluno)
        tarefas: list[Tarefa] = aluno.tarefas or []
        for tarefa in tarefas:
            tarefa.deleted_at = datetime.now()
        aluno.deleted_at = datetime.now()
        aluno.usuario.deleted_at = datetime.now()
        db.commit()

    @staticmethod
    def obter_alunos_por_orientador(db: Session, orientador_id: int) -> List[AlunoInDB]:
        alunos: List[Aluno] = PGCopRepository.obter_todos_orientandos_de_um_professor(
            db, orientador_id
        )
        return [ServicoAluno.de_aluno_para_aluno_in_db(aluno) for aluno in alunos]

    @staticmethod
    def obter_por_email(db: Session, email: str) -> Aluno:
        db_aluno: Aluno = PGCopRepository.obter_aluno_por_email(db, email)
        if db_aluno is None:
            raise AlunoNaoEncontradoException()
        return db_aluno

    @staticmethod
    def obter_aluno_por_cpf(db: Session, cpf: str) -> AlunoInDB:
        db_aluno = PGCopRepository.obter_aluno_por_cpf(db, cpf)
        if db_aluno is None:
            raise AlunoNaoEncontradoException()
        return ServicoAluno.de_aluno_para_aluno_in_db(db_aluno)
