from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class WasteSample(Base):
    id = Column(Integer, primary_key=True, index=True)
    waste_level = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner = relationship("User", back_populates="waste_samples")
    sampling_date = Column(DateTime)  # stored in UTC
