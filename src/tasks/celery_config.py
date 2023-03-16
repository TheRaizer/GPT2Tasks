import os

broker_url = os.environ["BROKER_URL"]

# List of modules to import when the Celery worker starts.
imports = ("src.tasks.generative_tasks",)

result_backend = os.environ["BACKEND_URL"]

# TODO: https://docs.celeryq.dev/en/stable/userguide/routing.html#guide-routing potentially route tasks to different queues depending on
# TODO the max_length and num_return_sequences.
# TODO: Use flower in start_app.sh to monitor tasks
# default is 4. We lessen this because model inference may take a while.
worker_prefetch_multiplier = 2
