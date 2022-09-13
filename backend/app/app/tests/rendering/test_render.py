import numpy as np
from sqlalchemy.orm import Session

from app.rendering import render
from app.rendering.utilities import (
    num_tiles,
    tile_ynum_from_latitude,
    tiles_affected_by_sample,
)
from app.tests.utils.user import create_random_user
from app.tests.utils.waste_sample import create_waste_sample


def test_color_channels_have_correct_shape():
    levels = np.ones((render.TILE_SIZE, render.TILE_SIZE))
    colors = render.get_color_channels_for_waste_levels(levels)

    assert colors.shape == (render.TILE_SIZE, render.TILE_SIZE, 3)


def test_finds_samples_in_tile(db: Session) -> None:
    user = create_random_user(db)
    create_waste_sample(
        db, owner_id=user.id, waste_level=0, latitude=52.521226, longitude=13.684172
    )
    renderer = render.TileRenderer(13, 4407, 2686, owner_id=user.id)
    assert len(renderer.samples) == 1


def test_ignores_samples_outside_tile(db: Session) -> None:
    user = create_random_user(db)
    create_waste_sample(
        db, owner_id=user.id, waste_level=0, latitude=52.521226, longitude=13.684172
    )
    renderer = render.TileRenderer(13, 0, 0, owner_id=user.id)
    assert len(renderer.samples) == 0


def test_rendering_green(db: Session) -> None:
    user = create_random_user(db)
    create_waste_sample(
        db=db, owner_id=user.id, waste_level=0, latitude=52.521226, longitude=13.684172
    )
    renderer = render.TileRenderer(13, 4407, 2686, owner_id=user.id)
    rendered_image = np.array(renderer.render())
    assert (rendered_image[..., 0] == 0).all()
    assert (rendered_image[..., 1] == 255).any()
    assert (rendered_image[..., 2] == 0).all()


def test_loading_over_coordinate_edges(db: Session) -> None:
    user = create_random_user(db)
    tile_left = (13, 0, int(tile_ynum_from_latitude(13, np.radians(50.0))))
    tile_right = (
        13,
        num_tiles(13) - 1,
        int(tile_ynum_from_latitude(13, np.radians(50))),
    )
    [
        create_waste_sample(
            db, owner_id=user.id, waste_level=0, latitude=50.0, longitude=lon
        )
        for lon in [179.99999, -179.99999]
    ]

    renderer_left = render.TileRenderer(*tile_left, owner_id=user.id)
    renderer_right = render.TileRenderer(*tile_right, owner_id=user.id)

    assert len(renderer_left.samples) == 2
    assert len(renderer_right.samples) == 2


def test_sample_affects_all_zoom_levels():
    zoom_levels = [zoom for (zoom, x, y) in tiles_affected_by_sample(0, 0)]
    for z in range(19):
        assert z in zoom_levels
