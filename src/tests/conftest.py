import os
import sys

import pytest
from core import base_professor, base_student, base_student_task

from src.api.utils.enums import TipoUsuarioEnum

current_dir = os.path.join(os.getcwd())
sys.path.append(current_dir)

os.environ["TESTING"] = "true"


def pytest_collection_modifyitems(items):
    """
    Modifies test items in place to ensure test modules run in a given order.
    """
    MODULE_ORDER = [
        "test_application",
        "test_professor_routes",
        "test_student_routes",
        "test_login_route",
        "test_set_new_password",
        "test_default_task_routes",
        "test_student_task_routes",
        "test_mailer",
    ]

    module_mapping = {item: item.module.__name__ for item in items}

    sorted_items = items.copy()

    # Iteratively move tests of each module to the end of the test queue.
    for module in MODULE_ORDER:
        sorted_items = [it for it in sorted_items if module_mapping[it] != module] + [
            it for it in sorted_items if module_mapping[it] == module
        ]
    items[:] = sorted_items


@pytest.fixture
def valid_student_data():
    return {
        "nome": base_student.name,
        "cpf": base_student.cpf,
        "email": base_student.email,
        "telefone": base_student.phone,
        "matricula": base_student.registration,
        "orientador_id": 1,
        "curso": base_student.course,
        "lattes": base_student.lattes,
        "data_ingresso": "2021-01-01",
        "data_qualificacao": "2022-06-01",
        "data_defesa": "2023-12-01",
        "senha": base_student.password,
        "tipo_usuario": TipoUsuarioEnum.ALUNO,
    }


@pytest.fixture
def valid_professor_data():
    return {
        "nome": base_professor.name,
        "email": base_professor.email,
        "tipo_usuario": base_professor.tipo_usuario,
        "senha": base_professor.password,
    }


@pytest.fixture
def valid_task_data():
    return {
        "nome": base_student_task.name,
        "descricao": base_student_task.description,
        "completada": base_student_task.completed,
        "data_prazo": base_student_task.deadline_date,
        "last_notified": base_student_task.last_notified,
        "data_conclusao": base_student_task.completion_date,
    }


# from src.api.database.models import (  # noqa
#     aluno,
#     professor,
#     solicitacoes,
#     tarefa,
#     tarefas_base,
#     tipo_usuario,
#     usuario,
# )
# from src.tests.core.mocked_database import engine

# @pytest.fixture(scope="function", autouse=True)
# def setup_database():
#     aluno.Aluno.metadata.drop_all(bind=engine)
#     aluno.Aluno.metadata.create_all(bind=engine)
#     professor.Professor.metadata.drop_all(bind=engine)
#     professor.Professor.metadata.create_all(bind=engine)
#     solicitacoes.Solicitacao.metadata.drop_all(bind=engine)
#     solicitacoes.Solicitacao.metadata.create_all(bind=engine)
#     tarefa.Tarefa.metadata.drop_all(bind=engine)
#     tarefa.Tarefa.metadata.create_all(bind=engine)
#     tarefas_base.TarefasBase.metadata.drop_all(bind=engine)
#     tarefas_base.TarefasBase.metadata.create_all(bind=engine)
#     tipo_usuario.TipoUsuario.metadata.drop_all(bind=engine)
#     tipo_usuario.TipoUsuario.metadata.create_all(bind=engine)
#     usuario.Usuario.metadata.drop_all(bind=engine)
#     usuario.Usuario.metadata.create_all(bind=engine)
