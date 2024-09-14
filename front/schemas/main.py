
from pydantic import BaseModel


class SThreadAdd(BaseModel):
    title: str
    nick: str | None = "Аноним"
    text: str