from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class SThreadAdd(BaseModel):
    title: str = Field(examples=['Есть одна тян!'], max_length=150)
    text: str = Field(examples=['Надеюсь ты достаточно ночной...'], max_length=1500)
    nick: str | None = Field(examples=['Макака'], default=None)

    model_config = ConfigDict(from_attributes=True)



class SThread(SThreadAdd):
    id: int
    create_at: datetime



class SPaginator(BaseModel):
    limit: int = 20
    offset: int = 0
