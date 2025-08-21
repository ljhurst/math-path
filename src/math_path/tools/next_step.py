from openai.types.chat import ChatCompletionToolParam
from openai.types.shared_params import FunctionDefinition

from math_path.domain import StepAction

DONE = ChatCompletionToolParam(
    type="function",
    function=FunctionDefinition(
        name="done",
        description="Indicates that the task is complete.",
        parameters={
            "type": "object",
            "properties": {
                "step": {
                    "type": "string",
                    "description": f"The next step to execute. Must be '{StepAction.DONE.value}'.",
                }
            },
            "required": ["step"],
        },
    ),
)


def done(step: StepAction) -> None:
    raise RuntimeError(
        "This tool is only used for structured output and should not be called"
    )
