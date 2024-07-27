from typing import Optional

from loguru import logger

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.tarefa import Tarefa
from src.api.database.models.usuario import Usuario
from src.api.database.repository import PGCopRepository
from src.api.entrypoints.alunos.schema import AlunoAtualizado, AlunoBase
from src.api.entrypoints.new_password.errors import (
    AuthenticationException,
    EmailNotFoundException,
)
from src.api.entrypoints.professores.errors import ProfessorNaoEncontradoException
from src.api.entrypoints.professores.schema import ProfessorAtualizado
from src.api.entrypoints.tarefas.errors import ExcecaoTarefaNaoEncontrada
from src.api.exceptions.http_service_exception import (
    AlteracaoStatusSolicitacaoException,
    AlunoNaoEncontradoException,
    CadastroSemOrientadorNaoEncontradoException,
    CPFJaRegistradoException,
    DeveSeSubmeterPeloMenosUmCampoParaAtualizarException,
    EmailJaRegistradoException,
    MatriculaJaRegistradaException,
    NumeroJaRegistradoException,
    OrientadorDeveSerInformadoException,
    OrientadorNaoEncontradoException,
    TipoUsuarioInvalidoException,
    UsuarioNaoEncontradoException,
)
from src.api.schemas.usuario import UsuarioBase
from src.api.utils import constantes
from src.api.utils.enums import StatusSolicitacaoEnum, TipoUsuarioEnum


class ServicoValidador:
    def __init__(self, repository: PGCopRepository):
        self._repo: PGCopRepository = repository

    def validar_professor_existe(self, db_professor: Optional[Professor]):
        if db_professor is None:
            raise ProfessorNaoEncontradoException()

    def validar_campos_de_atualizacao_nao_sao_nulos(
        self, updates_professor: ProfessorAtualizado
    ):
        if not any(updates_professor.model_dump().values()):
            raise DeveSeSubmeterPeloMenosUmCampoParaAtualizarException()

    def validar_tipo_usuario(
        self, tipo_usuario: TipoUsuarioEnum, *tipos_permitidos: list[TipoUsuarioEnum]
    ):
        if tipo_usuario and tipo_usuario not in tipos_permitidos:
            raise TipoUsuarioInvalidoException()

    async def validar_email_nao_esta_em_uso(
        self,
        email: str,
        usuario_id,
    ):
        if await self._repo.buscar_usuario_por_email_excluindo_id(email, usuario_id):
            raise EmailJaRegistradoException()

    async def validar_atualizacao_de_professor(
        self,
        professor_id: int,
        updates_professor: ProfessorAtualizado,
        db_professor: Professor,
    ):
        self.validar_professor_existe(db_professor)
        logger.info(f"{professor_id=} | Professor encontrado no banco de dados.")
        self.validar_campos_de_atualizacao_nao_sao_nulos(updates_professor)
        logger.info(f"{professor_id=} | Existem campos não nulos para atualizar.")
        self.validar_tipo_usuario(
            updates_professor.tipo_usuario,
            TipoUsuarioEnum.PROFESSOR,
            TipoUsuarioEnum.COORDENADOR,
        )
        logger.info(f"{professor_id=} | Tipo usuário válido.")
        await self.validar_email_nao_esta_em_uso(
            db_professor.usuario.email, db_professor.usuario.id
        )
        logger.info(f"{professor_id=} | Email não está em uso.")

    async def validar_email_registrado(
        self,
        usuario: UsuarioBase,
    ) -> None:
        if await self._repo.buscar_usuario_por_email(usuario.email):
            raise EmailJaRegistradoException()

    def validar_usuario_existe(self, db_usuario: Optional[Usuario]):
        if db_usuario is None:
            raise UsuarioNaoEncontradoException()

    async def buscar_e_validar_outro_aluno_possui_telefone(
        self,
        telefone: Optional[str],
        aluno_id: int,
    ):
        if not telefone:
            return
        if await self._repo.buscar_aluno_por_telefone_excluindo_id(telefone, aluno_id):
            raise NumeroJaRegistradoException()

    async def buscar_e_validar_professor_existe(
        self,
        professor_id: int,
    ):
        if not professor_id:
            return
        professor: Optional[Professor] = await self._repo.buscar_por_id(
            professor_id,
            Professor,
        )
        self.validar_professor_existe(professor)

    def validar_aluno_existe(self, db_aluno: Optional[Aluno]):
        if db_aluno is None:
            raise AlunoNaoEncontradoException()

    async def validar_atualizacao_de_aluno(
        self,
        aluno_id: int,
        aluno_atualizado: AlunoAtualizado,
        db_aluno: Aluno,
    ):
        self.validar_aluno_existe(db_aluno)
        await self.buscar_e_validar_outro_aluno_possui_telefone(
            aluno_atualizado.telefone, aluno_id
        )
        await self.buscar_e_validar_professor_existe(aluno_atualizado.orientador_id)
        await self.validar_email_nao_esta_em_uso(
            aluno_atualizado.email, db_aluno.usuario.id
        )
        self.validar_tipo_usuario(aluno_atualizado.tipo_usuario, TipoUsuarioEnum.ALUNO)

    async def validar_novo_aluno(self, aluno: AlunoBase) -> None:
        logger.info("Validando novo aluno.")
        if await self._repo.buscar_aluno_por_cpf(aluno.cpf):
            raise CPFJaRegistradoException()
        if await self._repo.buscar_aluno_por_telefone(aluno.telefone):
            raise NumeroJaRegistradoException()
        if not aluno.orientador_id:
            raise OrientadorDeveSerInformadoException()
        if not await self._repo.buscar_por_id(aluno.orientador_id, Professor):
            raise OrientadorNaoEncontradoException()
        if not await self._repo.buscar_por_id(constantes.SEM_ORIENTADOR, Professor):
            raise CadastroSemOrientadorNaoEncontradoException()
        if await self._repo.buscar_aluno_por_matricula(aluno.matricula):
            raise MatriculaJaRegistradaException()

    async def buscar_e_validar_aluno_existe(self, aluno_id: int):
        db_aluno = await self._repo.buscar_por_id(aluno_id, Aluno)
        if db_aluno is None:
            raise AlunoNaoEncontradoException()

    async def buscar_e_validar_tarefa_existe(self, tarefa_id: int):
        db_tarefa = await self._repo.buscar_por_id(tarefa_id, Tarefa)
        if db_tarefa is None:
            raise ExcecaoTarefaNaoEncontrada()

    def validar_email_nao_encontrado(self, db_usuario: Optional[Usuario]):
        if db_usuario is None:
            raise EmailNotFoundException()

    def validar_usuario_autenticado_por_usuario(self, db_usuario: Optional[Usuario]):
        if not db_usuario:
            raise AuthenticationException()

    def validar_usuari_autenticado_por_token(self, db_usuario: Usuario, token: str):
        if db_usuario.token_nova_senha != token:
            raise AuthenticationException()

    async def buscar_e_validar_alteracao_status_solicitacao(self, db_solicitacao: Solicitacao):
        if db_solicitacao.status != StatusSolicitacaoEnum.PENDENTE:
            raise AlteracaoStatusSolicitacaoException()
