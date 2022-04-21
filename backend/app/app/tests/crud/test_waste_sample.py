from random import randint, random

from sqlalchemy.orm import Session

from app import crud
from app.schemas.waste_sample import WasteSampleCreate, WasteSampleUpdate
from app.tests.utils.user import create_random_user


def test_create_waste_sample(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id
    )
    assert waste_sample.waste_level == waste_level
    assert waste_sample.latitude == latitude
    assert waste_sample.longitude == longitude
    assert waste_sample.owner_id == user.id


def test_get_waste_sample(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id
    )
    stored_waste_sample = crud.waste_sample.get(db=db, id=waste_sample.id)
    assert stored_waste_sample
    assert waste_sample.waste_level == stored_waste_sample.waste_level
    assert waste_sample.latitude == stored_waste_sample.latitude
    assert waste_sample.longitude == stored_waste_sample.longitude
    assert waste_sample.id == waste_sample.id
    assert waste_sample.owner_id == waste_sample.owner_id


def test_update_waste_sample(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id
    )
    waste_level2 = randint(0, 10)
    waste_sample_update = WasteSampleUpdate(waste_level=waste_level2)
    waste_sample2 = crud.waste_sample.update(
        db=db, db_obj=waste_sample, obj_in=waste_sample_update
    )
    assert waste_sample.id == waste_sample2.id
    assert waste_sample.latitude == waste_sample2.latitude
    assert waste_sample.longitude == waste_sample2.longitude
    assert waste_sample2.waste_level == waste_level2
    assert waste_sample.owner_id == waste_sample2.owner_id


def test_delete_waste_sample(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id
    )
    waste_sample2 = crud.waste_sample.remove(db=db, id=waste_sample.id)
    waste_sample3 = crud.waste_sample.get(db=db, id=waste_sample.id)
    assert waste_sample3 is None
    assert waste_sample2.id == waste_sample.id
    assert waste_sample2.waste_level == waste_level
    assert waste_sample2.latitude == latitude
    assert waste_sample2.longitude == longitude
    assert waste_sample2.owner_id == user.id


def test_get_waste_sample_in_range(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = 45.0
    longitude = 45.0

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id
    )
    stored_waste_samples = crud.waste_sample.get_multi_in_range(
        db=db,
        min_lat=latitude - 1,
        max_lat=latitude + 1,
        min_lon=longitude - 1,
        max_lon=longitude + 1,
    )
    assert stored_waste_samples
    assert waste_sample.id in [s.id for s in stored_waste_samples]


def test_get_waste_sample_outside_range(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = 45.0
    longitude = 45.0

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    crud.waste_sample.create_with_owner(db=db, obj_in=waste_sample_in, owner_id=user.id)
    stored_waste_samples = crud.waste_sample.get_multi_in_range(
        db=db,
        min_lat=latitude - 2,
        max_lat=latitude - 1,
        min_lon=longitude - 1,
        max_lon=longitude + 1,
    )
    assert not stored_waste_samples
