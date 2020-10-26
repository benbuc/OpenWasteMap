"""
Views from the Tile Server App.
"""

from django.http.response import HttpResponse

from .render_tile import get_tile

def index(request):
    """Return empty response"""
    return HttpResponse()

def tile(request, zoom, xcoord, ycoord):
    """Return the Tile at requested coordinates."""

    response = HttpResponse(content_type="image/png")
    get_tile(zoom, xcoord, ycoord).save(response, "PNG")
    return response
