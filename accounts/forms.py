"""
Contains different subclasses of formulars.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class RegistrationForm(UserCreationForm):
    #pylint: disable=too-few-public-methods
    """The form used for user registration on the site."""
    first_name  = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name   = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email       = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.'
    )

    class Meta:
        """RegistrationForms metadata."""
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )