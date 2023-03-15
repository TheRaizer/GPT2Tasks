import os
from celery import Celery
from celery import Celery
import logging

from src.model import language_model

logger = logging.getLogger(__name__)


BROKER_URL = os.environ["BROKER_URL"]
BACKEND_URL = os.environ["BACKEND_URL"]

app = Celery(
    "celery_app",
    broker=BROKER_URL,
    backend=BACKEND_URL,
    include=["src.tasks"],
)


@app.task(
    ignore_result=False,
    bind=True,
    path=("model", "LanguageModel"),
    name="generate_text_task",
)
def generate_text_task(self, data):
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

    return outputs
