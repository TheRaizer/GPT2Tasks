from typing import Any

from src.models.TaskModel import TaskModel


class TextGenerationResultModel(TaskModel):
    # TODO: make this List[str]
    results: Any
