from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.session import get_repo
from src.api.entrypoints.solicitacao.schema import SolicitacaoInDB
from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.services.solicitacao import ServicoSolicitacao
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
from src.api.utils.enums import StatusSolicitacaoEnum, TipoUsuarioEnum

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/{status}/{professor_id}",
    response_model=list[SolicitacaoInDB],
    status_code=status.HTTP_200_OK,
)
async def listar_solicitacoes(
    professor_id: int,
    status: StatusSolicitacaoEnum,
    token: str = Depends(oauth2_scheme),
    repository=Depends(get_repo()),
):
    logger.info(
        f"Solicitada listagem de solicitações pelo professor com id {professor_id}"
        f" | Autenticando usuário atual."
    )
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)
    logger.info(
        f"{professor_id=} {professor.id=} | "
        f"Tipo usuário atual é {professor.usuario.tipo_usuario.titulo}."
    )
    if professor.usuario.tipo_usuario.titulo not in [
        TipoUsuarioEnum.COORDENADOR,
        TipoUsuarioEnum.PROFESSOR,
    ]:
        raise NaoAutorizadoException()
    return await ServicoSolicitacao(repository).listar(
        professor_id=professor_id, status=status
    )


@router.put(
    "/{solicitacao_id}", response_model=SolicitacaoInDB, status_code=status.HTTP_200_OK
)
async def atualizar_status_solicitacao(
    solicitacao_id: int,
    status: StatusSolicitacaoEnum,
    repository=Depends(get_repo()),
    token: str = Depends(oauth2_scheme),
):
    logger.info(
        f"Atualização da solicitação de id {solicitacao_id}"
        f" | Autenticando usuário atual."
    )
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)
    db_solicitacao: Solicitacao = await ServicoSolicitacao(
        repository
    ).buscar_solicitacao_por_id(solicitacao_id)
    logger.info(
        f"{solicitacao_id=} {professor.id=} | "
        f"Tipo usuário atual é {professor.usuario.tipo_usuario.titulo}."
    )
    logger.info(
        f"{professor.id=} {db_solicitacao.professor_id=} | "
        f"Tipo usuário atual é {professor.usuario.tipo_usuario.titulo}."
    )
    if professor.usuario.tipo_usuario.titulo not in [
        TipoUsuarioEnum.COORDENADOR,
        TipoUsuarioEnum.PROFESSOR,
    ]:
        raise NaoAutorizadoException()
    elif professor.id != db_solicitacao.professor_id:
        raise NaoAutorizadoException()
    return await ServicoSolicitacao(repository).atualizar_status_solicitacao(
        solicitacao_id=solicitacao_id, status=status
    )
