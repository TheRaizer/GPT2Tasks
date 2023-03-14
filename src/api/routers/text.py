from typing import Optional
from fastapi import APIRouter, status
from src.models.ResultModel import ResultModel


router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post(
    "/generate",
    response_model=ResultModel,
    status_code=status.HTTP_202_CREATED,
)
def generate_text(
    prompt: str, length: int, num_of_return_sequences: Optional[int] = None
):
    # start celery prediction task
    pass
