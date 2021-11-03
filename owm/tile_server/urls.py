"""
URLconf for the Tile Server App.
"""

from django.urls import path

from . import views

app_name = "tile_server"  # pylint: disable=invalid-name
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:zoom>/<int:xcoord>/<int:ycoord>.png", views.tile, name="tile"),
]
