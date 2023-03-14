# syntax = docker/dockerfile:1.0-experimental

# this is a python version compatible with pytorch
FROM python:3.9-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . .

# use wget instead of curl since we are running this on a alpine base image https://github.com/caprover/caprover/issues/844#issuecomment-702618580
HEALTHCHECK CMD wget --no-verbose --tries=1 --spider http://localhost:8000/health || exit 1

CMD ["uvicorn", "src.api.fastAPI:app", "--host", "0.0.0.0", "--port", "8000"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]