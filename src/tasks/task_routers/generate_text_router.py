from src.tasks.task_length import TaskLength


def generate_text_router(name, args, kwargs, options, task=None, **kw):
    """
    Here we route any long tasks into the long queue.
    """

    if (
        name == "generative_tasks.generate_text"
        and len(args) >= 1
        and "task_length" in args[0]
        and args[0]["task_length"] == TaskLength.LONG.value
    ):
        return {
            "queue": "long",
            "routing_key": "generative.text.long",
        }
    else:
        return {"queue": "default", "routing_key": "task.default"}
