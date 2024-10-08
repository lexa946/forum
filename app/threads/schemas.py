from datetime import datetime

from pydantic import BaseModel, Field, validator, field_validator


class SThreadAdd(BaseModel):
    title: str = Field(examples=['Есть одна тян!'], max_length=150, min_length=5)
    text: str = Field(examples=['Надеюсь ты достаточно ночной...'], max_length=1500, min_length=15)
    nick: str|None = Field(examples=['Макака'], default="Аноним")

    class Config:
        from_attributes = True

    @field_validator('nick')
    def set_name(cls, nick):
        return nick or "Аноним"


class SThread(SThreadAdd):
    id: int
    create_at: datetime




class SStatusCode(BaseModel):
    status_code: int


class SThreadResponse(SStatusCode):
    thread: SThread


class SThreadsResponse(SStatusCode):
    threads: list[SThread]
