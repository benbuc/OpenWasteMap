import asyncio
import logging

from tenacity import RetryError

from app.core.celery_app import celery_app
from app.db.session import SessionLocal
from app.tile_cache import tilecache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TileCacheRenderOutdated:
    def __init__(self):
        self.tiles_in_progress = set()
        self.tiles_to_render = []

        # used to keep a strong reference to tasks
        # See: https://docs.python.org/3/library/asyncio-task.html#asyncio.create_task
        self.active_tasks = set()

    def fetch_outdated_tiles(self):
        """Fetch all tiles that are not currently rendering."""
        with SessionLocal() as db:
            outdated_tiles = tilecache.get_outdated_tiles(db)
        self.tiles_to_render = [
            tile for tile in outdated_tiles if tile not in self.tiles_in_progress
        ]

    async def render_tile(self, tile):
        try:
            celery_app.send_task(
                "app.worker.render_tile", args=[tile.zoom, tile.xcoord, tile.ycoord]
            )
            await tilecache.wait_for_tile_refresh(tile)
        except RetryError:
            logger.error(f"Timed out waiting for tile: f{tile}. Can be queued again.")
        finally:
            self.tiles_in_progress.discard(tile)

    def enqueue_rendering_tasks(self):
        for tile in self.tiles_to_render:
            self.tiles_in_progress.add(tile)

            task = asyncio.create_task(self.render_tile(tile))
            self.active_tasks.add(task)
            task.add_done_callback(self.active_tasks.discard)

    async def main(self):
        self.fetch_outdated_tiles()
        self.enqueue_rendering_tasks()

        await asyncio.sleep(60)

    async def mainloop(self):
        while True:
            try:
                await self.main()
            except Exception as e:
                logger.error(f"Error in mainloop: {e}")
