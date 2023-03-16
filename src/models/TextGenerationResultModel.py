from typing import List

from src.models.TaskModel import TaskModel


class TextGenerationResultModel(TaskModel):
    results: List[str]
