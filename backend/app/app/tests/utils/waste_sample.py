from random import randint, random
from typing import Optional

from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.waste_sample import WasteSampleCreate
from app.tests.utils.user import create_random_user


def create_random_waste_sample(
    db: Session, *, owner_id: Optional[int] = None, create_owner: bool = True
) -> models.WasteSample:
    if owner_id is None and create_owner:
        user = create_random_user(db)
        owner_id = user.id

    waste_level = randint(0, 10)
    latitude = random() * 90
    longitude = random() * 90
    return create_waste_sample(
        db,
        owner_id=owner_id,
        waste_level=waste_level,
        latitude=latitude,
        longitude=longitude,
    )


def create_waste_sample(
    db: Session,
    *,
    owner_id: Optional[int] = None,
    waste_level: int,
    latitude: float,
    longitude: float
) -> models.WasteSample:
    waste_sample_in = WasteSampleCreate(
        waste_level=waste_level, latitude=latitude, longitude=longitude, id=id
    )
    return crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=owner_id
    )
