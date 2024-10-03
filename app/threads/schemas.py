from datetime import datetime

from pydantic import BaseModel, Field


class SThreadAdd(BaseModel):
    title: str = Field(examples=['Есть одна тян!'], max_length=150)
    text: str = Field(examples=['Надеюсь ты достаточно ночной...'], max_length=1500)
    nick: str | None = Field(examples=['Макака'], default=None)

    class Config:
        from_attributes = True



class SThread(SThreadAdd):
    id: int
    create_at: datetime




class SStatusCode(BaseModel):
    status_code: int


class SThreadResponse(SStatusCode):
    thread: SThread


class SThreadsResponse(SStatusCode):
    threads: list[SThread]
