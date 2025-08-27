from math_path.domain import Action, Event, Role


def print_event(event: Event) -> None:
    print_role(event.role)
    print_action(event.action)
    print_data(event.data)
    print_separator()


def print_role(role: Role) -> None:
    print(f"Role: {role.value}")


def print_action(action: Action) -> None:
    print(f"Action: {action.value}")


def print_data(data: str) -> None:
    print(f"Data: {data}")


def print_separator() -> None:
    print()
    print("-" * 40)
    print()
