from typing import Annotated

from fastapi import APIRouter, Path, Depends
from starlette import status

from app.exceptions import ThreadNotFound
from app.schemas.base import SPaginator
from app.threads.dao import ThreadDAO
from app.threads.schemas import SThread, SThreadAdd, SThreadResponse, SThreadsResponse

router = APIRouter(prefix="/forum/api/v1/thread", tags=["Треды"])


@router.post('/')
async def add_thread(thread: SThreadAdd) -> SThreadResponse:
    thread = await ThreadDAO.add(**thread.model_dump())
    return SThreadResponse(
        status_code=status.HTTP_201_CREATED,
        thread=thread
    )


@router.get('/{thread_id:int}')
async def get_thread(thread_id: Annotated[int, Path(ge=1)]) -> SThreadResponse:
    thread = await ThreadDAO.find_by_id(thread_id)
    if not thread:
        raise ThreadNotFound
    return SThreadResponse(
        status_code=status.HTTP_200_OK,
        thread=thread
    )


@router.get('/all')
async def get_threads(paginator: Annotated[SPaginator, Depends()]) -> SThreadsResponse:
    threads = await ThreadDAO.find_all(offset=paginator.offset, limit=paginator.limit, order_by="desc")
    return SThreadsResponse(
        status_code=status.HTTP_200_OK,
        threads=threads
    )
