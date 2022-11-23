from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import verify_password
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string
from app.utils import generate_email_verification_token, generate_password_reset_token


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_reset_password_correct_token(client: TestClient, db: Session) -> None:
    user = create_random_user(db)
    password_reset_token = generate_password_reset_token(email=user.email)
    new_password = random_lower_string()
    r = client.post(
        f"{settings.API_V1_STR}/reset-password",
        json={"token": password_reset_token, "new_password": new_password},
    )
    assert r.status_code == 200
    db.refresh(user)
    assert verify_password(new_password, user.hashed_password)


def test_verify_email_correct_token(client: TestClient, db: Session) -> None:
    user = create_random_user(db, verify_email=False)
    assert user.email_verified is False
    email_verification_token = generate_email_verification_token(email=user.email)
    r = client.post(
        f"{settings.API_V1_STR}/verify-email", json={"token": email_verification_token}
    )
    assert r.status_code == 200
    db.refresh(user)
    assert user.email_verified is True
