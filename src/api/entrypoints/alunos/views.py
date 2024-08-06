from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from loguru import logger

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.session import get_repo
from src.api.entrypoints.alunos.schema import AlunoInDB, AlunoNovo
from src.api.entrypoints.tarefas.schema import TarefaInDB
from src.api.exceptions.credentials_exception import NaoAutorizadoException
from src.api.services.aluno import ServicoAluno
from src.api.services.tipo_usuario import ServicoTipoUsuarioGenerico
from src.api.services.tarefa import ServiceTarefa
from src.api.utils.enums import TipoUsuarioEnum

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/", response_model=AlunoInDB, status_code=status.HTTP_201_CREATED)
async def criar_aluno(aluno: AlunoNovo, repository=Depends(get_repo())):
    return await ServicoAluno(repository).criar(aluno)


@router.get("/{aluno_id}", response_model=AlunoInDB)
async def get_aluno(aluno_id: int, repository=Depends(get_repo())):
    return await ServicoAluno(repository).buscar_dados_in_db_por_id(aluno_id)


@router.delete(
    "/{aluno_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
async def deletar_aluno_por_id(
    aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info(f"Solicitado deleção de {aluno_id=} | Autenticando usuário atual.")
    coordenador: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token, tipo_usuario=TipoUsuarioEnum.COORDENADOR)
    logger.info(
        f"{aluno_id=} {coordenador.id=} | "
        f"Tipo usuário atual é {coordenador.usuario.tipo_usuario.titulo}."
    )
    if coordenador.usuario.tipo_usuario.titulo != TipoUsuarioEnum.COORDENADOR:
        raise NaoAutorizadoException()
    return await ServicoAluno(repository).deletar(aluno_id)


@router.delete("/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def deletar_aluno_atual(
    token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    aluno: Aluno = await ServicoTipoUsuarioGenerico(repository).buscar_usuario_atual(
        token=token, tipo_usuario=TipoUsuarioEnum.ALUNO
    )
    return await ServicoAluno(repository).deletar(aluno.id)


@router.get("/cpf/{aluno_cpf}", response_model=AlunoInDB)
async def get_aluno_cpf(aluno_cpf: str, repository=Depends(get_repo()),token: str = Depends(oauth2_scheme)):
    professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)

    if professor.usuario.tipo_usuario.titulo not in [
        TipoUsuarioEnum.COORDENADOR,
        TipoUsuarioEnum.PROFESSOR,
    ]:
        raise NaoAutorizadoException()
    else:
        return await ServicoAluno(repository).buscar_aluno_por_cpf(aluno_cpf)


@router.get("/email/{aluno_email}", response_model=AlunoInDB)
async def get_aluno_email(aluno_email: str, repository=Depends(get_repo())):
    return await ServicoAluno(repository).buscar_dados_in_db_por_email(aluno_email)


@router.put("/{aluno_id}/remover-orientador/", response_model=AlunoInDB)
async def remover_orientador_aluno(
    aluno_id: int, token: str = Depends(oauth2_scheme), repository=Depends(get_repo())
):
    logger.info(
        f"Solicitado remoção do orientador do {aluno_id=} | Autenticando usuário atual."
    )
    coordenador_ou_professor: Professor = await ServicoTipoUsuarioGenerico(
        repository
    ).buscar_usuario_atual(token=token)
    logger.info(
        f"{aluno_id=} {coordenador_ou_professor.id=} | "
        f"Tipo usuário atual é {coordenador_ou_professor.usuario.tipo_usuario.titulo}."
    )
    if (
        coordenador_ou_professor.usuario.tipo_usuario.titulo
        != TipoUsuarioEnum.COORDENADOR
    ) and (
        coordenador_ou_professor.usuario.tipo_usuario.titulo
        != TipoUsuarioEnum.PROFESSOR
    ):
        raise NaoAutorizadoException()

    return await ServicoAluno(repository).remover_orientador(aluno_id)


@router.get("/tarefas", response_model=list[TarefaInDB])
async def get_tarefas_por_id(token: str = Depends(oauth2_scheme), repository=Depends(get_repo())):
    aluno: Aluno = await ServicoTipoUsuarioGenerico(repository).buscar_usuario_atual(
        token=token, tipo_usuario=TipoUsuarioEnum.ALUNO
    )
    return await ServiceTarefa(repository).buscar_tarefas_por_aluno(aluno.id)