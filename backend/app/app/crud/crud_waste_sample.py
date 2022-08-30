from datetime import datetime
from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app import crud
from app.crud.base import CRUDBase
from app.models.waste_sample import WasteSample
from app.schemas.waste_sample import (
    WasteSampleCreate,
    WasteSampleUpdate,
    WasteSampleCreateBulk,
)


class CRUDWasteSample(CRUDBase[WasteSample, WasteSampleCreate, WasteSampleUpdate]):
    def create_with_owner(
        self,
        db: Session,
        *,
        obj_in: WasteSampleCreate,
        owner_id: int,
        sampling_date: datetime,
    ) -> WasteSample:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(
            **obj_in_data, owner_id=owner_id, sampling_date=sampling_date
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_multi(
        self, db: Session, *, obj_in: List[WasteSampleCreateBulk],
    ) -> List[int]:
        db_objs = []
        for sample_obj in obj_in:
            obj_in_data = jsonable_encoder(sample_obj)
            # exchange owner nickname with correct id from DB
            del obj_in_data["owner_nickname"]
            stored_owner = crud.user.get_by_nickname(
                db, nickname=sample_obj.owner_nickname
            )
            owner_id = stored_owner.id if stored_owner else None
            db_obj = self.model(**obj_in_data, owner_id=owner_id)
            db.add(db_obj)
            db_objs.append(db_obj)
        db.commit()
        [db.refresh(db_obj) for db_obj in db_objs]
        return [db_obj.id for db_obj in db_objs]

    def get_multi_by_owner(
        self, db: Session, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[WasteSample]:
        return (
            db.query(self.model)
            .filter(WasteSample.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_in_range(
        self,
        db: Session,
        *,
        min_lat: float,
        max_lat: float,
        min_lon: float,
        max_lon: float,
        owner_id: Optional[int] = None,
    ) -> List[WasteSample]:
        """
        Find all samples in the specified range.
        The longitude may be larger than 180 or less than 0 and the overflow
        is filtered from the other side of the coordinate system.
        """
        min_overflow = abs(min_lon + 180) if min_lon < -180 else 0
        max_overflow = abs(max_lon - 180) if max_lon > 180 else 0
        return (
            db.query(self.model)
            .filter((WasteSample.owner_id == owner_id) if owner_id else True)
            .filter(
                WasteSample.latitude >= min_lat,
                WasteSample.latitude <= max_lat,
                or_(
                    and_(
                        WasteSample.longitude >= min_lon,
                        WasteSample.longitude <= max_lon,
                    ),
                    WasteSample.longitude >= 180 - min_overflow,
                    WasteSample.longitude <= -180 + max_overflow,
                ),
            )
            .all()
        )

    def get_all(self, db: Session) -> List[WasteSample]:
        return db.query(self.model).all()


waste_sample = CRUDWasteSample(WasteSample)
