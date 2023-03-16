#!/bin/sh
celery -A src.tasks worker --loglevel=info --uid=nobody --gid=nogroup & uvicorn src.api.fastAPI:app --host 0.0.0.0 --port 8000