import logging
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from sqlalchemy.orm import Session
from tenacity import retry, retry_if_result, stop_after_delay, wait_fixed

from app.db.session import SessionLocal
from app.models.cached_tile import CachedTile
from app.rendering.utilities import tiles_affected_by_sample
from app.schemas.tile_cache import Tile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TileCache:
    """
    Handling the tile cache database.
    """

    def __init__(self, model):
        self.model = model
        self.base_path = Path("/tiles")

    def get_tile(self, db: Session, tile: Tile) -> Optional[CachedTile]:
        """
        Get a tile from the database.
        None if it doesn't exist.
        """
        cached_tile = (
            db.query(self.model)
            .filter(
                self.model.zoom == tile.zoom,
                self.model.xcoord == tile.xcoord,
                self.model.ycoord == tile.ycoord,
            )
            .first()
        )
        return cached_tile

    def updated_tile(self, db: Session, tile: Tile, prior_change_count: int):
        """
        A tile was updated, so reset the outdated flag and refresh time.
        If it doesn't exist in the database, create it.
        """
        cached_tile = (
            db.query(self.model)
            .filter(
                self.model.zoom == tile.zoom,
                self.model.xcoord == tile.xcoord,
                self.model.ycoord == tile.ycoord,
            )
            .first()
        )
        if cached_tile is None:
            cached_tile = self.model(
                zoom=tile.zoom, xcoord=tile.xcoord, ycoord=tile.ycoord
            )
            db.add(cached_tile)
            db.commit()
            db.refresh(cached_tile)
        else:
            cached_tile.change_count -= prior_change_count
            cached_tile.last_refresh = datetime.utcnow()
            db.commit()
            db.refresh(cached_tile)

    def get_outdated_tiles(self, db: Session) -> List[Tile]:
        """
        Get the list of outdated tiles.
        """
        outdated_tiles = (
            db.query(self.model)
            .filter(self.model.change_count > 0)
            .order_by(self.model.change_count.desc())
            .all()
        )
        return outdated_tiles

    def increment_tile_change_count(self, db: Session, tile: Tile):
        """
        Increment the change count of a tile.
        """
        # TODO: I don't yet understand this fully. Is this prone to race conditions?
        cached_tile = (
            db.query(self.model)
            .filter(
                self.model.zoom == tile.zoom,
                self.model.xcoord == tile.xcoord,
                self.model.ycoord == tile.ycoord,
            )
            .first()
        )

        # If tile is not in the cache we don't need to outdate it
        if cached_tile is not None:
            cached_tile.change_count += 1
            db.commit()
            db.refresh(cached_tile)

    def increment_tiles_at_coordinate(self, db: Session, latitude: int, longitude: int):
        for tile in tiles_affected_by_sample(latitude, longitude):
            self.increment_tile_change_count(db, tile)

    def path_for_tile(self, tile: Tile):
        return (
            self.base_path
            / str(tile.zoom)
            / str(tile.xcoord)
            / f"{str(tile.ycoord)}.png"
        )

    def is_on_disk(self, tile: Tile):
        return self.path_for_tile(tile).exists()

    @retry(
        stop=stop_after_delay(10),
        wait=wait_fixed(0.2),
        retry=retry_if_result(lambda x: x is False),
    )
    async def wait_for_tile_on_disk(self, tile: Tile):
        return self.is_on_disk(tile)

    @retry(
        stop=stop_after_delay(30),
        wait=wait_fixed(1),
        retry=retry_if_result(lambda x: x is False),
    )
    async def wait_for_tile_refresh(self, tile: Tile):
        with SessionLocal() as db:
            cached_tile = self.get_tile(db, tile)
            if cached_tile is None:
                return False
            if tile.last_refresh is None:
                return cached_tile.last_refresh is not None
            elif cached_tile.last_refresh is None:
                return False
            else:
                return cached_tile.last_refresh > tile.last_refresh


tilecache = TileCache(CachedTile)
