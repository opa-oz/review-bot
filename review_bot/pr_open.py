import json
from typing import Any

from pydantic import BaseModel

from review_bot.github_client import get_github_client
from review_bot.helpers import get_jira_from_title, find_jira_links, replace_jira_links_with_shield
from review_bot.models import Person, Repository, PullRequest


class OpenedPRPayload(BaseModel):
    action: str
    number: int

    sender: Person

    repository: Repository
    pull_request: PullRequest


async def on_pr_open(request: Any):
    print("🦁on_pr_open")
    payload: OpenedPRPayload = OpenedPRPayload.parse_obj(request)

    title = payload.pull_request.title
    body = payload.pull_request.body

    ticket = get_jira_from_title(title)

    github = get_github_client()

    todos = []
    new_body = body

    if ticket is not None:
        label, number = ticket

        placeholder = f"{label}-X"

        if placeholder in new_body:
            new_body = new_body.replace(placeholder, f"{label}-{number}")

        jira_links = find_jira_links(new_body)
        if len(jira_links) != 0:
            new_body = replace_jira_links_with_shield(new_body, jira_links)

            todos.append("update-body")

    assignee = payload.pull_request.assignee

    if assignee is None:
        todos.append("update-assignee")

    async with github as client:
        for todo in todos:
            if todo == "update-body":
                resp = await client.patch(
                    payload.pull_request.url,
                    headers={"Accept": "application/vnd.github+json"},
                    data=json.dumps({"body": new_body})
                )

                if resp.status_code != 200:
                    print("🔴🔴🔴 Error:", resp.text)
            elif todo == "update-assignee":
                resp = await client.post(
                    payload.pull_request.issue_url,
                    headers={"Accept": "application/vnd.github+json"},
                    data=json.dumps({"assignees": [payload.pull_request.user.login]})
                )

                if resp.status_code != 200:
                    print("🔴🔴🔴 Error:", resp.text)

    return {}
