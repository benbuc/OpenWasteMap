from typing import Any, List

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core.config import settings
from app.utils import generate_email_verification_token, send_email_verification

router = APIRouter()


@router.get("", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.

    Set limit to 0 to retrieve all users.
    """
    if limit:
        users = crud.user.get_multi(db, skip=skip, limit=limit)
    else:
        users = crud.user.get_all(db)
    return users


@router.post("", response_model=schemas.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    background_tasks: BackgroundTasks,
) -> Any:
    """
    Create new user.
    """
    user_with_email = crud.user.get_by_email(db, email=user_in.email)
    user_with_nickname = crud.user.get_by_nickname(db, nickname=user_in.nickname)
    if user_with_email:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    if user_with_nickname:
        raise HTTPException(
            status_code=400,
            detail="The user with this nickname already exists in the system.",
        )
    user = crud.user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        email_verification_token = generate_email_verification_token(
            email=user_in.email
        )
        send_email_verification(
            background_tasks=background_tasks,
            email_to=user_in.email,
            nickname=user_in.nickname,
            token=email_verification_token,
        )

    return user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
def read_user_me(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/{user_id}", response_model=schemas.User)
def read_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = crud.user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    return user
