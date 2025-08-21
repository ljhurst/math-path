from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition

ADD_ONE = ChatCompletionToolParam(
    type="function",
    function=FunctionDefinition(
        name="add_one",
        description="Adds one to the given number.",
        parameters={
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",
                    "description": "The number to which one will be added.",
                }
            },
            "required": ["number"],
        },
    ),
)


def add_one(number: int) -> int:
    return number + 1


SUBTRACT_ONE = ChatCompletionToolParam(
    type="function",
    function=FunctionDefinition(
        name="subtract_one",
        description="Subtracts one from the given number.",
        parameters={
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",
                    "description": "The number from which one will be subtracted.",
                }
            },
            "required": ["number"],
        },
    ),
)


def subtract_one(number: int) -> int:
    return number - 1


MULTIPLY_BY_TWO = ChatCompletionToolParam(
    type="function",
    function=FunctionDefinition(
        name="multiply_by_two",
        description="Multiplies the given number by two.",
        parameters={
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",
                    "description": "The number to be multiplied by two.",
                }
            },
            "required": ["number"],
        },
    ),
)


def multiply_by_two(number: int) -> int:
    return number * 2


DIVIDE_BY_TWO = ChatCompletionToolParam(
    type="function",
    function=FunctionDefinition(
        name="divide_by_two",
        description="Divides the given number by two.",
        parameters={
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer",
                    "description": "The number to be divided by two.",
                }
            },
            "required": ["number"],
        },
    ),
)


def divide_by_two(number: int) -> int:
    return number / 2
