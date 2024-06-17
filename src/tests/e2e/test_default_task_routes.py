import pytest
from core.application import client
from core.base_default_task import (
    alternative_course,
    alternative_description,
    alternative_name,
    course,
    deadline_in_months,
    description,
    name,
    task_id,
)

valid_form = {
    "nome": name,
    "descricao": description,
    "prazo_em_meses": deadline_in_months,
    "curso": course,
}


@pytest.mark.dependency()
def test_create_default_task():
    """
    Test route for creating a new default task.
    """
    url = "/tarefas_base/"

    # Test sending a form with bad information.
    invalid_form_cases = [
        {"nome": ""},  # Empty name
        {"nome": " " * 20},  # Blank name
        {"nome": "N"},  # Short name
    ]
    for invalid_form in invalid_form_cases:
        form = valid_form.copy()
        form.update(invalid_form)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a incomplete form.
    for key in valid_form.keys():
        if valid_form[key] is None:
            continue

        form = valid_form.copy()
        form.pop(key)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a valid form.
    assert 200 <= client.post(url, json=valid_form).status_code <= 299

    # Test sending an alternative valid form.
    form = valid_form.copy()
    form["nome"] = alternative_name
    form["descricao"] = alternative_description
    assert 200 <= client.post(url, json=form).status_code <= 299


@pytest.mark.dependency(depends=["test_create_default_task"])
def test_get_default_task():
    """
    Test route for getting the default_task from the database.
    """
    expected = {"nome": name, "descricao": description, "curso": course}

    response = client.get(f"/tarefas_base/{task_id}")
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_default_task"])
def test_get_default_tasks_by_course_type():
    """
    Test route for getting the default tasks from the database by the course type.
    """
    expected = [
        {"nome": name, "descricao": description, "curso": course},
        {
            "nome": alternative_name,
            "descricao": alternative_description,
            "curso": course,
        },
    ]

    response = client.get(f"/tarefas_base/curso/{course}")
    assert 200 <= response.status_code <= 299

    result = sorted(response.json(), key=lambda x: x["id"])

    for row in range(len(result)):
        for key, value in expected[row].items():
            assert result[row].get(key, "") == value


@pytest.mark.dependency(depends=["test_create_default_task"])
def test_update_default_task():
    """
    Test route for updating the default task's information on the database.
    """
    url = f"/tarefas_base/{task_id}"

    new_data = {
        "nome": "Th1s is 4 nic3 s#per ultr@ titl3!! =)",
        "descricao": "Th1s is 4 nic3 s#per ultr@ d3scr1ption!! =)",
        "curso": alternative_course,
    }

    # Update user's information.
    form = valid_form.copy()
    form.update(new_data)

    response = client.put(url, json=form)
    assert 200 <= response.status_code <= 299

    # Get the user's information and check the changes.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in new_data.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_default_task"])
def test_delete_default_task():
    """
    Test route for deleting the default_task from the database.
    """
    url = f"/tarefas_base/{task_id}"

    # Try to get the user.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    # Update user's information.
    response = client.delete(url)
    assert 200 <= response.status_code <= 299

    # Try to get the deleted user.
    response = client.get(url)
    assert response.status_code >= 400
