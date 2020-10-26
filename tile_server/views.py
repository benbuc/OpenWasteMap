"""
Vies from the Tile Server App.
"""

from PIL import Image

from django.http.response import HttpResponse

def index(request):
    """Return empty response"""
    return HttpResponse()

def tile(request, zoom, xcoord, ycoord):
    """Return the Tile at requested coordinates."""

    red = Image.new('RGBA', (256, 256), (zoom, xcoord, ycoord, 128))
    response = HttpResponse(content_type="image/png")
    red.save(response, "PNG")
    return response
