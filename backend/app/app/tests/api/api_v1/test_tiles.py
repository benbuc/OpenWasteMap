import io

from fastapi.testclient import TestClient
from PIL import Image
from PIL.PngImagePlugin import PngImageFile

from app.tests.utils.tile import get_tile_url


def test_tiles_accessible(client: TestClient) -> None:
    response = client.get(get_tile_url())
    assert response.status_code == 200


def test_tiles_serves_image(client: TestClient) -> None:
    response = client.get(get_tile_url())
    assert response.status_code == 200
    im = Image.open(io.BytesIO(response.content))
    assert type(im) is PngImageFile
