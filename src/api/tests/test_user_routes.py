from core.application import client


def test_create_user():
    invalid_form = {"Nome": "Roberto", "Email": "roberto@ufba.br", "Role": "professor"}  # Missing password
    invalid_password = {"Nome": "Roberto", "Email": "roberto@ufba.br", "Role": "professor", "Senha": "patao 002"}  # Contains spacing
    valid_user = {"Nome": "Roberto", "Email": "roberto@ufba.br", "Role": "professor", "Senha": "patao002"}

    url = "/usuarios/"

    assert client.post(url, json=invalid_form).status_code >= 400
    assert client.post(url, json=invalid_password).status_code >= 400
    assert 200 <= client.post(url, json=valid_user).status_code <= 299