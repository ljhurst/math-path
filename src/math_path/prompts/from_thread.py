from math_path.domain import Thread
from math_path.utils.thread_utils import format_thread

from .next_step import NEXT_STEP
from .task import TASK


def create_prompt(thread: Thread) -> str:
    formatted_thread = format_thread(thread)

    # return textwrap.dedent(f"""
    return f"""
        <task>
            {TASK}
        </task>

        <thread>
            {formatted_thread}
        </thread>

        <next_step>
            {NEXT_STEP}
        </next_step>
        """
    # """).strip()
