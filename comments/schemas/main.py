from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SCommentAdd(BaseModel):
    text: str = Field(examples=['Сделай уже что-нибудь!'], max_length=1500)
    nick: str | None = Field(examples=['БабкаВТапках'], default=None, max_length=15,
                             description="Можешь добавить, а можешь и не добавлять.")
    thread_id: int = Field(description="ID Треда")

    model_config = ConfigDict(from_attributes=True)


class SComment(SCommentAdd):
    id: int
    create_at: datetime



class SGetCommentsThread(BaseModel):
    thread_id: int = Field(ge=1)
    limit: int = 20
    offset: int = 0

