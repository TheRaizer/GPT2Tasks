from typing import List
from pydantic import BaseModel

from enum import Enum


class TaskStatus(Enum):
    PROCESSING = "processing"
    FAILED = "failed"
    COMPLETE = "complete"


class TaskModel(BaseModel):
    task_id: str
    status: TaskStatus
