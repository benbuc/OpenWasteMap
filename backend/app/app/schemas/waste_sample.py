from datetime import datetime
from typing import Optional

from pydantic import BaseModel, confloat, conint


# Shared properties
class WasteSampleBase(BaseModel):
    waste_level: Optional[conint(ge=0, le=10)] = None
    latitude: Optional[confloat(ge=-90.0, le=90.0)] = None
    longitude: Optional[confloat(ge=-180.0, le=180.0)] = None


# Properties to receive on waste sample creation
class WasteSampleCreate(WasteSampleBase):
    waste_level: conint(ge=0, le=10)
    latitude: confloat(ge=-90.0, le=90.0)
    longitude: confloat(ge=-180.0, le=180.0)


# Properties for import and export of multiple samples
class WasteSampleImportExport(WasteSampleCreate):
    owner_nickname: Optional[str]
    sampling_date: datetime


# Properties to receive on waste sample update
class WasteSampleUpdate(WasteSampleBase):
    pass


# Properties shared by models stored in DB
class WasteSampleInDBBase(WasteSampleBase):
    id: int
    owner_id: Optional[int]
    sampling_date: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class WasteSample(WasteSampleInDBBase):
    pass


# Properties properties stored in DB
class WasteSampleInDB(WasteSampleInDBBase):
    pass
