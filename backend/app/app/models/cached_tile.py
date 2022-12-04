from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer

from app.db.base_class import Base

if TYPE_CHECKING:
    from .waste_sample import WasteSample  # noqa: F401


class CachedTile(Base):
    zoom = Column(Integer, primary_key=True, index=True, nullable=False)
    xcoord = Column(Integer, primary_key=True, index=True, nullable=False)
    ycoord = Column(Integer, primary_key=True, index=True, nullable=False)
    change_count = Column(Integer, nullable=False, default=0)
