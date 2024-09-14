from typing import Annotated

from fastapi import APIRouter, Path, Depends
from starlette import status

from backend.repository import ThreadRepository
from schemas.responses import SThreadResponse, SThreadsResponse
from schemas.main import SThreadAdd, SThread, SPaginator

router = APIRouter(prefix="/forum/api/v1/thread", tags=["Треды"])


@router.post('/')
async def add_thread(add_thread: SThreadAdd) -> SThreadResponse:
    thread: SThread = await ThreadRepository.add_thread(add_thread)
    return {
        "status_code": status.HTTP_201_CREATED,
        "thread": thread
    }


@router.get('/{thread_id:int}')
async def get_thread(thread_id: Annotated[int, Path(ge=1)]) -> SThreadResponse:
    thread: SThread = await ThreadRepository.get_thread(thread_id)
    return {
        "status_code": status.HTTP_200_OK,
        "thread": thread
    }

@router.get('/all')
async def get_threads(paginator: Annotated[SPaginator, Depends()]) -> SThreadsResponse:
    threads: list[SThread] = await ThreadRepository.get_threads(paginator)
    return {
        "status_code": status.HTTP_200_OK,
        "threads": threads
    }


