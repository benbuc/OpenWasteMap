"""
Contains the Views for the Accounts app."
"""

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django_email_verification import sendConfirm

from waste_samples.models import WasteSample

from .forms import RegistrationForm
from .models import OWMUser, user_is_verified
from .decorators import verified_account_required

@verified_account_required
def profile(request):
    """Render a profile overview for a logged in user."""
    return render(request, 'registration/profile.html', {
        'samples': WasteSample.objects.filter(user=request.user)
    })

def register(request):
    """Used to let new users register on the site."""

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            user_profile = OWMUser.objects.create(user=user)

            if not settings.IS_TEST:
                sendConfirm(user_profile)

            return redirect(reverse('accounts:register_done'))

    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {
        'form': form,
    })

@login_required
def register_done(request):
    """Show a thanks page after successful registration."""
    return render(request, 'registration/register_done.html')

@login_required
def not_verified(request):
    """
    Show a view where users can resend the verification mail
    or change their email address.
    """
    if user_is_verified(request.user):
        return redirect(reverse('accounts:profile'))

    return render(request, 'registration/not_verified.html')
