"""
Views from the Tile Server App.
"""

from django.http.response import HttpResponse

from .render import TileRenderer

def index(request):
    """Return empty response"""
    return HttpResponse()

def tile(request, zoom, xcoord, ycoord):
    """Return the Tile at requested coordinates."""

    response = HttpResponse(content_type="image/png")
    TileRenderer(zoom, xcoord, ycoord).render().save(response, "PNG")
    return response
