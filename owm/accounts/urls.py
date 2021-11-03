"""
URLconf for the Accounts app."
"""

from django.contrib.auth import views as auth_views
from django.urls import include, path, reverse_lazy

from . import views

app_name = "accounts"  # pylint: disable=invalid-name
urlpatterns = [
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            success_url=reverse_lazy("accounts:password_reset_done")
        ),
        name="password_reset",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("accounts:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path("", include("django.contrib.auth.urls")),
    path("profile/", views.profile, name="profile"),
    path("profile/verify", views.not_verified, name="not_verified"),
    path("register/", views.register, name="register"),
    path("register/done", views.register_done, name="register_done"),
    path("email_change/", views.email_change, name="email_change"),
    path("email_change/done", views.email_change_done, name="email_change_done"),
    path("resend_confirmation/", views.resend_confirmation, name="resend_confirmation"),
]
