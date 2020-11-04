"""
Custom Models for the Accounts App.
"""

from django.contrib.auth import get_user_model
from django.db import models

def user_is_verified(user):
    """Returns True if the user has a verified email address."""
    try:
        return user.owmuser.email_verified
    except OWMUser.DoesNotExist:
        OWMUser.objects.create(user=user)
        return False

class OWMUser(models.Model):
    """
    Profile model for the standard Django user model.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
