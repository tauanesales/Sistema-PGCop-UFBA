from core.mocked_database import mocked_database
from fastapi.testclient import TestClient

from src.api.app import get_app
from src.api.database.session import get_repo

app = get_app()
app.dependency_overrides[get_repo] = mocked_database

client = TestClient(app)
