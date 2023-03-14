import os
from celery import Celery

# TODO: setup these environment variables using docker
BROKER_URI = os.environ["BROKER_URI"]
BACKEND_URI = os.environ["BACKEND_URI"]

app = Celery(
    "celery_app",
    broker=BROKER_URI,
    backend=BACKEND_URI,
    include=["celery_task_app.tasks"],
)
