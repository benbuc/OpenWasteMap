import io
from pathlib import Path

from raven import Client

from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal
from app.rendering.render import TileRenderer
from app.schemas.tile_cache import Tile
from app.tile_cache import tilecache

client_sentry = Client(settings.SENTRY_DSN)


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task(time_limit=60)
def render_tile(zoom: int, xcoord: int, ycoord: int) -> str:
    with SessionLocal() as db:
        # TODO: can we reuse database connection?
        tilecache.updated_tile(db, Tile(zoom=zoom, xcoord=xcoord, ycoord=ycoord))

    image_out = io.BytesIO()
    rendered_tile = TileRenderer(zoom, xcoord, ycoord).render()
    rendered_tile.save(image_out, "png")

    tile_path = Path("/tiles") / str(zoom) / str(xcoord) / f"{ycoord}.png"
    tile_path.parent.mkdir(parents=True, exist_ok=True)
    with open(tile_path, "wb") as f:
        f.write(image_out.getvalue())


celery_app.autodiscover_tasks(["app.backup"])
