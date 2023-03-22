#!/bin/bash

# create a worker the default queue and long queue
# naming convention is:
# %h: Hostname, including domain name.
# %n: Hostname only.
# %d: Domain name only.
# these values are obtained from the hostname

# workers contain multiple pool processes. In this case we use the --autoscale=10,3 parameter to declare
# the max and min number of pool processes respectively.

#* default queue (--queues option includes long queue just for local purposes as running two separate workers for each queue consumes too much memory)
celery --app=src.tasks worker --pool=prefork -n worker1@%h --autoscale=10,3 --queues=default,long --loglevel=INFO --uid=nobody --gid=nogroup &\
#* long queue. This is a worker we would run on a separate machine as to process longer tasks separately from the default tasks.
# celery --app=src.tasks worker --pool=prefork -n worker2@%h --autoscale=50,3 --queues=long --loglevel=INFO --uid=nobody --gid=nogroup &\
uvicorn src.api.fastAPI:app --host 0.0.0.0 --port 8000