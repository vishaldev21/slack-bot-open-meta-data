from typing import TypedDict


class State(TypedDict):
    logs: dict
    github_changes: list
    lineage: str
    analysis: str
    fix_suggestion: str
    is_issue: bool
    issue_number: str
    owner: str
    repo: str
    sha: str
