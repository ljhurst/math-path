from openai import OpenAI
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageFunctionToolCall
from openai.types.chat.chat_completion import (
    ChatCompletionMessage,
    Choice,
)

from math_path.prompts import SYSTEM
from math_path.utils import auth_utils
from math_path.utils.tool_utils import get_openai_tools

LLM_PROVIDER_URL = "https://nike-sole-blazer-1.cloud.databricks.com/serving-endpoints"
LLM_MODEL_ID = "databricks-claude-3-7-sonnet"


def invoke(prompt: str) -> Choice:
    pat = auth_utils.get_pat()

    client = OpenAI(
        api_key=pat,
        base_url=LLM_PROVIDER_URL,
    )

    messages = [
        {
            "role": "system",
            "content": SYSTEM,
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    tools = get_openai_tools()

    stream = client.chat.completions.create(
        model=LLM_MODEL_ID, messages=messages, tools=tools, temperature=0.0, stream=True
    )

    index = None
    finish_reason_so_far = None
    message_so_far = ""
    tool_calls_so_far = []

    for chunk in stream:
        if not chunk.choices:
            continue

        choice = chunk.choices[0]

        if choice.index is not None:
            index = choice.index

        if choice.finish_reason:
            finish_reason_so_far = chunk.choices[0].finish_reason

        if choice.delta.content:
            message_so_far = _handle_delta_content(chunk, message_so_far)

        if choice.delta.tool_calls:
            tool_calls_so_far = _handle_delta_tool_calls(chunk, tool_calls_so_far)

    return Choice(
        index=index,
        finish_reason=finish_reason_so_far,
        message=ChatCompletionMessage(
            role="assistant",
            content=message_so_far,
            tool_calls=tool_calls_so_far,
        ),
    )


def _handle_delta_content(chunk: ChatCompletionChunk, message_so_far: str) -> str:
    content_piece = chunk.choices[0].delta.content

    print(content_piece, end="", flush=True)

    return message_so_far + content_piece


def _handle_delta_tool_calls(
    chunk: ChatCompletionChunk,
    tool_calls_so_far: list[ChatCompletionMessageFunctionToolCall],
) -> list[ChatCompletionMessageFunctionToolCall]:
    tool_call = chunk.choices[0].delta.tool_calls[0]

    index = tool_call.index

    if len(tool_calls_so_far) == index:
        updated_id = tool_call.id
        updated_name = tool_call.function.name
        updated_arguments = tool_call.function.arguments

        tool_calls_so_far.append(
            _create_tool_call(updated_id, updated_name, updated_arguments)
        )
    else:
        existing_tool_call = tool_calls_so_far[index]

        updated_id = existing_tool_call.id
        updated_name = existing_tool_call.function.name
        updated_arguments = (
            existing_tool_call.function.arguments + tool_call.function.arguments
        )

        tool_calls_so_far[index] = _create_tool_call(
            updated_id, updated_name, updated_arguments
        )

    return tool_calls_so_far


def _create_tool_call(
    updated_id: str, updated_name: str, updated_arguments: str
) -> ChatCompletionMessageFunctionToolCall:
    return ChatCompletionMessageFunctionToolCall(
        id=updated_id,
        type="function",
        function={"name": updated_name, "arguments": updated_arguments},
    )
