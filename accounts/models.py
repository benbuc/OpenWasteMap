"""
Custom Models for the Accounts App.
"""

from django.contrib.auth import get_user_model
from django.db import models

class OWMUser(models.Model):
    """
    Profile model for the standard Django user model.
    """

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    email_verified = models.BooleanField(default=False)
