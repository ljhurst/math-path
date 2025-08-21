from typing import Any, Callable

from openai.types.chat import ChatCompletionToolParam
from pydantic import BaseModel

from math_path.tools.math import (
    ADD_ONE,
    DIVIDE_BY_TWO,
    MULTIPLY_BY_TWO,
    SUBTRACT_ONE,
    add_one,
    divide_by_two,
    multiply_by_two,
    subtract_one,
)
from math_path.tools.next_step import DONE, done


class ToolInfo(BaseModel):
    openai_details: ChatCompletionToolParam
    implementation: Callable


TOOLS_MAP = {
    "done": ToolInfo(
        openai_details=DONE,
        implementation=done,
    ),
    "add_one": ToolInfo(
        openai_details=ADD_ONE,
        implementation=add_one,
    ),
    "subtract_one": ToolInfo(
        openai_details=SUBTRACT_ONE,
        implementation=subtract_one,
    ),
    "multiply_by_two": ToolInfo(
        openai_details=MULTIPLY_BY_TWO,
        implementation=multiply_by_two,
    ),
    "divide_by_two": ToolInfo(
        openai_details=DIVIDE_BY_TWO,
        implementation=divide_by_two,
    ),
}


def get_openai_tools() -> list[ChatCompletionToolParam]:
    return [tool_info.openai_details for tool_info in TOOLS_MAP.values()]


def call_tool(name: str, args: dict) -> Any:
    if name not in TOOLS_MAP:
        raise ValueError(f"Tool '{name}' is not registered.")

    tool_info = TOOLS_MAP[name]

    return tool_info.implementation(**args)
