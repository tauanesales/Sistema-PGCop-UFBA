from core.application import client


def test_health_checker():
    assert client.get("/health-check").status_code == 200
