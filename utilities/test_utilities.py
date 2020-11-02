"""
Containing helper functions for running tests.
"""

from django.contrib.auth import get_user_model
from accounts.models import OWMUser

def get_testuser():
    """Return a testuser and credentials."""
    credentials = {
        'username'  : 'testuser',
        'email'     : 'mail@example.com',
        'password'  : 'MySup3erSecretK3Y',
    }
    user = get_user_model().objects.create_user(**credentials)
    OWMUser.objects.create(user=user)
    return (user, credentials)
