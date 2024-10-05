from typing import Annotated, Union

from fastapi import APIRouter, Path, Depends, status, UploadFile, Form, File

from app.comments.dao import CommentDAO
from app.comments.schemas import SComment, SCommentResponse, SCommentAdd, SCommentsResponse
from app.exceptions import CommentNotFount
from app.schemas.base import SPaginator

router = APIRouter(prefix="/forum/api/v1/comment", tags=["Комментарии"])


@router.post('/')
async def add_comment(text: Annotated[str, Form()],
                      thread_id: Annotated[int, Form(ge=1)],
                      nick: Annotated[str, Form()] = "Аноним",
                      files: Union[list[UploadFile], None] = None):
    comment = SCommentAdd(text=text, nick=nick, thread_id=thread_id)
    comment = await CommentDAO.add(comment=comment, files=files)
    return SCommentResponse(
        status_code=status.HTTP_201_CREATED,
        comment=comment,
    )

@router.get('/{comment_id:int}')
async def get_comment(comment_id: Annotated[int, Path(ge=1)]) -> SCommentResponse:
    comment = await CommentDAO.find_by_id(comment_id)
    if not comment:
        raise CommentNotFount
    return SCommentResponse(
        status_code=status.HTTP_200_OK,
        comment=comment
    )


@router.get('/thread')
async def get_thread_comments(thread_id: int, paginator: Annotated[SPaginator, Depends()]) -> SCommentsResponse:
    comments = await CommentDAO.find_all(
        thread_id=thread_id,
        offset=paginator.offset,
        limit=paginator.limit,
        order_by="asc"
    )
    print(c)
    return SCommentsResponse(
        status_code=status.HTTP_200_OK,
        comments=comments
    )
