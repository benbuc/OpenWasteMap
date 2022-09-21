from app.core.celery_app import celery_app


@celery_app.task
def full_backup():
    with open("hallowelt.txt", "w") as f:
        f.write("HALLO WELT")


@celery_app.on_after_finalize.connect
def setup_periodic_backup(sender, **kwargs):
    sender.add_periodic_task(10.0, full_backup, name="Create Backup")
