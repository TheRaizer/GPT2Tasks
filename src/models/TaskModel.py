from pydantic import BaseModel

class TaskModel(BaseModel):
    task_id: str
    status: str
