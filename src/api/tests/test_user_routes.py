from core.application import client
from core.base_user import email, name, password, role, new_role, user_id


def test_create_user():
    """
    Test route for creating a new user.
    """
    url = "/usuarios/"

    # Test sending invalid forms.
    invalid_form_cases = [
        {"Nome": name, "Email": email, "Role": "senador", "Senha": password},                    # Illegal role
        {"Nome": name, "Role": role, "Senha": password},                                         # Missing email
        {"Nome": name, "Email": email, "Role": role},                                            # Missing password
        {"Nome": "", "Email": email, "Role": role, "Senha": password},                           # Empty name
        {"Nome": name, "Email": "", "Role": role, "Senha": password},                            # Empty email
        {"Nome": name, "Email": email, "Role": role, "Senha": ""},                               # Empty password
        {"Nome": name, "Email": email.replace("@", ""), "Role": role, "Senha": password},        # Invalid email (no domain)
        {"Nome": name, "Email": email.split("@")[0] + "@", "Role": role, "Senha": password},     # Invalid email (no domain name)
        {"Nome": name, "Email": email + "@ufba.br", "Role": role, "Senha": password},            # Invalid email (illegal char)
        {"Nome": name, "Email": email, "Role": role, "Senha": password + " " + "3"},             # Invalid password (with spaces)
        {"Nome": name, "Email": email, "Role": role, "Senha": password[:3]},                     # Invalid password (very short)
    ]

    for invalid_form in invalid_form_cases:
        assert client.post(url, json=invalid_form).status_code >= 400

    # Test sending a valid form.
    valid_form_case = {"Nome": name, "Email": email, "Role": role, "Senha": password}
    assert 200 <= client.post(url, json=valid_form_case).status_code <= 299

    # Test sending the same valid form again.
    assert client.post(url, json=valid_form_case).status_code >= 400

    # Test sending a different form but with an email that already exists on database.
    valid_form_case["Nome"] = "Another guy"
    valid_form_case["Senha"] = "AnotherPassword"
    valid_form_case["Role"] = "orientador"
    assert client.post(url, json=valid_form_case).status_code >= 400


def test_get_user():
    """
    Test route for getting the user from the database.
    """
    url = f"/usuarios/{user_id}"

    expected = {"Nome": name, "Email": email, "Role": role}
    
    response = client.get(url)

    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


def test_get_user_by_email():
    """
    Test route for getting the user from the database by his email.
    """
    url = f"/usuarios/email/{email}"

    expected = {"Nome": name, "Email": email, "Role": role}
    
    response = client.get(url)

    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in expected.items():
        assert result.get(key, "") == value


def test_update_user():
    """
    Test route for updating the user's information on the database.
    """
    url = f"/usuarios/{user_id}"

    new_data = {"Nome": name, "Email": email.split("@")[0] + "@ufmg.br", "Role": new_role}
    
    # Update user's information.
    response = client.put(url, json = new_data)
    assert 200 <= response.status_code <= 299

    # Get the user's information and check the changes.
    response = client.get(url)
    assert 200 <= response.status_code <= 299

    result = response.json()

    for key, value in new_data.items():
        assert result.get(key, "") == value
    

def test_delete_user():
    """
    Test route for deleting the user from the database.
    """
    url = f"/usuarios/{user_id}"

    # Update user's information.
    response = client.delete(url)
    assert 200 <= response.status_code <= 299

    # Try to get the deleted user.
    response = client.get(url)
    assert response.status_code >= 400