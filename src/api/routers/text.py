from typing import List, cast, Optional
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from models.TaskModel import TaskModel, TaskStatus
from models.TextGenerationResultModel import TextGenerationResultModel
from src.tasks.generate_text import generate_text_task


router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post(
    "/generate",
    response_model=TextGenerationResultModel,
    status_code=status.HTTP_202_CREATED,
)
async def generate_text(
    prompt: str, max_length: int, num_of_return_sequences: Optional[int] = None
):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    task_id = generate_text_task.delay(
        {
            "prompt": prompt,
            "max_length": max_length,
            "num_of_return_sequences": num_of_return_sequences,
        }
    )
    return {"task_id": str(task_id), "status": "Processing"}


@router.get(
    "/result/{task_id}",
    response_model=TextGenerationResultModel,
    status_code=200,
    responses={202: {"model": TaskModel, "description": "Accepted: Not Ready"}},
)
async def get_result(task_id):
    """Fetch text generation result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(
            status_code=202,
            content=TaskModel(
                task_id=str(task_id), status=TaskStatus.PROCESSING
            ),
        )
    results: Optional[List[str]] = cast(Optional[List[str]], task.get())

    if results is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="no results were found",
        )

    return TextGenerationResultModel(
        task_id=str(task_id), status=TaskStatus.COMPLETE, results=results
    )
