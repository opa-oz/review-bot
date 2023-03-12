import json
from typing import Any

from pydantic import BaseModel

from review_bot.github_client import get_github_client
from review_bot.helpers import get_review_label, get_review_shield
from review_bot.models import Comment, Issue


class IssueCommentPayload(BaseModel):
    issue: Issue
    comment: Comment


async def on_issue_comment(request: Any):
    print("🦁on_issue_comment")
    payload: IssueCommentPayload = IssueCommentPayload.parse_obj(request)

    github = get_github_client()

    comment_text = str(payload.comment.body).strip()
    issue_body = payload.issue.body
    labels = payload.issue.labels

    commenter = payload.comment.user
    assignee = payload.issue.assignee if payload.issue.assignee is not None else payload.issue.user

    todos = []
    new_body = issue_body

    print("====", comment_text, commenter.login, assignee.login)

    review_label_test = get_review_label()
    labels_names = list(map(lambda x: x.name, labels))

    if comment_text == '/ready' and commenter.login == assignee.login:
        if review_label_test not in issue_body:
            # TODO: pick reviewers
            shield = get_review_shield()
            new_body = shield + "\r\n" + new_body
            todos.append("update-body")
            todos.append("add-label")
    elif comment_text == '/stop' and commenter.login == assignee.login:
        if review_label_test in issue_body:
            new_body = issue_body.replace(get_review_shield() + "\r\n", "")
            todos.append("update-body")

        if review_label_test in labels_names:
            todos.append("remove-label")

    async with github as client:
        for todo in todos:
            if todo == "update-body":
                resp = await client.patch(
                    payload.issue.url,
                    headers={"Accept": "application/vnd.github+json"},
                    data=json.dumps({"body": new_body})
                )

                if resp.status_code != 200:
                    print("🔴🔴🔴 Error:", resp.text)
            elif todo == "add-label":
                resp = await client.patch(
                    payload.issue.url,
                    headers={"Accept": "application/vnd.github+json"},
                    data=json.dumps({"labels": labels_names + [review_label_test]})
                )
                if resp.status_code != 200:
                    print("🔴🔴🔴 Error:", resp.text)
            elif todo == "remove-label":
                resp = await client.patch(
                    payload.issue.url,
                    headers={"Accept": "application/vnd.github+json"},
                    data=json.dumps({"labels": list(filter(lambda x: x != review_label_test, labels_names))})
                )
                if resp.status_code != 200:
                    print("🔴🔴🔴 Error:", resp.text)

    return {}
