"""
Admin Page for Accounts App.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import OWMUser


class OWMUserInline(admin.StackedInline):
    """OWMUser inline admin descriptor."""

    model = OWMUser
    can_delete = False


class UserAdmin(BaseUserAdmin):
    """New User Admin."""

    inlines = (OWMUserInline,)


admin.site.unregister(get_user_model())
admin.site.register(get_user_model(), UserAdmin)
