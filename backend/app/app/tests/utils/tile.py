from app.core.config import settings


def get_tile_url(x: int = 0, y: int = 0, z: int = 0) -> str:
    return f"{settings.API_V1_STR}/tiles/{x}/{y}/{z}.png"
