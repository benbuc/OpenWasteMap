from celery import Celery

celery_app = Celery(
    "worker",
    broker="amqp://guest@queue//",
    backend="rpc://guest@localhost//",
)

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.render_tile": "main-queue",
    "app.backup.tasks.full_backup": "main-queue",
}
