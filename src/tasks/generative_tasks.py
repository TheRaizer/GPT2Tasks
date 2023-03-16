from src.tasks import app
from src.model import language_model
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@app.task(
    name="generative_tasks.generate_text",
    acks_late=True,
)
def generate_text(data):
    """
    When this task is called we first execute the __call__ method of InferenceTask
    in the context of model.LanguageModel. We then execute whatever is in this function
    also in the context of model.LanguageModel.

    path: is what defines the context of the task (what self will refer too).
    base: is what will initially run before the rest of the task is executed.
    """

    num_return_sequences = (
        1
        if data["num_return_sequences"] is None
        else data["num_return_sequences"]
    )

    outputs = language_model.generate_text(
        prompt=data["prompt"],
        max_length=data["max_length"],
        num_return_sequences=num_return_sequences,
    )

    logger.info(
        "generated outputs from prompt: {prompt}".format(prompt=data["prompt"])
    )

    return outputs
