from pydantic import BaseModel

from schemas.main import SThread

class SStatusCode(BaseModel):
    status_code: int


class SThreadResponse(SStatusCode):
    thread: SThread


class SThreadsResponse(SStatusCode):
    threads: list[SThread]
