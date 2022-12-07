from sqlalchemy.orm import Session

from app.schemas.tile_cache import Tile
from app.tile_cache import tilecache


def test_increment_change_count(db: Session):
    tile = Tile(zoom=1, xcoord=1, ycoord=1)
    tilecache.updated_tile(db, tile, 0)
    db_tile = tilecache.get_tile(db, tile)
    assert db_tile.change_count == 0

    tilecache.increment_tile_change_count(db, tile)
    db_tile = tilecache.get_tile(db, tile)
    assert db_tile.change_count == 1

    outdated_tiles = tilecache.get_outdated_tiles(db)
    assert db_tile in outdated_tiles
