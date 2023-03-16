import os
from celery import Celery
from celery import Celery


BROKER_URL = os.environ["BROKER_URL"]
BACKEND_URL = os.environ["BACKEND_URL"]

app = Celery(
    "celery_app",
    broker=BROKER_URL,
    backend=BACKEND_URL,
)
app.config_from_object("src.tasks.celery_config")
