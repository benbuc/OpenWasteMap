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
    path('email_change/', views.email_change, name='email_change'),
    path('email_change/done', views.email_change_done, name='email_change_done'),
    path('resend_confirmation/', views.resend_confirmation, name='resend_confirmation'),
]
