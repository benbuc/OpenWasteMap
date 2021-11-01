"""
Decorators for Accounts app.
"""

from django.contrib.auth.decorators import login_required, user_passes_test

from .models import user_is_verified


def verified_account_required(function):
    """
    Decorator for views that checks that the user is logged in
    and the email address is verified.
    Redirects to the verification page if not.
    """

    actual_decorator = user_passes_test(
        user_is_verified,
        login_url="accounts:not_verified",
        redirect_field_name=None,
    )
    return login_required(actual_decorator(function))


def disallow_logged_in(function):
    """
    Decorator for views that checks that the user is not
    logged in. Otherwise redirects to the profile page.
    """

    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url="accounts:profile",
        redirect_field_name=None,
    )
    return actual_decorator(function)
