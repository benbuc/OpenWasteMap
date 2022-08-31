from datetime import datetime
from random import randint, random

from sqlalchemy.orm import Session

from app import crud
from app.schemas.waste_sample import (
    WasteSampleCreate,
    WasteSampleUpdate,
    WasteSampleImportExport,
)
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_datetime
from app.tests.utils.waste_sample import create_random_waste_sample


def test_create_waste_sample(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90
    sampling_date = datetime.utcnow()

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id, sampling_date=sampling_date
    )
    assert waste_sample.waste_level == waste_level
    assert waste_sample.latitude == latitude
    assert waste_sample.longitude == longitude
    assert waste_sample.owner_id == user.id
    assert waste_sample.sampling_date == sampling_date


def test_create_waste_samples_multi(db: Session) -> None:
    users = [create_random_user(db) for _ in range(2)]
    waste_samples_in = [
        WasteSampleImportExport(
            waste_level=randint(0, 10),
            latitude=random() * 90,
            longitude=random() * 90,
            owner_nickname=users[randint(0, len(users) - 1)].nickname,
            sampling_date=random_datetime(),
        )
        for _ in range(5)
    ]
    waste_sample_ids = crud.waste_sample.create_multi(db=db, obj_in=waste_samples_in)
    assert waste_sample_ids
    assert len(waste_sample_ids) == len(waste_samples_in)
    for sample_in, stored_id in zip(waste_samples_in, waste_sample_ids):
        stored_sample = crud.waste_sample.get(db=db, id=stored_id)
        assert stored_sample
        assert sample_in.waste_level == stored_sample.waste_level
        assert sample_in.latitude == stored_sample.latitude
        assert sample_in.longitude == stored_sample.longitude
        assert sample_in.owner_nickname == stored_sample.owner.nickname
        assert sample_in.sampling_date == stored_sample.sampling_date


def test_get_waste_sample(db: Session) -> None:
    waste_sample = create_random_waste_sample(db)
    stored_waste_sample = crud.waste_sample.get(db=db, id=waste_sample.id)
    assert stored_waste_sample
    assert waste_sample.waste_level == stored_waste_sample.waste_level
    assert waste_sample.latitude == stored_waste_sample.latitude
    assert waste_sample.longitude == stored_waste_sample.longitude
    assert waste_sample.id == stored_waste_sample.id
    assert waste_sample.owner_id == stored_waste_sample.owner_id
    assert waste_sample.sampling_date == stored_waste_sample.sampling_date


def test_update_waste_sample(db: Session) -> None:
    waste_sample = create_random_waste_sample(db)
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
    assert waste_sample.sampling_date == waste_sample2.sampling_date


def test_delete_waste_sample(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90
    sampling_date = datetime.utcnow()

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id, sampling_date=sampling_date
    )
    waste_sample2 = crud.waste_sample.remove(db=db, id=waste_sample.id)
    waste_sample3 = crud.waste_sample.get(db=db, id=waste_sample.id)
    assert waste_sample3 is None
    assert waste_sample2.id == waste_sample.id
    assert waste_sample2.waste_level == waste_level
    assert waste_sample2.latitude == latitude
    assert waste_sample2.longitude == longitude
    assert waste_sample2.owner_id == user.id
    assert waste_sample2.sampling_date == sampling_date


def test_get_waste_sample_in_range(db: Session) -> None:
    waste_level = randint(0, 10)
    latitude = 45.0
    longitude = 45.0
    sampling_date = datetime.utcnow()

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id, sampling_date=sampling_date
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
    sampling_date = datetime.utcnow()

    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude
    )
    user = create_random_user(db)
    crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=user.id, sampling_date=sampling_date
    )
    stored_waste_samples = crud.waste_sample.get_multi_in_range(
        db=db,
        min_lat=latitude - 2,
        max_lat=latitude - 1,
        min_lon=longitude - 1,
        max_lon=longitude + 1,
    )
    assert not stored_waste_samples


def test_get_all_waste_samples(db: Session) -> None:
    waste_samples = [
        WasteSampleImportExport(
            waste_level=ws.waste_level,
            latitude=ws.latitude,
            longitude=ws.longitude,
            sampling_date=ws.sampling_date,
            owner_nickname=ws.owner.nickname,
        )
        for ws in [create_random_waste_sample(db) for _ in range(10)]
    ]
    all_waste_samples = [
        WasteSampleImportExport(**s) for s in crud.waste_sample.get_all(db)
    ]
    for waste_sample in waste_samples:
        assert waste_sample in all_waste_samples
