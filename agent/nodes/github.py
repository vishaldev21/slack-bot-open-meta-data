from ..state import State
import httpx
from langchain.tools import tool


def get_latest_commit_shas(owner, repo, limit=3):
    """provides latest commit sha from github

    Args:
        owner (str): github repo owner
        repo (str): github repo
        limit (int, optional): _description_. Defaults to 3.

    Returns:
        str: latest commit sha
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {"per_page": limit}
    response = httpx.get(url)
    response.raise_for_status()
    commits = response.json()
    return commits[0]["sha"]


def get_commit_diff(state: State):
    """provides file changes

    Args:
        owner (str): github repo owner
        repo (str): github repo
        sha (str): commit sha

    Returns:
        str: file changes
    """
    owner = state.get("owner")
    repo = state.get("repo")
    sha = get_latest_commit_shas(owner, repo)
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"
    headers = {"Accept": "application/vnd.github.v3.diff"}
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()
        return {"github_changes": response.text}
    except Exception as err:
        print(err)
        return {"github_changes": ""}
