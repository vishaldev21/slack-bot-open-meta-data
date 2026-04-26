from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from ..state import State
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPEN_AI_API_KEY"] = os.getenv("OPEN_AI_API_KEY")


def mcp_node_factory(mcp_tools):

    llm = ChatOpenAI(
        model="gpt-5.4-nano-2026-03-17", api_key=os.getenv("OPEN_AI_API_KEY")
    )

    agent = create_agent(
        model=llm,
        tools=mcp_tools,  # 👈 ONLY HERE
    )

    async def node(state: State):
        log = state.get("logs")

        response = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                    Get lineage for:
                    FQN: {log.get("FQN")}
                    Entity: {log.get("entity")}
                    Logs: {log}
                    """,
                    }
                ]
            }
        )

        return {"lineage": response["messages"][-1].content}

    return node
