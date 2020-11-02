"""
Containing helper functions for running tests.
"""

from django.contrib.auth import get_user_model
from accounts.models import OWMUser

def get_testuser(email_verified=True):
    """
    Return a testuser and credentials.
    Users email is verified per default.
    """

    credentials = {
        'username'  : 'testuser',
        'email'     : 'mail@example.com',
        'password'  : 'MySup3erSecretK3Y',
    }
    user = get_user_model().objects.create_user(**credentials)
    OWMUser.objects.create(user=user, email_verified=email_verified)
    return (user, credentials)
