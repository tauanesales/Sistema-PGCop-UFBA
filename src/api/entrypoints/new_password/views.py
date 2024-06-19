from fastapi import APIRouter, Depends, status

from src.api.database.session import get_repo
from src.api.entrypoints.new_password.schema import (
    NovaSenhaAtualizada,
    NovaSenhaCodigoAutenticacao,
    NovaSenhaSolicitada,
)
from src.api.services.nova_senha import ServicoNovaSenha

router = APIRouter()


@router.post("/", status_code=status.HTTP_200_OK)
async def set_new_password(
    request: NovaSenhaAtualizada, repository=Depends(get_repo())
):
    await ServicoNovaSenha(repository).atualizar_para_nova_senha(
        request.email, request.senha, request.token
    )


@router.post("/auth", status_code=status.HTTP_200_OK)
async def authenticate(
    request: NovaSenhaCodigoAutenticacao, repository=Depends(get_repo())
):
    await ServicoNovaSenha(repository).autenticar_usuario_com_token(
        request.email, request.token
    )


@router.post("/create_token", status_code=status.HTTP_201_CREATED)
async def create_token(request: NovaSenhaSolicitada, repository=Depends(get_repo())):
    await ServicoNovaSenha(repository).create_token(request.email)
