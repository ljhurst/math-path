from math_path.domain import Event


def format_event(event: Event) -> str:
    return f"""
            <event>
                <role>{event.role.value}</role>
                <data>{event.data}</data>
            </event>
        """
