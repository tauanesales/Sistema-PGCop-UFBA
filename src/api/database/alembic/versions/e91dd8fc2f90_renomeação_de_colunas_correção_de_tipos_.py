"""Renomeação de colunas, correção de tipos, etc

Revision ID: e91dd8fc2f90
Revises: 10e4f2e0b261
Create Date: 2024-06-19 06:21:10.434972

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import mysql

from src.api.database.models.tarefas_base import TarefaBase

# revision identifiers, used by Alembic.
revision: str = "e91dd8fc2f90"
down_revision: Union[str, None] = "10e4f2e0b261"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "alunos",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "alunos",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "alunos",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.alter_column(
        "professores",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "professores",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "professores",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.alter_column(
        "solicitacoes",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "solicitacoes",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "solicitacoes",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.alter_column(
        "tarefas",
        "data_ultima_notificacao",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        nullable=False,
    )
    op.alter_column(
        "tarefas",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.alter_column(
        "tarefas_base",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas_base",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas_base",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.alter_column(
        "tipo_usuario",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "tipo_usuario",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "tipo_usuario",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.add_column(
        "usuarios", sa.Column("token_nova_senha", sa.String(length=255), nullable=True)
    )
    op.alter_column(
        "usuarios",
        "created_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "usuarios",
        "updated_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "usuarios",
        "deleted_at",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=True,
    )
    op.drop_column("usuarios", "new_password_token")
    # ### end Alembic commands ###

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
                "created_at": "2024-06-18 00:00:00",
                "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Defesa de Mestrado",
                "descricao": "Atividade referente à defesa de mestrado, que deve \
                    ocorrer em até 24 meses.",
                "prazo_em_meses": 24,
                "curso": "MESTRADO",
                "id": 2,
                "created_at": "2024-06-18 00:00:00",
                "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Qualificacao Doutorado",
                "descricao": "Atividade referente à qualificacao de doutorado, \
                    que deve ocorrer em até 24 meses.",
                "prazo_em_meses": 24,
                "curso": "DOUTORADO",
                "id": 3,
                "created_at": "2024-06-18 00:00:00",
                "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
            {
                "nome": "Defesa Doutorado",
                "descricao": "Atividade referente à defesa de doutorado, que deve \
                    ocorrer em até 48 meses.",
                "prazo_em_meses": 48,
                "curso": "DOUTORADO",
                "id": 4,
                "created_at": "2024-06-18 00:00:00",
                "updated_at": "2024-06-18 00:00:00",
                "deleted_at": None,
            },
        ],
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "usuarios",
        sa.Column(
            "new_password_token",
            mysql.VARCHAR(collation="utf8mb4_unicode_ci", length=255),
            nullable=True,
        ),
    )
    op.alter_column(
        "usuarios",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "usuarios",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "usuarios",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.drop_column("usuarios", "token_nova_senha")
    op.alter_column(
        "tipo_usuario",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "tipo_usuario",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "tipo_usuario",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas_base",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "tarefas_base",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas_base",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "tarefas",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "tarefas",
        "data_ultima_notificacao",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        nullable=True,
    )
    op.alter_column(
        "solicitacoes",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "solicitacoes",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "solicitacoes",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "professores",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "professores",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "professores",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "alunos",
        "deleted_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=True,
    )
    op.alter_column(
        "alunos",
        "updated_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "alunos",
        "created_at",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    # ### end Alembic commands ###
    op.execute("DELETE FROM tarefas_base WHERE id IN (1, 2, 3, 4)")
