"""
Containing helper functions for running tests.
"""

from django.contrib.auth import get_user_model

def get_testuser():
    """Return a testuser and credentials."""
    credentials = {
        'username'  : 'testuser',
        'email'     : 'mail@example.com',
        'password'  : 'MySup3erSecretK3Y',
    }
    user = get_user_model().objects.create_user(**credentials)
    return (user, credentials)
