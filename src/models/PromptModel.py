from typing import Optional
from pydantic import BaseModel, Field


class PromptModel(BaseModel):
    prompt: str
    max_length: int = Field(
        default=50, title="The max number of tokens to generate", le=400, ge=1
    )
    num_return_sequences: int = Field(
        default=1,
        title="The number of separate sequences with the given max_length to generate",
        le=5,
        ge=1,
    )
