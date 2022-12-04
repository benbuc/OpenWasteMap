from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cached_tile import CachedTile
from app.schemas.tile_cache import Tile


class TileCache:
    """
    Handling the tile cache database.
    """

    def __init__(self, model):
        self.model = model

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

    def updated_tile(self, db: Session, tile: Tile):
        """
        A tile was updated, so reset the outdated flag.
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
            cached_tile.change_count = 0
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


tilecache = TileCache(CachedTile)
