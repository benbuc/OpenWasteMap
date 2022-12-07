from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Tile(BaseModel):
    zoom: int
    xcoord: int
    ycoord: int
    last_refresh: Optional[datetime] = None
