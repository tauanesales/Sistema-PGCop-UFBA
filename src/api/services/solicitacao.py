from loguru import logger
from sqlalchemy.orm import Session

from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.solicitacao.schema import SolicitacaoInDB
from src.api.utils.enums import StatusSolicitacaoEnum


class ServicoSolicitacao:
    @staticmethod
    def criar(db: Session, aluno_id, professor_id) -> SolicitacaoInDB:
        db_solicitacao: Solicitacao = Solicitacao(
            aluno_id=aluno_id,
            professor_id=professor_id,
            status=StatusSolicitacaoEnum.PENDENTE,
        )
        db.add(db_solicitacao)
        db.commit()
        logger.info(f"Solicitação para {aluno_id=} criada com sucesso.")
        db.refresh(db_solicitacao)
        return ServicoSolicitacao.de_solicitacao_para_solicitacao_in_db(db_solicitacao)

    @staticmethod
    def listar(
        db: Session, professor_id: int, status: StatusSolicitacaoEnum
    ) -> list[SolicitacaoInDB]:
        solicitacoes: list[
            Solicitacao
        ] = PGCopRepository.obter_lista_de_solicitacoes_de_professor(
            db, professor_id=professor_id, status=status
        )
        logger.info(
            f"Solicitacoes para {professor_id=} listadas \
                 com sucesso. Total: {len(solicitacoes)}."
        )
        return [
            ServicoSolicitacao.de_solicitacao_para_solicitacao_in_db(solicitacao)
            for solicitacao in solicitacoes
        ]

    @staticmethod
    def de_solicitacao_para_solicitacao_in_db(
        db_solicitacao: Solicitacao,
    ) -> SolicitacaoInDB:
        return SolicitacaoInDB(
            id=db_solicitacao.id,
            aluno_id=db_solicitacao.aluno_id,
            nome_aluno=db_solicitacao.aluno.usuario.nome,
            professor_id=db_solicitacao.professor_id,
            nome_professor=db_solicitacao.professor.usuario.nome,
            status=db_solicitacao.status,
        )

    def atualizar_status_solicitacao(
        db: Session, solicitacao_id: int, status: StatusSolicitacaoEnum
    ) -> SolicitacaoInDB:
        db_solicitacao: Solicitacao = PGCopRepository.obter_por_id(
            db, solicitacao_id, Solicitacao
        )
        db_solicitacao.status = status
        db.commit()
        db.refresh(db_solicitacao)
        logger.info(
            f"Solicitação {solicitacao_id=} atualizada com sucesso para \
                  {db_solicitacao.status}."
        )
        return ServicoSolicitacao.de_solicitacao_para_solicitacao_in_db(db_solicitacao)
