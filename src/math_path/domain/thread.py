from pydantic import BaseModel

from math_path.domain import Event


class Thread(BaseModel):
    events: list[Event]
