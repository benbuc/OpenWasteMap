"""
Contains the Views for the Accounts app."
"""

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm

@login_required
def profile(request):
    """Render a profile overview for a logged in user."""
    return render(request, 'registration/profile.html')

def register(request):
    """Used to let new users register on the site."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def register_done(request):
    """Show a thanks page after successful registration."""
    render(request, 'registration/register_done.html')
