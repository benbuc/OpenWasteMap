from typing import Optional

from pydantic import BaseModel


# Shared properties
class WasteSampleBase(BaseModel):
    waste_level: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


# Properties to receive on waste sample creation
class WasteSampleCreate(WasteSampleBase):
    waste_level: int
    latitude: float
    longitude: float


# Properties to receive on waste sample update
class WasteSampleUpdate(WasteSampleBase):
    pass


# Properties shared by models stored in DB
class WasteSampleInDBBase(WasteSampleBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Properties to return to client
class WasteSample(WasteSampleInDBBase):
    pass


# Properties properties stored in DB
class WasteSampleInDB(WasteSampleInDBBase):
    pass
