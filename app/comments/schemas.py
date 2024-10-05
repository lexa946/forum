from datetime import datetime


from pydantic import BaseModel, Field


class SMedia(BaseModel):
    id: int
    comment_id: int
    filename: str
    s3_url:str

    class Config:
        from_attributes = True


class SCommentAdd(BaseModel):
    text: str = Field(examples=['Сделай уже что-нибудь!'], max_length=1500)
    nick: str | None = Field(examples=['БабкаВТапках'], default="Аноним", max_length=15,
                             description="Можешь добавить, а можешь и не добавлять.")
    thread_id: int = Field(description="ID Треда", ge=1)

    class Config:
        from_attributes = True


class SComment(SCommentAdd):
    id: int
    create_at: datetime
    media: list[SMedia]

class SAddCommentMedia(BaseModel):
    comment_id: int
    file: str


class SCommentMedia(SAddCommentMedia):
    id: int

    class Config:
        from_attributes = True


class SStatusCodeResponse(BaseModel):
    status_code: int


class SCommentResponse(SStatusCodeResponse):
    comment: SComment

class SCommentsResponse(SStatusCodeResponse):
    comments: list[SComment]
