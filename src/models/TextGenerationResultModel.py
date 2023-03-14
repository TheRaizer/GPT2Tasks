from typing import List

from src.models import TaskModel


class TextGenerationResultModel(TaskModel):
    results: List[str]
