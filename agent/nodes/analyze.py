from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from ..state import State
from typing_extensions import TypedDict
from langchain.messages import HumanMessage
import os


class StructuredOutput(TypedDict):
    is_issue: bool
    analysis: str
    fix_suggestion: str


def analyze():

    llm = ChatOpenAI(
        model="gpt-5.4-nano-2026-03-17", api_key=os.getenv("OPEN_AI_API_KEY")
    )

    agent = create_agent(model=llm, response_format=StructuredOutput)

    async def node(state: State):
        logs = state.get("logs")
        changes = state.get("github_changes")
        lineage = state.get("lineage")

        prompt = f"""
You are an intelligent system.

Analyze the following:
- Logs: {logs}
- GitHub Changes: {changes}
- Lineage: {lineage}

Decide:
1. Is this a breaking issue? (true/false)
2. If yes, suggest a fix

Return JSON:
{{
  "is_issue": true/false,
  "analysis": "...",
  "fix_suggestion": "..."
}}
"""

        response = await agent.ainvoke({"messages": [HumanMessage(prompt)]})

        # ⚠️ ideally parse JSON properly
        content = response["structured_response"]

        return {
            "analysis": content["analysis"],
            "is_issue": content["is_issue"],
            "fix_suggestion": content["fix_suggestion"],
        }

    return node
