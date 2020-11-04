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

class EmailChangeForm(forms.Form):
    """
    Allow users to set a new email address.

    The Email then has to be verified.
    """
    error_messages = {
        'email_exists': 'The email address already exists.',
    }
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'})
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_email(self):
        """Make sure the email is not yet used."""
        email = self.cleaned_data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )

        return email

    def save(self, commit=True):
        """Save new Email."""
        self.user.email = self.cleaned_data['email']

        if commit:
            self.user.save()

        return self.user
