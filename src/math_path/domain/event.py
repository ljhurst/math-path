from enum import Enum

from pydantic import BaseModel

from math_path.domain.step_action import StepAction


class Role(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"
    TOOL = "TOOL"


class Event(BaseModel):
    role: Role
    action: StepAction
    data: str
