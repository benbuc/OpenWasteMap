"""
Contains different subclasses of formulars.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class RegistrationForm(UserCreationForm):
    """The form used for user registration on the site."""
    first_name  = forms.CharField(max_length=30, required=False, help_text="Optional.")
    last_name   = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email       = forms.EmailField(
        max_length=254,
        help_text='Required. Enter a valid email address.'
    )

    def clean_email(self):
        """Clean email to be unique"""

        email = self.cleaned_data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(
                "Email already exists",
                code="email_exists"
            )

        return email

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
