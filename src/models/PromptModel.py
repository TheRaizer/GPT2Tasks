from typing import Optional
from pydantic import BaseModel


class PromptModel(BaseModel):
    prompt: str
    max_length: int
    num_return_sequences: Optional[int] = None
