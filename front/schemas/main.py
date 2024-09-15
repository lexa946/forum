
from pydantic import BaseModel


class SThreadAdd(BaseModel):
    title: str
    nick: str | None = "Аноним"
    text: str


class SCommentAdd(BaseModel):
    nick: str | None = "Аноним"
    text: str
    thread_id: int
