from pydantic import BaseModel
from typing import List
from .task_obj_schema import Task


class Plan(BaseModel):
    blog_title: str
    tasks: List[Task]
