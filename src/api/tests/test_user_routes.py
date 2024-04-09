from core.application import client


def test_create_user():
    """
    Test route for creating a new user.
    """
    url = "/usuarios/"

    name = "Roberto"
    email = "roberto@ufba.br"
    role = "professor"
    password = "patao002"

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