"""
Containing helper functions for running tests.
"""

from accounts.models import OWMUser
from django.contrib.auth import get_user_model


def get_testuser(
    email_verified=True,
    username="testuser",
    email="mail@example.com",
    password="MySup3erSecretK3Y",
):
    """
    Return a testuser and credentials.
    Users email is verified per default.
    """

    credentials = {
        "username": username,
        "email": email,
        "password": password,
    }
    user = get_user_model().objects.create_user(**credentials)
    OWMUser.objects.create(user=user, email_verified=email_verified)
    return (user, credentials)
