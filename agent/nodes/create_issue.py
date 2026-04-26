from ..state import State
import httpx
import os


def create_issue(state: State):
    try:
        url = "https://api.github.com/repos/vishaldev21/db_schema/issues"
        headers = {
            "Authorization": f"Bearer {os.getenv('GITHUB_ACCESS_TOKEN')}",
            "Accept": "application/vnd.github+json",
        }

        data = {
            "title": state.get("logs")["message"],
            "body": state.get("fix_suggestion"),
            "labels": ["bug"],
        }

        response = httpx.post(url, json=data, headers=headers)
        response.raise_for_status()
        data = response.json()
        return {"issue_number": data.get("number")}
    except Exception as err:
        return {"issue_number": -1}
