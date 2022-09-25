from typing import Any

from fastapi import APIRouter, Depends

from app import models
from app.api import deps
from app.core.celery_app import celery_app

router = APIRouter()


@router.post("/backup")
def read_all_waste_samples(
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Backup all important data to BACKUP_DIR
    """

    celery_app.send_task("app.backup.tasks.full_backup")

    return {"msg": "Backup scheduled"}
