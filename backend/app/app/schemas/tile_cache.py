from pydantic import BaseModel


class Tile(BaseModel):
    zoom: int
    xcoord: int
    ycoord: int
