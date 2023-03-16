from celery.worker.control import control_command

# view this to understand remote control commands https://docs.celeryq.dev/en/stable/userguide/workers.html

# execute the command using celery -A myapp control increase_prefetch_count 3


@control_command(
    args=[("n", int)],
    signature="[N=1]",  # <- used for help on the command-line.
)
def increase_prefetch_count(state, n=1):
    """This function allows us to increase the task prefetch
    count of all tasks.

    Args:
        state (_type_): gives access to consumers (workers)
        n (int, optional): the amount to increase the prefetch count by. Defaults to 1.

    Returns:
        _type_: a message
    """
    state.consumer.qos.increment_eventually(n)
    return {"ok": "prefetch count incremented"}
