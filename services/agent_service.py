from langchain_mcp_adapters.client import MultiServerMCPClient
from agent.graph import build_graph
from agent.state import State
from dotenv import load_dotenv
import os

load_dotenv()


async def build_agent_graph():

    client = MultiServerMCPClient(
        {
            "openmetadata": {
                "transport": "http",
                "url": "http://localhost:8585/mcp",
                "headers": {"Authorization": f"Bearer {os.getenv('BOT_ACCESS_TOKEN')}"},
            }
        }
    )
    initial_state: State = {
        "logs": {},
        "github_changes": [],
        "lineage": "",
        "analysis": "",
        "fix_suggestion": "",
        "is_issue": False,
        "issue_number": "",
        "owner": "",
        "repo": "",
        "sha": "",
    }
    mcp_tools = await client.get_tools()
    graph = build_graph(mcp_tools)
    result = await graph.ainvoke(initial_state)
    # print(result)
    return result
