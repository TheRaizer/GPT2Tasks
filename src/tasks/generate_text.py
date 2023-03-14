import logging
from celery import Task

from model import LanguageModel

from .worker import app

logger = logging.getLogger(__name__)


class Inferencetask(Task):
    """
    Abstraction of Celery's Task class to support loading ML model.
    """

    abstract = True

    def __init__(self):
        super().__init__()
        self.model = None

    def __call__(self, *args, **kwargs):
        """
        Load model on first call (i.e. first task processed)
        Avoids the need to load model on each task request
        """
        if not self.model:
            logger.info("Loading Model...")
            self.model = LanguageModel(model_path="./gpt2_onnx")
            logger.info("Model loaded")
        return self.run(*args, **kwargs)


@app.task(
    ignore_result=False,
    bind=True,
    base=Inferencetask,
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
    outputs = self.model.generate_text(
        prompt=data["prompt"],
        max_length=data["max_length"],
        num_return_sequences=data["num_return_sequences"],
    )

    return outputs
