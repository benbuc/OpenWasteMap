"""
The Django Admin configuration for waste samples.
"""

from django.contrib import admin

from .models import WasteSample

admin.site.register(WasteSample)
