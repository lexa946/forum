from pydantic import BaseModel


class SPaginator(BaseModel):
    limit: int = 20
    offset: int = 0
