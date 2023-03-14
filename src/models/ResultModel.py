from typing import List

from src.models import TaskModel


class ResultModel(TaskModel):
    prompt: str
    outputs: List[str]
