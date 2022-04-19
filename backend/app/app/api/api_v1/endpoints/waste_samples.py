from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("/", response_model=List[schemas.WasteSample])
def read_waste_samples(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve waste samples.
    """
    if crud.user.is_superuser(current_user):
        waste_samples = crud.waste_sample.get_multi(db, skip=skip, limit=limit)
    else:
        waste_samples = crud.waste_sample.get_multi_by_owner(
            db=db, owner_id=current_user.id, skip=skip, limit=limit
        )
    return waste_samples


@router.post("/", response_model=schemas.WasteSample)
def create_waste_sample(
    *,
    db: Session = Depends(deps.get_db),
    waste_sample_in: schemas.WasteSampleCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new waste sample.
    """
    waste_sample = crud.waste_sample.create_with_owner(
        db=db, obj_in=waste_sample_in, owner_id=current_user.id
    )
    return waste_sample


@router.put("/{id}", response_model=schemas.WasteSample)
def update_waste_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    waste_sample_in: schemas.WasteSampleUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a waste sample.
    """
    waste_sample = crud.waste_sample.get(db=db, id=id)
    if not waste_sample:
        raise HTTPException(status_code=404, detail="Waste Sample not found")
    if not crud.user.is_superuser(current_user) and (
        waste_sample.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    waste_sample = crud.waste_sample.update(
        db=db, db_obj=waste_sample, obj_in=waste_sample_in
    )
    return waste_sample


@router.get("/{id}", response_model=schemas.WasteSample)
def read_waste_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get waste sample by ID.
    """
    waste_sample = crud.waste_sample.get(db=db, id=id)
    if not waste_sample:
        raise HTTPException(status_code=404, detail="Waste Sample not found")
    if not crud.user.is_superuser(current_user) and (
        waste_sample.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return waste_sample


@router.delete("/{id}", response_model=schemas.WasteSample)
def delete_waste_sample(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an waste sample.
    """
    waste_sample = crud.waste_sample.get(db=db, id=id)
    if not waste_sample:
        raise HTTPException(status_code=404, detail="Waste Sample not found")
    if not crud.user.is_superuser(current_user) and (
        waste_sample.owner_id != current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    waste_sample = crud.waste_sample.remove(db=db, id=id)
    return waste_sample