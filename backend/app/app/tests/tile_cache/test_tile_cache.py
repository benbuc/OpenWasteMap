from sqlalchemy.orm import Session

from app.tests.utils.tile_cache import create_random_tile
from app.tile_cache import tilecache


def test_get_outdated_tiles(db: Session):
    create_random_tile(db, outdated=True)

    outdated_tiles = tilecache.get_outdated_tiles(db)
    assert len(outdated_tiles) > 0
