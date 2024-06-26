import pytest
from core.application import client
from core.base_student import (
    alternative_cpf,
    alternative_email,
    alternative_phone,
    alternative_registration,
    cpf,
    email,
    name,
    password,
    registration,
    user_id,
)
from loguru import logger


@pytest.mark.dependency()
def test_create_student(valid_student_data, valid_professor_data):
    """
    Test route for creating a new student.
    """
    url = "/alunos/"

    # Test sending a form with bad information.
    invalid_form_cases = [
        {"nome": ""},  # Empty name
        {"nome": " " * 20},  # Blank name
        {"nome": "N"},  # Short name
        {"nome": "Je4n L0u1"},  # Illegal name
        {"cpf": ""},  # Empty CPF
        {"cpf": " " * 11},  # Blank CPF
        {"cpf": "this is my cpf"},  # Illegal CPF
        {"cpf": "123.456.789-11"},  # Invalid CPF
        {"email": ""},  # Empty email
        {"email": " " * 20},  # Blank email
        {"email": email.replace("@", "")},  # Invalid email (no domain)
        {"email": email.split("@")[0] + "@"},  # Invalid email (no domain name)
        {
            "email": email.split("@")[0] + "some@name@ufba.br"
        },  # Invalid email (illegal char)
        {"curso": ""},  # Empty course
        {"curso": " " * 20},  # Blank course
        {"curso": "SomeCourse"},  # Illegal course
        {"senha": ""},  # Empty password
        {"senha": " " * 10},  # Blank password
        {"senha": password + " " + "something"},  # Illegal password (with spaces)
        {"senha": password[:3]},  # Short password
    ]
    for invalid_form in invalid_form_cases:
        form = valid_student_data.copy()
        form.update(invalid_form)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a incomplete form.
    for key in valid_student_data.keys():
        if valid_student_data[key] is None:
            continue

        form = valid_student_data.copy()
        form.pop(key)

        assert client.post(url, json=form).status_code >= 400

    # Must have a professor associated to the student.
    resp = client.post("/professores/", json=valid_professor_data)
    valid_student_data["orientador_id"] = resp.json()["id"]

    # Test sending a valid form.
    resp = client.post(url, json=valid_student_data)
    logger.info(resp.json())
    assert 200 <= resp.status_code <= 299

    # Test sending the same valid form again (you should NOT be able to create the same
    # student again).
    assert client.post(url, json=valid_student_data).status_code >= 400

    # Test sending a different form but with an email that already exists on database.
    form = valid_student_data.copy()
    form["telefone"] = alternative_phone  # Phone is a unique field at the database.
    form["nome"] = "Another Guy"
    form["senha"] = "AnotherPassword"
    form["cpf"] = alternative_cpf
    form["matricula"] = alternative_registration
    assert client.post(url, json=form).status_code >= 400

    # Test sending a different form but with a CPF that already exists on database.
    form = valid_student_data.copy()
    form["telefone"] = alternative_phone  # Phone is a unique field at the database.
    form["nome"] = "Another Guy"
    form["senha"] = "AnotherPassword"
    form["email"] = alternative_email
    form["matricula"] = alternative_registration
    assert client.post(url, json=form).status_code >= 400

    # Test sending a different form but with a registration that already exists on
    # database.
    form = valid_student_data.copy()
    form["telefone"] = alternative_phone  # Phone is a unique field at the database.
    form["nome"] = "Another Guy"
    form["senha"] = "AnotherPassword"
    form["cpf"] = alternative_cpf
    form["email"] = alternative_email
    assert client.post(url, json=form).status_code >= 400

    # Test sending a form with the same data, but different identication.
    form = valid_student_data.copy()
    form["telefone"] = alternative_phone  # Phone is a unique field at the database.
    form["cpf"] = alternative_cpf
    form["email"] = alternative_email
    form["matricula"] = alternative_registration
    assert 200 <= client.post(url, json=form).status_code <= 299


@pytest.mark.dependency(depends=["test_create_student"])
def test_get_student():
    """
    Test route for getting the student from the database.
    """
    expected = {"nome": name, "email": email, "cpf": cpf, "matricula": registration}

    response = client.get(f"/alunos/{user_id}")
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_student"])
def test_get_student_by_cpf():
    """
    Test route for getting the student from the database by his CPF.
    """
    expected = {"nome": name, "email": email, "cpf": cpf, "matricula": registration}

    response = client.get(f"/alunos/cpf/{cpf}")
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_student"])
def test_get_student_by_email():
    """
    Test route for getting the student from the database by his email.
    """
    expected = {"nome": name, "email": email, "cpf": cpf, "matricula": registration}

    response = client.get(f"/alunos/email/{email}")
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_student"])
def test_update_student():
    """
    Test route for updating the student's information on the database.
    """
    url = f"/alunos/{user_id}"

    new_data = {
        # "nome": alternative_name,
        # "email": alternative_email.split("@")[0] + "foo" + "@ufmg.br",
        # "curso": alternative_course,
        "telefone": "(11) 99874-6543",
        "lattes": "http://lattes.cnpq.br/6271096128174325",
    }

    response = client.put(url, json=new_data)
    logger.info(response.json())
    assert 200 <= response.status_code <= 299

    # Get the user's information and check the changes.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in new_data.items():
        assert result.get(key, "") == value


@pytest.mark.dependency(depends=["test_create_student"])
def test_delete_student():
    """
    Test route for deleting the student from the database.
    """
    url = f"/alunos/{user_id}"

    # Try to get the user.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    # Update user's information.
    response = client.delete(url)
    assert 200 <= response.status_code <= 299

    # Try to get the deleted user.
    response = client.get(url)
    assert response.status_code >= 400
