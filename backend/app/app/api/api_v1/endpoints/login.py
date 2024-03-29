from datetime import timedelta
from typing import Any

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils import (
    generate_email_verification_token,
    generate_password_reset_token,
    send_email_verification,
    send_reset_password_email,
    verify_email_verification_token,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=schemas.Msg)
async def recover_password(email: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = crud.user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    await send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password", response_model=schemas.Msg)
def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    crud.user.update(db, db_obj=user, obj_in=schemas.UserUpdate(password=new_password))
    return {"msg": "Password updated successfully"}


@router.post("/verify-email", response_model=schemas.Msg)
def verify_email(
    token: str = Body(..., embed=True), db: Session = Depends(deps.get_db)
) -> Any:
    """
    Verify e-mail address
    """
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    crud.user.update_email_verified(db, db_obj=user, new_email_verified=True)
    return {"msg": "E-mail verified"}


@router.post("/resend-verification", response_model=schemas.Msg)
def resend_email_verification(
    background_tasks: BackgroundTasks,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    if current_user.email_verified:
        raise HTTPException(status_code=400, detail="Email address already verified.")

    email_verification_token = generate_email_verification_token(
        email=current_user.email
    )
    send_email_verification(
        background_tasks=background_tasks,
        email_to=current_user.email,
        nickname=current_user.nickname,
        token=email_verification_token,
    )

    return {"msg": "Re-sent email verification"}
