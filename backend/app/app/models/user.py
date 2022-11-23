from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .waste_sample import WasteSample  # noqa: F401


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nickname = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    email_verified = Column(Boolean(), default=False)
    waste_samples = relationship("WasteSample", back_populates="owner")
    date_joined = Column(DateTime)  # stored in UTC
