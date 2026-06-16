import operator
from typing import TypedDict, List, Annotated, Optional
from schemas.plan_obj_schema import Plan


class State(TypedDict):
    topic: str
    plan: Optional[Plan]
    sections: Annotated[List[str], operator.add]
    final: str
