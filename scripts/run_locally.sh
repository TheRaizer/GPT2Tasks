#!/bin/bash

docker image prune -a -f &\
docker-compose up --build -d --remove-orphans