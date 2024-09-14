from typing import Annotated

from fastapi import APIRouter, Path, Depends
from starlette import status

from backend.repository import CommentRepository
from schemas.responses import SCommentResponse, SCommentsResponse
from schemas.main import SCommentAdd, SComment, SGetCommentsThread

router = APIRouter(prefix="/forum/api/v1/comment", tags=["Комментарии"])


@router.post('/')
async def add_thread(add_thread: SCommentAdd) -> SCommentResponse:
    comment: SComment = await CommentRepository.add_comment(add_thread)
    return {
        "status_code": status.HTTP_201_CREATED,
        "comment": comment
    }


@router.get('/{comment_id:int}')
async def get_thread(comment_id: Annotated[int, Path(ge=1)]) -> SCommentResponse:
    comment: SComment = await CommentRepository.get_comment(comment_id)
    return {
        "status_code": status.HTTP_200_OK,
        "comment": comment
    }




@router.get('/thread')
async def get_thread(get_comments_thread: Annotated[SGetCommentsThread, Depends()]) -> SCommentsResponse:
    comments: list[SComment] = await CommentRepository.get_comments(
        thread_id=get_comments_thread.thread_id,
        offset=get_comments_thread.offset,
        limit=get_comments_thread.limit,
    )
    return {
        "status_code": status.HTTP_200_OK,
        "comments": comments
    }






