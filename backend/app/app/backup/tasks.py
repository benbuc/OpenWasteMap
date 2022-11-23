import io
import json
import zipfile
from datetime import datetime

from celery.schedules import crontab
from fastapi.encoders import jsonable_encoder

from app import crud
from app.core.celery_app import celery_app
from app.core.config import settings
from app.db.session import SessionLocal


@celery_app.task
def full_backup():
    """
    Backup all important data to LOCAL_BACKUP_DIR
    This directory must be a mounted volume
    """

    with SessionLocal() as db:
        all_waste_samples = crud.waste_sample.get_all(db)
        all_users = crud.user.get_all(db)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, False) as zip_file:
        zip_file.writestr(
            "waste_samples.json",
            json.dumps(jsonable_encoder(all_waste_samples)),
        )
        zip_file.writestr(
            "users.json",
            json.dumps(jsonable_encoder(all_users)),
        )

    backup_filename = (
        f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{settings.SERVER_NAME}.zip"
    )

    with open(settings.LOCAL_BACKUP_DIR / backup_filename, "wb") as f:
        f.write(zip_buffer.getvalue())


@celery_app.on_after_finalize.connect
def setup_periodic_backup(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=5, minute=0), full_backup, name="Create Backup"
    )
