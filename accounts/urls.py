"""
URLconf for the Accounts app."
"""

from django.urls import path, include
from . import views

app_name = 'accounts' # pylint: disable=invalid-name
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.profile, name='profile'),
    path('profile/verify', views.not_verified, name='not_verified'),
    path('register/', views.register, name='register'),
    path('register/done', views.register_done, name='register_done'),
]
