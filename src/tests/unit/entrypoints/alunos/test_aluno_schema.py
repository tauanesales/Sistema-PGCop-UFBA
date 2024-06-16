import pytest
from pydantic import ValidationError

from src.api.entrypoints.alunos.schema import AlunoCreate
from src.api.exceptions.validation_exception import (
    PasswordWithoutLowercaseError,
    PasswordWithoutNumberError,
    PasswordWithoutSpecialCharacterError,
    PasswordWithoutUppercaseError,
    PasswordWithSpacesError,
)


def test_aluno_create_valid(valid_student_data: dict):
    aluno = AlunoCreate(**valid_student_data)
    assert aluno.nome == valid_student_data.get("nome")
    assert aluno.cpf == valid_student_data.get("cpf")
    assert aluno.email == valid_student_data.get("email")
    assert aluno.telefone == valid_student_data.get("telefone")
    assert aluno.matricula == valid_student_data.get("matricula")
    assert aluno.orientador_id == valid_student_data.get("orientador_id")
    assert aluno.curso == valid_student_data.get("curso")
    assert aluno.lattes == valid_student_data.get("lattes")
    assert aluno.data_ingresso == valid_student_data.get("data_ingresso")
    assert aluno.data_qualificacao == valid_student_data.get("data_qualificacao")
    assert aluno.data_defesa == valid_student_data.get("data_defesa")
    assert aluno.senha == valid_student_data.get("senha")


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
def test_aluno_create_password_with_spaces_error(valid_student_data, password):
    valid_student_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        AlunoCreate(**valid_student_data)

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
def test_aluno_create_password_without_number_error(valid_student_data, password):
    valid_student_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        AlunoCreate(**valid_student_data)

    assert str(PasswordWithoutNumberError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "password1",
        "password1!",
        "password!123",
    ],
)
def test_aluno_create_password_without_uppercase_error(valid_student_data, password):
    valid_student_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        AlunoCreate(**valid_student_data)

    assert str(PasswordWithoutUppercaseError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "PASSWORD1",
        "PASSWORD1!",
        "PASSWORD!123",
    ],
)
def test_aluno_create_password_without_lowercase_error(valid_student_data, password):
    valid_student_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        AlunoCreate(**valid_student_data)

    assert str(PasswordWithoutLowercaseError()) in exc.value.errors()[0].get("msg")


@pytest.mark.parametrize(
    "password",
    [
        "Password1",
        "Password123",
        "PASSword12",
    ],
)
def test_aluno_create_password_without_special_character_error(
    valid_student_data, password
):
    valid_student_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        AlunoCreate(**valid_student_data)

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
def test_aluno_create_short_password_error(valid_student_data, password):
    valid_student_data["senha"] = password
    with pytest.raises(ValidationError) as exc:
        AlunoCreate(**valid_student_data)

    assert "String should have at least 8 characters" in exc.value.errors()[0].get(
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
def test_aluno_create_valid_password(valid_student_data, password):
    valid_student_data["senha"] = password
    student = AlunoCreate(**valid_student_data)
    assert student.senha == password
