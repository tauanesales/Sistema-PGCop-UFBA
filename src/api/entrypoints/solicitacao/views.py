from loguru import logger
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer

from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.solicitacao.schema import SolicitacaoInDB
from src.api.services.solicitacao import ServicoSolicitacao
from src.api.services.tipo_usuario import ServicoTipoUsuario
from src.api.utils.enums import StatusSolicitacaoEnum
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get(
    "/{status}/{professor_id}",
    response_model=list[SolicitacaoInDB],
    status_code=status.HTTP_200_OK,
)
async def listar_solicitacoes(
    professor_id: int, status: StatusSolicitacaoEnum, repository=Depends(get_repo())
):
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
    token: str = Depends(oauth2_scheme)
):
    logger.info(f"Atualização da solicitação de id {solicitacao_id} | Autenticando usuário atual.")
    coordenador: Professor = await ServicoTipoUsuario(repository).buscar_usuario_atual(token=token)
    logger.info(
        f"{solicitacao_id=} {coordenador.id=} | "
        f"Tipo usuário atual é {coordenador.usuario.tipo_usuario.titulo}."
    )
    if (coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.COORDENADOR) and (coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.PROFESSOR):
        raise NaoAutorizadoException()
    return await ServicoSolicitacao(repository).atualizar_status_solicitacao(
        solicitacao_id=solicitacao_id, status=status
    )
