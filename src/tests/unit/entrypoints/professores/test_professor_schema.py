import pytest
from pydantic import ValidationError

from src.api.entrypoints.professores.schema import ProfessorCreate
from src.api.exceptions.validation_exception import (
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
)


def test_professor_create_valid(valid_professor_data: dict):
    professor = ProfessorCreate(**valid_professor_data)
    assert professor.nome == valid_professor_data.get("nome")
    assert professor.email == valid_professor_data.get("email")
    assert professor.role == valid_professor_data.get("role")
    assert professor.senha == valid_professor_data.get("senha")


@pytest.mark.parametrize(
    "password",
    [
        "               ",
        " password",
        "p assword123",
        "PASSWORD123 ",
        "Password1! ",
        " Password1!",
        "Pass word1!",
    ],
)
def test_professor_create_password_with_spaces_error(valid_professor_data, password):
    valid_professor_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        ProfessorCreate(**valid_professor_data)

    assert str(PasswordWithSpacesError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "password",
        "Password!",
        "password",
        "PASSWORD!",
        "PASSWORd!",
    ],
)
def test_professor_create_password_without_number_error(valid_professor_data, password):
    valid_professor_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        ProfessorCreate(**valid_professor_data)

    assert str(PasswordWithoutNumberError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "password1",
        "password1!",
        "password!123",
    ],
)
def test_professor_create_password_without_uppercase_error(
    valid_professor_data, password
):
    valid_professor_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        ProfessorCreate(**valid_professor_data)

    assert str(PasswordWithoutUppercaseError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "PASSWORD1",
        "PASSWORD1!",
        "PASSWORD!123",
    ],
)
def test_professor_create_password_without_lowercase_error(
    valid_professor_data, password
):
    valid_professor_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        ProfessorCreate(**valid_professor_data)

    assert str(PasswordWithoutLowercaseError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "Password1",
        "Password123",
        "PASSword12",
    ],
)
def test_professor_create_password_without_special_character_error(
    valid_professor_data, password
):
    valid_professor_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        ProfessorCreate(**valid_professor_data)

    assert str(PasswordWithoutSpecialCharacterError()) in exc.value.errors()[0].get(
        "msg"
    )


@pytest.mark.parametrize(
    "password",
    [
        "123",
        "abc",
        "",
        " ",
    ],
)
def test_professor_create_short_password_error(valid_professor_data, password):
    valid_professor_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        ProfessorCreate(**valid_professor_data)

    assert "String should have at least 7 characters" in exc.value.errors()[0].get(
        "msg"
    )


@pytest.mark.parametrize(
    "password",
    [
        "Password1!",
        "Password!123",
        "Password!123",
    ],
)
def test_professor_create_valid_password(valid_professor_data, password):
    valid_professor_data["senha"] = password
    student = ProfessorCreate(**valid_professor_data)
    assert student.senha == password
