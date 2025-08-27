import json
import logging

from openai.types.chat import ChatCompletionMessageFunctionToolCall
from openai.types.chat.chat_completion import Choice

from math_path.domain import Action, Event, Role, Thread
from math_path.llm import databricks_playground
from math_path.prompts import create_prompt
from math_path.utils import display_utils, tool_utils

logger = logging.getLogger(__name__)

MAX_AGENT_STEPS = 10


def run(start_number: int, end_number: int) -> Thread:
    logger.info(
        f"Starting run with start_number: {start_number}, end_number: {end_number}"
    )

    start_event = Event(
        role=Role.USER,
        action=Action.USER_INPUT,
        data=f"""
            Use the available tools to turn <start_number> into <end_number>.

            <start_number>{start_number}</start_number>
            <end_number>{end_number}</end_number>
        """,
    )

    display_utils.print_event(start_event)

    thread = Thread(events=[start_event])

    return _loop_until_done(thread)


def _loop_until_done(thread: Thread) -> Thread:
    for _ in range(MAX_AGENT_STEPS):
        display_utils.print_role(Role.ASSISTANT)
        display_utils.print_action(Action.ASSISTANT_RESPONSE)
        display_utils.print_data("")
        choice = _determine_next_step(thread)
        print()
        display_utils.print_separator()

        first_tool_call_name = choice.message.tool_calls[0].function.name.upper()
        reasoning = choice.message.content

        logger.info(f"Next step action: {first_tool_call_name}")
        logger.info(f"Next step reasoning: {reasoning}")

        assistant_event = Event(
            role=Role.ASSISTANT,
            action=Action.ASSISTANT_RESPONSE,
            data=reasoning,
        )

        thread.events.append(assistant_event)

        match first_tool_call_name:
            case Action.DONE.value:
                next_events = _handle_done_step()

                thread.events += next_events

                return thread
            case _:
                next_events = _handle_tool_step(choice)

                thread.events += next_events

    raise RuntimeError("Maximum number of agent steps reached without completion.")


def _determine_next_step(thread: Thread) -> Choice:
    prompt = create_prompt(thread)

    logger.info("Determining next step with prompt:")
    logger.info(f"\n{prompt}")

    return databricks_playground.invoke(prompt)


def _handle_done_step() -> list[Event]:
    logger.info("Execution done")
    done_event = Event(
        role=Role.ASSISTANT,
        action=Action.DONE,
        data="Execution completed successfully.",
    )

    display_utils.print_event(done_event)

    return [done_event]


def _handle_tool_step(choice: Choice) -> list[Event]:
    return [
        event
        for tool_call in choice.message.tool_calls
        for event in _call_tool(tool_call)
    ]


def _call_tool(tool_call: ChatCompletionMessageFunctionToolCall) -> list[Event]:
    tool_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    tool_call_event = Event(
        role=Role.TOOL,
        action=Action.TOOL_CALL,
        data=f"Calling tool: {tool_name} with arguments: {arguments}",
    )

    display_utils.print_event(tool_call_event)

    tool_response = tool_utils.call_tool(tool_name, arguments)

    tool_result_event = Event(
        role=Role.TOOL,
        action=Action.TOOL_RESULT,
        data=f"{tool_name} result: {tool_response}",
    )

    display_utils.print_event(tool_result_event)

    return [tool_call_event, tool_result_event]
