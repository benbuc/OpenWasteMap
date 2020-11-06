"""
Contains the views for the Map Viewer app."
"""

from django.shortcuts import render
from django.conf import settings

def index(request):
    """The Map Viewers index view."""

    return render(request, 'map_viewer/index.html', {'owm_version': settings.OWM_VERSION})
