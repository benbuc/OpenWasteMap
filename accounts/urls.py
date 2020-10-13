"""
URLconf for the Accounts app."
"""

from django.urls import path, include
from . import views

app_name = 'accounts' # pylint: disable=invalid-name
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
]
