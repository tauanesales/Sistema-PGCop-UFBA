from core.application import client

from core.base_professor import (
    email, 
    name, 
    password,
    role
)

import pytest

name = "New" +  name
email = "new" + email

valid_form = {
    "nome": name,
    "email": email,
    "role": role,
    "senha": password,
}

newPasswordAuth = None


@pytest.mark.dependency()
def test_create_token():
    """
    Test route for creating a token to allow setting a new password.
    """
    global newPasswordAuth

    # A new user must be created for testing.
    assert 200 <= client.post("professores/", json=valid_form).status_code <= 299

    # Create token.
    response = client.post("new_password/create_token", json={"email": email})
    assert 200 <= response.status_code <= 299

    newPasswordAuth = response.json()


@pytest.mark.dependency(depends=["test_create_token"])
def test_authentication():
    """
    Test route for checking access token.
    """
    # Authenticate token.
    assert 200 <= client.post("new_password/auth", json=newPasswordAuth).status_code <= 299

