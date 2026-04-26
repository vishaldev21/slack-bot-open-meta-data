from typing import Literal
from ..state import State


def route_after_analysis(state: State) -> Literal["create_issue", "__end__"]:
    if state.get("is_issue"):
        return "create_issue"
    return "__end__"
