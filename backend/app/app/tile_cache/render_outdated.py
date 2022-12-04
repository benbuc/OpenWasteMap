import asyncio
import logging

from sqlalchemy.orm import Session

from app.api import deps
from app.tile_cache import tilecache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def get_outdated_tiles(db: Session):
    pass


def render_outdated(db: Session):
    outdated_tiles = tilecache.get_outdated_tiles(db)
    logging.info(f"Rendering {len(outdated_tiles)} tiles")


async def mainloop():
    """Main loop to render outdated tiles."""
    db = next(deps.get_db())
    while True:
        # Get the list of outdated tiles
        # outdated_tiles = get_outdated_tiles()
        # Get the list of tiles to render
        # tiles_to_render = get_tiles_to_render(outdated_tiles)
        # Render the tiles
        # render_tiles(tiles_to_render)
        # Update the database
        # update_database(tiles_to_render)
        render_outdated(db)

        # Nothing to do, sleep for a while
        await asyncio.sleep(1)
