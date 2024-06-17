import pytest
from core.application import client
from core.base_student_task import (
    alternative_description,
    alternative_name,
    description,
    name,
    task_id,
)
from loguru import logger

aluno_id: int = 1


@pytest.mark.dependency()
def test_create_task(valid_professor_data, valid_student_data, valid_task_data):
    """
    Test route for creating a new task.
    """
    global aluno_id

    url = "/tarefas/"

    # Test sending a form with bad information.
    invalid_form_cases = [
        {"nome": ""},  # Empty name
        {"nome": " " * 20},  # Blank name
        {"nome": "N"},  # Short name
    ]
    for invalid_form in invalid_form_cases:
        form = valid_task_data.copy()
        form.update(invalid_form)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a incomplete form.
    for key in valid_task_data.keys():
        if valid_task_data[key] is None:
            continue

        form = valid_task_data.copy()
        form.pop(key)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a valid form.
    valid_professor_data["email"] = valid_professor_data["email"] + "newProfessor"

    resp_professor = client.post("/professores/", json=valid_professor_data)
    logger.info(resp_professor.json())
    valid_student_data["orientador_id"] = resp_professor.json()["id"]

    resp_aluno = client.post("/alunos/", json=valid_student_data)
    aluno_id = resp_aluno.json()["id"]
    valid_task_data["aluno_id"] = aluno_id

    resp2 = client.post(url, json=valid_task_data)
    logger.info(resp2.json())
    assert 200 <= resp2.status_code <= 299

    # Test sending an alternative valid form.
    form = valid_task_data.copy()
    form["nome"] = alternative_name
    form["descricao"] = alternative_description
    assert 200 <= client.post(url, json=form).status_code <= 299

    # Test sending the same form but for a student that does NOT exists on database.
    form = valid_task_data.copy()
    form["aluno_id"] = 1 + 10**4
    assert client.post(url, json=form).status_code >= 400


@pytest.mark.dependency(depends=["test_create_task"])
def test_get_task():
    """
    Test route for getting the task from the database.
    """
    expected = {"nome": name, "descricao": description, "aluno_id": aluno_id}

    response = client.get(f"/tarefas/{task_id}")
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_task"])
def test_get_tasks_by_student_id():
    """
    Test route for getting the tasks from the database by the ID of a student.
    """
    global aluno_id

    expected = [
        {"nome": name, "descricao": description, "aluno_id": aluno_id},
        {
            "nome": alternative_name,
            "descricao": alternative_description,
            "aluno_id": aluno_id,
        },
    ]

    response = client.get(f"/tarefas/aluno/{aluno_id}")
    assert 200 <= response.status_code <= 299

    result = sorted(response.json(), key=lambda x: x["id"])

    for row in range(len(result)):
        for key, value in expected[row].items():
            assert result[row].get(key, "") == value


@pytest.mark.dependency(depends=["test_create_task"])
def test_update_task(valid_task_data):
    """
    Test route for updating the task's information on the database.
    """
    global aluno_id

    url = f"/tarefas/{task_id}"

    new_data = {
        "nome": "Th1s is 4 nic3 s#per ultr@ titl3!! =)",
        "descricao": "Th1s is 4 nic3 s#per ultr@ d3scr1ption!! =)",
    }

    # Update user's information.
    form = valid_task_data.copy()
    form.update(new_data)
    form["aluno_id"] = aluno_id

    response = client.put(url, json=form)
    logger.info(response.json())
    assert 200 <= response.status_code <= 299

    # Get the user's information and check the changes.
    response = client.get(url)
    logger.info(response.json())
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in new_data.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_task"])
def test_delete_task():
    """
    Test route for deleting the task from the database.
    """
    url = f"/tarefas/{task_id}"

    # Try to get the user.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    # Update user's information.
    response = client.delete(url)
    assert 200 <= response.status_code <= 299

    # Try to get the deleted user.
    response = client.get(url)
    assert response.status_code >= 400
