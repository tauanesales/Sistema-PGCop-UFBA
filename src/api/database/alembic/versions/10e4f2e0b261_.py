"""empty message

Revision ID: 10e4f2e0b261
Revises: ac61d214ad4e
Create Date: 2024-08-17 12:46:33.257026

"""

from datetime import datetime
from typing import Sequence, Union

from alembic import op

from src.api.database.models.aluno import Aluno
from src.api.database.models.professor import Professor
from src.api.database.models.solicitacoes import Solicitacao
from src.api.database.models.tarefas_base import TarefaBase
from src.api.database.models.tipo_usuario import TipoUsuario
from src.api.database.models.usuario import Usuario

# revision identifiers, used by Alembic.
revision: str = "10e4f2e0b261"
down_revision: Union[str, None] = "ac61d214ad4e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.bulk_insert(
        TipoUsuario.__table__,
        [
            {
                "titulo": "COORDENADOR",
                "descricao": "Coordenador description",
                "id": 1,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "titulo": "PROFESSOR",
                "descricao": "Professor description",
                "id": 2,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "titulo": "ALUNO",
                "descricao": "Aluno description",
                "id": 3,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
        ],
    )
    op.bulk_insert(
        Usuario.__table__,
        [
            {
                "nome": "Sem Orientador",
                "email": "sem_orientador@ufba.br",
                "senha_hash": "$2b$12$qx8sUyzH7L0/P3slZg6maOW1g11/G09YT89zxP2/cukl2aznAwCfW",  # noqa
                "new_password_token": None,
                "tipo_usuario_id": 2,
                "id": 1,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Coord Fred Durão",
                "email": "fred_coordenador@ufba.br",
                "senha_hash": "$2b$12$WGZL3R1KnQaZUMBs27Cw.e/YXYHgcEQ0iFQI59EaddLd./DRJkTlm",  # noqa
                "new_password_token": None,
                "tipo_usuario_id": 1,
                "id": 2,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Prof Fred Durão",
                "email": "fred_professor@ufba.br",
                "senha_hash": "$2b$12$jagLVP7tdNJQ0y/V97yTGe5I7gcVFn8tb79LgBMShlfbYGZZ0qyBq",  # noqa
                "new_password_token": None,
                "tipo_usuario_id": 2,
                "id": 3,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Aluno Fred Durão",
                "email": "fred_aluno@ufba.br",
                "senha_hash": "$2b$12$UkAuRH33KQCtXszd93ujhO994KdVA8BOAyvtaO4zDxlys54g.ruai",  # noqa
                "new_password_token": None,
                "tipo_usuario_id": 3,
                "id": 4,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
        ],
    )
    op.bulk_insert(
        Professor.__table__,
        [
            {
                "usuario_id": 1,
                "id": 1,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "usuario_id": 2,
                "id": 2,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
            {
                "usuario_id": 3,
                "id": 3,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            },
        ],
    )
    op.bulk_insert(
        Aluno.__table__,
        [
            {
                "cpf": "851.711.570-81",
                "telefone": "(71) 99999-9999",
                "matricula": "123456",
                "lattes": "http://lattes.cnpq.br/6271096128174325",
                "curso": "MESTRADO",
                "data_ingresso": datetime.now(),
                "data_qualificacao": datetime.now(),
                "data_defesa": datetime.now(),
                "orientador_id": 3,
                "usuario_id": 4,
                "id": 1,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            }
        ],
    )
    op.bulk_insert(
        Solicitacao.__table__,
        [
            {
                "aluno_id": 1,
                "professor_id": 3,
                "status": "PENDENTE",
                "id": 1,
                # "created_at": "2024-06-17 00:00:00",
                # "updated_at": "2024-06-17 00:00:00",
                "deleted_at": None,
            }
        ],
    )
    op.bulk_insert(
        TarefaBase.__table__,
        [
            {
                "nome": "Qualificacao de Mestrado",
                "descricao": "Atividade referente à qualificacao de mestrado, \
                  que deve ocorrer em até 12 meses.",
                "prazo_em_meses": 12,
                "curso": "MESTRADO",
                "id": 1,
                # "created_at": "2024-06-18 00:00:00",
                # "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Defesa de Mestrado",
                "descricao": "Atividade referente à defesa de mestrado, que deve \
                    ocorrer em até 24 meses.",
                "prazo_em_meses": 24,
                "curso": "MESTRADO",
                "id": 2,
                # "created_at": "2024-06-18 00:00:00",
                # "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Qualificacao Doutorado",
                "descricao": "Atividade referente à qualificacao de doutorado, \
                    que deve ocorrer em até 24 meses.",
                "prazo_em_meses": 24,
                "curso": "DOUTORADO",
                "id": 3,
                # "created_at": "2024-06-18 00:00:00",
                # "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Defesa Doutorado",
                "descricao": "Atividade referente à defesa de doutorado, que deve \
                    ocorrer em até 48 meses.",
                "prazo_em_meses": 48,
                "curso": "DOUTORADO",
                "id": 4,
                # "created_at": "2024-06-18 00:00:00",
                # "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM solicitacoes WHERE id = 1")
    op.execute("DELETE FROM alunos WHERE id = 1")
    op.execute("DELETE FROM professores WHERE id IN (1, 2)")
    op.execute("DELETE FROM usuarios WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM tipo_usuario WHERE id IN (1, 2, 3)")
    op.execute("DELETE FROM tarefas_base WHERE id IN (1, 2, 3, 4)")
