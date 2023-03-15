from typing import Optional
from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.models.TaskModel import TaskModel
from src.models.TextGenerationResultModel import TextGenerationResultModel
from src.tasks.worker import generate_text_task


router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


# TODO: since this is now a post request get values from body NOT query params
@router.post(
    "/generate",
    response_model=TaskModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_text(
    prompt: str, max_length: int, num_return_sequences: Optional[int] = None
):
    """Create celery prediction task. Return task_id to client in order to retrieve result"""
    task_id = generate_text_task.delay(
        {
            "prompt": prompt,
            "max_length": max_length,
            "num_return_sequences": num_return_sequences,
        }
    )
    return TaskModel(task_id=str(task_id), status=states.PENDING)


@router.get(
    "/result/{task_id}",
    response_model=TextGenerationResultModel,
    status_code=200,
)
async def get_result(task_id):
    """Fetch text generation result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        json_compatible_task_data = jsonable_encoder(
            TaskModel(task_id=str(task_id), status=states.PENDING)
        )
        return JSONResponse(
            status_code=202,
            content=json_compatible_task_data,
        )
    results = task.get()

    if results is None:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="no results were found",
        )

    return TextGenerationResultModel(
        task_id=str(task_id), status=states.SUCCESS, results=results
    )
