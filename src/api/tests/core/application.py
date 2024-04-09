from fastapi.testclient import TestClient

import os
import sys

current_dir = os.path.join(os.getcwd())
sys.path.append(current_dir)

from src.api.app import get_app
from src.api.database.session import get_db
from core.mocked_database import mocked_database

app = get_app()
app.dependency_overrides[get_db] = mocked_database

client = TestClient(app)