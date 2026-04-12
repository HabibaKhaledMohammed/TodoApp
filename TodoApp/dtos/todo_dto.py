from pydantic import BaseModel


class TodoDto(BaseModel):
    title: str
    description: str | None = None
    priority: int
    complete: bool