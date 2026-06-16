from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int
    title: str
    brief: str = Field(..., description="What to cover in this section.")
