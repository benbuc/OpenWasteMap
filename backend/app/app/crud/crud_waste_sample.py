from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.waste_sample import WasteSample
from app.schemas.waste_sample import WasteSampleCreate, WasteSampleUpdate


class CRUDWasteSample(CRUDBase[WasteSample, WasteSampleCreate, WasteSampleUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: WasteSampleCreate, owner_id: int
    ) -> WasteSample:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, owner_id=owner_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

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


waste_sample = CRUDWasteSample(WasteSample)
