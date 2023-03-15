#!/bin/sh
celery -A src.tasks.worker worker --loglevel=info & uvicorn src.api.fastAPI:app --host 0.0.0.0 --port 8000