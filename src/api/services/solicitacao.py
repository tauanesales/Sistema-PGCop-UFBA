from loguru import logger

from src.api.database.models.aluno import Aluno
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.solicitacao.schema import SolicitacaoInDB
from src.api.exceptions.value_error_validation_exception import InvalidOrientadorError
from src.api.services.servico_base import ServicoBase
from src.api.utils.constantes import SEM_ORIENTADOR
from src.api.utils.enums import StatusSolicitacaoEnum


class ServicoSolicitacao(ServicoBase):
    _repo: PGCopRepository

    async def criar(self, aluno: Aluno, professor_id: int) -> SolicitacaoInDB:
        db_solicitacao: Solicitacao = Solicitacao(
            status=StatusSolicitacaoEnum.PENDENTE,
            aluno_id=aluno.id,
            professor_id=professor_id,
        )

        if professor_id == SEM_ORIENTADOR:
            raise InvalidOrientadorError()

        await self._repo.criar(db_solicitacao)
        logger.info(f"{db_solicitacao.id=} | Solicitação para criada com sucesso.")
        return self.de_solicitacao_para_solicitacao_in_db(db_solicitacao)

    async def listar(
        self, professor_id: int, status: StatusSolicitacaoEnum
    ) -> list[SolicitacaoInDB]:
        solicitacoes: list[
            Solicitacao
        ] = await self._repo.buscar_lista_de_solicitacoes_de_professor(
            professor_id=professor_id, status=status
        )
        logger.info(
            f"Solicitacoes para {professor_id=} listadas \
                 com sucesso. Total: {len(solicitacoes)}."
        )
        return [
            self.de_solicitacao_para_solicitacao_in_db(solicitacao)
            for solicitacao in solicitacoes
        ]

    def de_solicitacao_para_solicitacao_in_db(
        self,
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

    async def atualizar_status_solicitacao(
        self, solicitacao_id: int, status: StatusSolicitacaoEnum
    ) -> SolicitacaoInDB:
        db_solicitacao: Solicitacao = await self._repo.buscar_por_id(
            solicitacao_id, Solicitacao
        )

        if db_solicitacao.professor_id == SEM_ORIENTADOR:
            raise InvalidOrientadorError()

        db_solicitacao.status = status
        self._repo.salvar(db_solicitacao)
        logger.info(
            f"Solicitação {solicitacao_id=} atualizada com sucesso para \
                  {db_solicitacao.status}."
        )

        if status == StatusSolicitacaoEnum.ACEITA:
            await self.atualizar_orientador_aluno(
                db_solicitacao.aluno_id, db_solicitacao.professor_id
            )

        return self.de_solicitacao_para_solicitacao_in_db(db_solicitacao)

    async def atualizar_orientador_aluno(
        self, aluno_id: int, orientador_id: int
    ) -> None:
        db_aluno: Aluno = await self._repo.buscar_por_id(aluno_id, Aluno)
        db_aluno.orientador_id = orientador_id
        logger.info(f"Atribuição de orientador para {db_aluno.id=}.")
