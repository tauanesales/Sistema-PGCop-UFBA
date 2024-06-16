import os
import sys
from datetime import date

import pytest
from core import base_professor, base_student

current_dir = os.path.join(os.getcwd())
sys.path.append(current_dir)

os.environ["TESTING"] = "true"


def pytest_collection_modifyitems(items):
    """
    Modifies test items in place to ensure test modules run in a given order.
    """
    MODULE_ORDER = [
        "test_application",
        "test_student_routes",
        "test_professor_routes",
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
        "data_ingresso": date(2021, 1, 1),
        "data_qualificacao": date(2022, 6, 1),
        "data_defesa": date(2023, 12, 1),
        "senha": base_student.password,
    }


@pytest.fixture
def valid_professor_data():
    return {
        "nome": base_professor.name,
        "email": base_professor.email,
        "role": base_professor.role,
        "senha": base_professor.password,
    }
