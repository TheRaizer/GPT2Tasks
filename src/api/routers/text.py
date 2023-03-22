from celery import states
from celery.result import AsyncResult
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from src.models.TaskModel import TaskModel
from src.models.TextGenerationResultModel import TextGenerationResultModel
from src.tasks.generative_tasks import generate_text as generate_text_task
from src.tasks.task_length import TaskLength
from src.models.PromptModel import PromptModel
import logging


logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/text",
    tags=["text"],
    responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}},
)


@router.post(
    "/generate",
    response_model=TaskModel,
    status_code=status.HTTP_202_ACCEPTED,
)
async def generate_text(prompt_data: PromptModel):
    try:
        """Create celery prediction task. Return task_id to client in order to retrieve result"""

        # if you are generating more than 500 total tokens then your task will be placed in to the priority queue
        # the priority queue will contain more workers
        task_length: TaskLength = (
            TaskLength.LONG
            if prompt_data.num_return_sequences * prompt_data.max_length > 500
            else TaskLength.SHORT
        )

        task_id = generate_text_task.delay(
            {
                "prompt": prompt_data.prompt,
                "max_length": prompt_data.max_length,
                "num_return_sequences": prompt_data.num_return_sequences,
                "task_length": task_length.value,
            }
        )
        return TaskModel(task_id=str(task_id), status=states.PENDING)
    except generate_text_task.OperationalError as exc:
        logger.exception("Sending task raised: %r", exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="sending task raised error",
        )


@router.get(
    "/result/{task_id}",
    response_model=TextGenerationResultModel,
    status_code=200,
)
async def get_result(task_id: str):
    """Fetch text generation result for given task_id"""
    task = AsyncResult(task_id)
    if not task.ready():
        json_compatible_task_data = jsonable_encoder(
            TaskModel(task_id=task_id, status=states.PENDING)
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
        task_id=task_id, status=states.SUCCESS, results=results
    )
