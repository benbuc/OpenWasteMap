import asyncio
import logging

from app.api import deps
from app.core.celery_app import celery_app
from app.tile_cache import tilecache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TileCacheRenderOutdated:
    def __init__(self):
        self.db = next(deps.get_db())
        self.tiles_in_progress = {}
        self.tiles_to_render = []

    def fetch_outdated_tiles(self):
        outdated_tiles = tilecache.get_outdated_tiles(self.db)
        self.tiles_to_render = [
            tile for tile in outdated_tiles if tile not in self.tiles_in_progress
        ]

    def start_rendering_tasks(self):
        for tile in self.tiles_to_render:
            self.tiles_in_progress[tile] = celery_app.send_task(
                "app.worker.render_tile", args=[tile.zoom, tile.xcoord, tile.ycoord]
            )

    def check_tiles_in_progress(self):
        # TODO: do we need to include a timeout here?
        for tile, task in self.tiles_in_progress.copy().items():
            if task.state == "SUCCESS":
                del self.tiles_in_progress[tile]
            elif task.state == "FAILURE":
                logger.error(f"Failed to render tile {tile}")
                del self.tiles_in_progress[tile]

    async def mainloop(self):
        while True:
            self.fetch_outdated_tiles()
            if self.tiles_to_render:
                self.start_rendering_tasks()

            if self.tiles_in_progress:
                self.check_tiles_in_progress()

            if not self.tiles_to_render and not self.tiles_in_progress:
                # Nothig to do at the moment, sleep a little longer
                await asyncio.sleep(60)
            else:
                # Some tiles are still being rendered, sleep a little shorter
                await asyncio.sleep(1)
