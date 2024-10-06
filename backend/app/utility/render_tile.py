from app.rendering.render import TileRenderer
from PIL import Image
import cProfile


def render_tile(zoom: int, xcoord: int, ycoord: int) -> Image:
    renderer = TileRenderer(zoom, xcoord, ycoord)
    rendered_tile = renderer.render()

    return rendered_tile


if __name__ == "__main__":
    # cProfile.run("render_tile(2, 3, 1)", sort="cumtime")
    render_tile(0, 0, 0).save("tile.png")
