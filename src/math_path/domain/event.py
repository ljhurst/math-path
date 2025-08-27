from enum import Enum

from pydantic import BaseModel

from math_path.domain import Action


class Role(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    TOOL = "TOOL"


class Event(BaseModel):
    role: Role
    action: Action
    data: str
