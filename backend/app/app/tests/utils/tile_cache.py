from sqlalchemy.orm import Session

from app.tile_cache import tilecache


def create_random_tile(db: Session, outdated: bool = False):
    tilecache.updated_tile(db)
    if outdated:
        tilecache.increment_tile_change_count(db)
