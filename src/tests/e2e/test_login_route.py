import pytest
from core.application import client

from loguru import logger

token = None


@pytest.mark.dependency()
def test_login(valid_professor_data):
    """
    Test route for log in to an account.
    """
    global token

    valid_professor_data["email"] = valid_professor_data["email"] + "new"

    email = valid_professor_data["email"]
    password = valid_professor_data["senha"]

    # Create a new user.
    resp = client.post("/professores/", json=valid_professor_data)
    assert 200 <= resp.status_code <= 299

    # Log in to the account.
    login_data = {
        "username": email, 
        "password": password, 
        "grant_type": "password",
        "scope": "items:read items:write users:read profile openid"
    }

    response = client.post(
        "token/",
        data=login_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    logger.info(response.json())

    assert 200 <= response.status_code <= 299

    token = response.json()
    assert "access_token" in token

    # Try to invade the account.
    test_cases = [
        {"username": email, "grant_type": "password"},
        {"username": email, "password": "", "grant_type": "password"},
        {"username": email, "password": " ", "grant_type": "password"},
        {"username": email, "password": " " * len(password), "grant_type": "password"},
        {"username": email, "password": password[:-1], "grant_type": "password"},
        {
            "username": email,
            "password": password.capitalize(),
            "grant_type": "password",
        },
        {"username": email, "password": password.upper(), "grant_type": "password"},
    ]

    for test_case in test_cases:
        response = client.post(
            "token/",
            data=test_case,
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code >= 400

    # Try to log in to an account of different username but same password.
    login_data = {
        "username": email.split("@")[0] + "@ufmg.br",
        "password": password,
        "grant_type": "password",
    }

    response = client.post(
        "token/",
        data=login_data,
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code >= 400


@pytest.mark.dependency(depends=["test_login"])
def test_check_token():
    """
    Test route for checking user access.
    """

    headers = {
        "Authorization": f"{token['token_type'].capitalize()} {token['access_token']}"
    }

    response = client.get("professores/me", headers=headers)
    assert 200 <= response.status_code <= 299
