from datetime import datetime
from typing import Optional
from fastapi_cache.decorator import cache

from loguru import logger

from src.api.config import Config
from src.api.database.models.tarefas_base import TarefaBase
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.tarefas_base.errors import ExcecaoTarefaNaoEncontrada
from src.api.entrypoints.tarefas_base.schema import (
    TarefaBaseAtualizada,
    TarefaBaseBase,
    TarefaBaseInDB,
)
from src.api.services.servico_base import ServicoBase


class ServiceTarefaBase(ServicoBase):
    _repo: PGCopRepository

    async def criar_tarefa_base(self, tarefa: TarefaBaseBase):
        db_tarefa_base = TarefaBase(
            nome=tarefa.nome,
            descricao=tarefa.descricao,
            prazo_em_meses=tarefa.prazo_em_meses,
            curso=tarefa.curso,
        )
        await self._repo.criar(db_tarefa_base)

        return db_tarefa_base

    async def atualizar_tarefa_base(
        self, tarefa_id: int, tarefa_base_atualizada: TarefaBaseAtualizada
    ):
        logger.info(
            f"{tarefa_id=} | Iniciando processo de atualização de tarefa base. \
            Validando informações. {tarefa_base_atualizada.model_dump()=}"
        )
        db_tarefa_base: TarefaBase = await self.buscar_tarefa_base(tarefa_id)
        to_update = tarefa_base_atualizada.model_dump()
        for key, value in list(to_update.items())[::-1]:
            if value is None:
                to_update.pop(key)
        await self._repo.atualizar_por_id(tarefa_id, TarefaBase, **to_update)
        return self.de_tarefa_base_para_tarefa_base_in_db(db_tarefa_base)

    async def deletar_tarefa_base(self, tarefa_base_id: int) -> None:
        logger.info(
            f"{tarefa_base_id=} | Iniciando processo de deleção de tarefa base."
        )
        db_tarefa_base = await self.buscar_tarefa_base(tarefa_base_id)
        db_tarefa_base.deleted_at = datetime.utcnow()
        logger.info(f"{tarefa_base_id=} | Tarefa base deletada.")

    async def buscar_tarefa_base(self, tarefa_base_id: int) -> TarefaBase:
        logger.info(f"{tarefa_base_id=} | Pesquisando por tarefa base.")
        db_tarefa_base: Optional[TarefaBase] = await self._repo.buscar_por_id(
            tarefa_base_id, TarefaBase
        )
        if not db_tarefa_base:
            raise ExcecaoTarefaNaoEncontrada()
        logger.info(f"{tarefa_base_id=} | Tarefa base encontrada.")
        return db_tarefa_base

    @cache(expire=60 * Config.MINUTOS_DE_CACHE_REQUISICOES)
    async def buscar_tarefas_base_por_curso(self, curso: str) -> list[TarefaBaseInDB]:
        logger.info(f"{curso=} | Pesquisando por tarefas base por curso.")
        db_tarefas_base: list[TarefaBase] = await self._repo.filtrar(
            TarefaBase, curso=curso, deleted_at=None
        )
        return [
            self.de_tarefa_base_para_tarefa_base_in_db(tarefa)
            for tarefa in db_tarefas_base
        ]

    def de_tarefa_base_para_tarefa_base_in_db(
        self, tarefa: TarefaBase
    ) -> TarefaBaseInDB:
        return TarefaBaseInDB(
            id=tarefa.id,
            nome=tarefa.nome,
            descricao=tarefa.descricao,
            prazo_em_meses=tarefa.prazo_em_meses,
            curso=tarefa.curso,
        )
