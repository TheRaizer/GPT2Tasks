import os
from kombu import Exchange, Queue

from src.tasks.task_routers.generate_text_router import generate_text_router

broker_url = os.environ["BROKER_URL"]

# List of modules to import when the Celery worker starts.
imports = ("src.tasks.generative_tasks",)

result_backend = os.environ["BACKEND_URL"]

# default is 4. We lessen this because model inference may take a while.
worker_prefetch_multiplier = 2

task_routes = (generate_text_router,)


task_queues = (
    Queue(  # default queue for all tasks
        "default",
        Exchange("default", type="direct"),
        routing_key="task.default",
    ),
    Queue(  # priority queue for generating text (more workers for larger tasks)
        "long",
        Exchange("default", type="direct"),
        routing_key="generative.text.long",
    ),
)
