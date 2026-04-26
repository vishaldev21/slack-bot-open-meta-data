from langgraph.graph import StateGraph, START, END
from .state import State
from .nodes.get_logs import get_logs
from .nodes.github import get_commit_diff
from .nodes.lineage import mcp_node_factory
from .nodes.analyze import analyze
from .nodes.create_issue import create_issue
from .nodes.conditional_edge import route_after_analysis


def build_graph(mcp_tools):
    builder = StateGraph(State)
    builder.add_node("read_logs", get_logs)
    builder.add_node("github", get_commit_diff)
    builder.add_node("open-metadata", mcp_node_factory(mcp_tools))
    builder.add_node("analyze", analyze())
    builder.add_node("create_issue", create_issue)

    builder.add_edge(START, "read_logs")
    builder.add_edge("read_logs", "github")
    builder.add_edge("github", "open-metadata")
    builder.add_edge("open-metadata", "analyze")
    builder.add_conditional_edges(
        "analyze",
        route_after_analysis,
        {
            "create_issue": "create_issue",
            "__end__": END,
        },
    )
    builder.add_edge("create_issue", END)

    return builder.compile()
