from pydantic import BaseModel

from schemas.main import SComment


class SStatusCodeResponse(BaseModel):
    status_code: int


class SCommentResponse(SStatusCodeResponse):
    comment: SComment


class SCommentsResponse(SStatusCodeResponse):
    comments: list[SComment]
