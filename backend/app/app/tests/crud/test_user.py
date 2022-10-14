from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_email, random_lower_string


def test_create_user(db: Session) -> None:
    email = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, nickname=nickname, password=password)
    datetime_before = datetime.utcnow()
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email
    assert user.nickname == nickname
    assert user.email_verified is False
    assert hasattr(user, "hashed_password")
    # Check the join date is reasonably close
    assert 0 < (user.date_joined - datetime_before).total_seconds() <= 1


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, nickname=nickname, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email
    assert user.nickname == authenticated_user.nickname
    assert authenticated_user.email_verified is False


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    user = create_random_user(db)
    is_active = crud.user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(
        email=email, nickname=nickname, password=password, disabled=True
    )
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active


def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    nickname = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(email=email, nickname=nickname, password=password)
    user = crud.user.create(db, obj_in=user_in)
    user = crud.user.update_is_superuser(db, db_obj=user, new_is_superuser=True)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    user = create_random_user(db)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    nickname = random_lower_string()
    email = random_email()
    user_in = UserCreate(
        email=email, nickname=nickname, password=password, is_superuser=True
    )
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert user.nickname == user_2.nickname
    assert user.date_joined == user_2.date_joined
    assert user.email_verified == user_2.email_verified
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    nickname = random_lower_string()
    email = random_email()
    user_in = UserCreate(
        email=email, nickname=nickname, password=password, is_superuser=True
    )
    user = crud.user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert user.nickname == user_2.nickname
    assert user.date_joined == user_2.date_joined
    assert verify_password(new_password, user_2.hashed_password)


def test_update_user_without_password(db: Session) -> None:
    password = random_lower_string()
    nickname = random_lower_string()
    full_name = random_lower_string()
    email = random_email()
    user_in = UserCreate(
        email=email,
        nickname=nickname,
        full_name=full_name,
        password=password,
        is_superuser=True,
    )
    user = crud.user.create(db, obj_in=user_in)
    new_full_name = random_lower_string()
    user_in_update = UserUpdate(full_name=new_full_name)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user_2.full_name == new_full_name


def test_get_all_users(db: Session) -> None:
    users = [create_random_user(db) for _ in range(3)]
    all_users = crud.user.get_all(db)
    for user in users:
        assert user in all_users


def test_check_if_user_email_verified(db: Session) -> None:
    user = create_random_user(db)
    is_email_verified = crud.user.is_email_verified(user)
    assert is_email_verified is True


def test_check_if_user_not_email_verified(db: Session) -> None:
    user = create_random_user(db, verify_email=False)
    is_email_verified = crud.user.is_email_verified(user)
    assert is_email_verified is False


def test_update_user_email_verified(db: Session) -> None:
    user = create_random_user(db, verify_email=False)
    stored_user_1 = crud.user.get(db, id=user.id)
    assert stored_user_1.email_verified is False
    crud.user.update_email_verified(db, db_obj=user, new_email_verified=True)
    stored_user_2 = crud.user.get(db, id=user.id)
    assert stored_user_2.email_verified is True


def test_username_email_forced_lowercase(db: Session) -> None:
    email = random_email().upper()
    nickname = random_lower_string().upper()
    password = random_lower_string()
    user_in = UserCreate(email=email, nickname=nickname, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email.lower()
    assert user.nickname == nickname.lower()
