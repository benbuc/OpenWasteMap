"""
Contains the views for the Map Viewer app."
"""

from django.shortcuts import render

# Create your views here.
def index(request):
    """The Map Viewers index view."""

    return render(request, 'map_viewer/index.html')
