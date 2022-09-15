import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import BackgroundTasks, HTTPException
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from fastapi_mail.errors import ConnectionErrors
from jose import jwt

from app.core.config import settings

if settings.EMAILS_ENABLED:
    email_conn_config = ConnectionConfig(
        MAIL_USERNAME=settings.SMTP_USER,
        MAIL_PASSWORD=settings.SMTP_PASSWORD,
        MAIL_FROM=settings.SMTP_USER,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_HOST,
        MAIL_TLS=settings.SMTP_TLS,
        MAIL_SSL=False,
        VALIDATE_CERTS=False,
        TEMPLATE_FOLDER=Path(settings.EMAIL_TEMPLATES_DIR),
    )

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def send_email_async(
    email_to: str,
    subject: str = "",
    template_name: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=environment,
        subtype="html",
    )
    fm = FastMail(email_conn_config)
    try:
        await fm.send_message(message, template_name=template_name)
    except ConnectionErrors as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="email sending failed")


def send_email_background(
    background_tasks: BackgroundTasks,
    email_to: str,
    subject: str = "",
    template_name: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=environment,
        subtype="html",
    )
    fm = FastMail(email_conn_config)
    background_tasks.add_task(fm.send_message, message, template_name=template_name)


def send_test_email(email_to: str, background_tasks: BackgroundTasks) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"

    send_email_background(
        background_tasks=background_tasks,
        email_to=email_to,
        subject=subject,
        template_name="test_email.html",
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )

    return


async def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    await send_email_async(
        email_to=email_to,
        subject=subject,
        template_name="reset_password.html",
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "aud": "password_reset"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"], audience="password_reset"
        )
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def send_email_verification(
    email_to: str, nickname: str, token: str, background_tasks: BackgroundTasks
) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Verify e-mail"
    server_host = settings.SERVER_HOST
    link = f"{server_host}/verify-email?token={token}"
    send_email_background(
        background_tasks=background_tasks,
        email_to=email_to,
        subject=subject,
        template_name="verify_email.html",
        environment={"project_name": project_name, "nickname": nickname, "link": link},
    )


def generate_email_verification_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email, "aud": "email_verification"},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_email_verification_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            audience="email_verification",
        )
        return decoded_token["sub"]
    except jwt.JWTError:
        return None
