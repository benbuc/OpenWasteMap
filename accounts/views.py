"""
Contains the Views for the Accounts app."
"""

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django_email_verification import sendConfirm

from waste_samples.models import WasteSample

from .forms import RegistrationForm
from .models import OWMUser

@login_required
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
            OWMUser.objects.create(user=user)

            if not settings.IS_TEST:
                sendConfirm(user)

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
