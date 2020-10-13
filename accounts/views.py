"""
Contains the Views for the Accounts app."
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    """Render a profile overview for a logged in user."""
    return render(request, 'registration/profile.html')
