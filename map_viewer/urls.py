"""
URLconf for the Map Viewer app.
"""

from django.urls import path

from . import views

app_name = "map_viewer"  # pylint: disable=invalid-name
urlpatterns = [
    path("", views.index, name="index"),
]
