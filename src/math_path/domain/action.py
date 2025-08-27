from enum import Enum


class Action(Enum):
    USER_INPUT = "USER_INPUT"
    ASSISTANT_RESPONSE = "ASSISTANT_RESPONSE"
    TOOL_CALL = "TOOL_CALL"
    TOOL_RESULT = "TOOL_RESULT"
    DONE = "DONE"
