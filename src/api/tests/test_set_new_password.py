from core.application import client

from core.base_professor import (
    email, 
    name, 
    password,
    role
)

from typing import Dict, Optional
import pytest

name = "New" +  name
email = "new" + email
new_password = "new" + password

valid_form = {
    "nome": name,
    "email": email,
    "role": role,
    "senha": password,
}

newPasswordAuth: Optional[Dict] = None


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


@pytest.mark.dependency(depends=["test_authentication"])
def test_set_new_password():
    """
    Test route for setting access token.
    """

    # Log in to the account.
    login_data = {
        "username": email, 
        "password": password, 
        "grant_type": "password"
    }
    response = client.post("token/", data=login_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert 200 <= response.status_code <= 299

    # Set a new password.
    newPasswordJson = newPasswordAuth.copy()
    newPasswordJson["nova_senha"] = new_password
    assert 200 <= client.post("new_password/", json=newPasswordJson).status_code <= 299

    # It must not work anymore.
    response = client.post("token/", data=login_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert 400 <= response.status_code <= 499

    # Log in to the account.
    login_data["password"] = new_password
    
    response = client.post("token/", data=login_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert 200 <= response.status_code <= 299
    
