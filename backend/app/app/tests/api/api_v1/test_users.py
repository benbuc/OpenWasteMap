from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app.core.config import settings
from app.schemas.user import UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_users_superuser_me(
    client: TestClient, superuser_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER
    assert current_user["nickname"] == settings.FIRST_SUPERUSER_NICKNAME
    assert current_user["date_joined"]


def test_get_users_normal_user_me(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me", headers=normal_user_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is False
    assert current_user["email"] == settings.EMAIL_TEST_USER
    assert current_user["date_joined"]


def test_create_user_new_email(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "nickname": nickname, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.user.get_by_email(db, email=username)
    assert user
    assert user.email == created_user["email"]
    assert user.nickname == created_user["nickname"]
    assert user.date_joined.isoformat() == created_user["date_joined"]


def test_get_existing_user(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, nickname=nickname, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_email(db, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]
    assert existing_user.nickname == api_user["nickname"]
    assert existing_user.date_joined.isoformat() == api_user["date_joined"]


def test_get_existing_user_nickname(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, nickname=nickname, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}", headers=superuser_token_headers,
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.user.get_by_nickname(db, nickname=nickname)
    assert existing_user
    assert existing_user.email == api_user["email"]
    assert existing_user.nickname == api_user["nickname"]
    assert existing_user.date_joined.isoformat() == api_user["date_joined"]


def test_create_user_existing_username(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    # username = email
    nickname1 = random_lower_string()
    nickname2 = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, nickname=nickname1, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": username, "nickname": nickname2, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_existing_nickname(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username1 = random_email()
    username2 = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username1, nickname=nickname, password=password)
    crud.user.create(db, obj_in=user_in)
    data = {"email": username2, "nickname": nickname, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=superuser_token_headers, json=data,
    )
    created_user = r.json()
    assert r.status_code == 400
    assert "_id" not in created_user


def test_create_user_by_normal_user(
    client: TestClient, normal_user_token_headers: Dict[str, str]
) -> None:
    username = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    data = {"email": username, "nickname": nickname, "password": password}
    r = client.post(
        f"{settings.API_V1_STR}/users/", headers=normal_user_token_headers, json=data,
    )
    assert r.status_code == 400


def test_retrieve_users(
    client: TestClient, superuser_token_headers: dict, db: Session
) -> None:
    username = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=username, nickname=nickname, password=password)
    crud.user.create(db, obj_in=user_in)

    username2 = random_email()
    nickname2 = random_lower_string()
    password2 = random_lower_string()
    user_in2 = UserCreate(email=username2, nickname=nickname2, password=password2)
    crud.user.create(db, obj_in=user_in2)

    r = client.get(f"{settings.API_V1_STR}/users/", headers=superuser_token_headers)
    all_users = r.json()

    assert len(all_users) > 1
    for item in all_users:
        assert "email" in item
        assert "nickname" in item
        assert "date_joined" in item
