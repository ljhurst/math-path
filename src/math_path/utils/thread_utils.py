from math_path.domain import Thread
from math_path.utils.event_utils import format_event


def format_thread(thread: Thread) -> str:
    return "\n\n".join(format_event(event) for event in thread.events)
