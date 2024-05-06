from core.application import client

from core.base_professor import (
    alternative_email,
    alternative_name,
    alternative_role,
    email, 
    name, 
    password,
    role,
    user_id
)


valid_form = {
    "nome": name,
    "email": email,
    "role": role,
    "senha": password,
}

token = None


def test_login():
    """
    Test route for log in to an account.
    """
    global token

    # Create a new user.
    assert 200 <= client.post("professores/", json=valid_form).status_code <= 299
    
    # Log in to the account.
    login_data = {
        "username": email, 
        "password": password, 
        "grant_type": "password"
    }

    response = client.post("token/", data=login_data, headers={"content-type": "application/x-www-form-urlencoded"})

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
        {"username": email, "password": password.capitalize(), "grant_type": "password"},
        {"username": email, "password": password.upper(), "grant_type": "password"},
    ]

    for test_case in test_cases:
        response = client.post("token/", data=test_case, headers={"content-type": "application/x-www-form-urlencoded"})
        assert response.status_code >= 400

    # Try to log in to an account of different username but same password.
    login_data = {
        "username": email.split("@")[0] + "@ufmg.br", 
        "password": password, 
        "grant_type": "password"
    }

    response = client.post("token/", data=login_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code >= 400


def test_check_token():
    """
    Test route for checking user access.
    """

    headers = {"Authorization": f"{token['token_type'].capitalize()} {token['access_token']}"}

    response = client.get("professores/me", headers=headers)
    assert 200 <= response.status_code <= 299