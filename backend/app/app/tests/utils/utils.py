import random
import string
from datetime import datetime, timedelta
from typing import Dict

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=16))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_datetime() -> datetime:
    now = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    delta = now - epoch
    random_delta = random.randint(0, int(delta.total_seconds()))
    return now - timedelta(seconds=random_delta)


def get_superuser_token_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
