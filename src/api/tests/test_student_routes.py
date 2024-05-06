from core.application import client

from core.base_student import (
    admission_date, 
    advisor_id,
    alternative_course,
    alternative_cpf, 
    alternative_email, 
    alternative_name,
    course, 
    cpf, 
    defense_date,
    email, 
    lattes,
    name, 
    password, 
    phone,
    qualification_date,
    registration,
    user_id
)

import pytest


valid_form = {
    "nome": name,
    "cpf": cpf,
    "email": email,
    "matricula": registration,
    "curso": course,
    "senha": password,
    "telefone": phone,
    "lattes": lattes,
    "data_ingresso": admission_date,
    "data_defesa": defense_date,
    "data_qualificacao": qualification_date,
    "orientador_id": advisor_id,
}


def test_create_student():
    """
    Test route for creating a new student.
    """
    url = "/alunos/"

    # Test sending a form with bad information.
    invalid_form_cases = [
        {"nome": ""},                                                                          # Empty name
        {"nome": " " * 20},                                                                    # Blank name
        {"nome": "N"},                                                                         # Short name
        {"nome": "Je4n L0u1"},                                                                 # Illegal name
        {"cpf": ""},                                                                           # Empty CPF
        {"cpf": " " * 11},                                                                     # Blank CPF
        {"cpf": "this is my cpf"},                                                             # Illegal CPF
        {"cpf": "123.456.789-11"},                                                             # Invalid CPF
        {"email": ""},                                                                         # Empty email
        {"email": " " * 20},                                                                   # Blank email
        {"email": email.replace("@", "")},                                                     # Invalid email (no domain)
        {"email": email.split("@")[0] + "@"},                                                  # Invalid email (no domain name)
        {"email": email.split("@")[0] + "some@name@ufba.br"},                                  # Invalid email (illegal char)
        {"curso": ""},                                                                         # Empty course
        {"curso": " " * 20},                                                                   # Blank course
        {"curso": "SomeCourse"},                                                               # Illegal course
        {"senha": ""},                                                                         # Empty password
        {"senha": " " * 10},                                                                   # Blank password
        {"senha": password + " " + "something"},                                               # Illegal password (with spaces)
        {"senha": password[:3]},                                                               # Short password
    ]
    for invalid_form in invalid_form_cases:
        form = valid_form.copy()
        form.update(invalid_form)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a incomplete form.
    for key in valid_form.keys():
        form = valid_form.copy()
        form.pop(key)

        assert client.post(url, json=form).status_code >= 400

    # Test sending a valid form.
    assert 200 <= client.post(url, json=valid_form).status_code <= 299

    # Test sending the same valid form again (you should NOT be able to create the same student again).
    assert client.post(url, json=valid_form).status_code >= 400

    # Test sending a different form but with an email that already exists on database.
    form = valid_form.copy()
    form["nome"] = "Another Guy"
    form["senha"] = "AnotherPassword"
    form["cpf"] = alternative_cpf
    assert client.post(url, json=form).status_code >= 400

    # Test sending a different form but with a CPF that already exists on database.
    form = valid_form.copy()
    form["nome"] = "Another Guy"
    form["senha"] = "AnotherPassword"
    form["email"] = alternative_email
    assert client.post(url, json=form).status_code >= 400

    # Test sending a form with the same data, except the identication.
    form = valid_form.copy()
    form["cpf"] = alternative_cpf
    form["email"] = alternative_email
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

    new_data = {"nome": alternative_name, "email": alternative_email.split("@")[0] + "foo" + "@ufmg.br", "course": alternative_course}
    
    # Update user's information.
    form = valid_form.copy()
    form.update(new_data)
    form.pop("senha")

    response = client.put(url, json=form)
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