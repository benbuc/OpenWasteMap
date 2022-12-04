import base64
import io

from raven import Client

from app.core.celery_app import celery_app
from app.core.config import settings
from app.rendering.render import TileRenderer

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def render_tile(zoom: int, xcoord: int, ycoord: int) -> str:
    image_out = io.BytesIO()
    rendered_tile = TileRenderer(zoom, xcoord, ycoord).render()
    rendered_tile.save(image_out, "png")

    return base64.b64encode(image_out.getvalue()).decode()


celery_app.autodiscover_tasks(["app.backup"])
