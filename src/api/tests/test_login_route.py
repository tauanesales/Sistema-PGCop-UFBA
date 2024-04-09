from core.application import client
from core.base_user import email, name, password, role, new_role, user_id


def test_login():
    """
    Test route for log in to an account.
    """

    # Create a new user.
    user_data = {"Nome": name, "Email": email, "Role": role, "Senha": password}
    assert 200 <= client.post("usuarios/", json=user_data).status_code <= 299
    
    # Log in to the account.
    login_data = {
        "username": email, 
        "password": password, 
        "grant_type": "password"
    }

    response = client.post("token/", data=login_data, headers={"content-type": "application/x-www-form-urlencoded"})
    assert 200 <= response.status_code <= 299


