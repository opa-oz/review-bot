from typing import Union

from fastapi import FastAPI, Header, Request
from pathlib import Path

from pydantic import BaseModel
from dotenv import load_dotenv

from review_bot import on_pr_open, on_issue_comment

load_dotenv()
app = FastAPI()

base_dir = Path.cwd()
static_dir = base_dir / 'static'


class Redirect(BaseModel):
    action: str


@app.get("/ping")
async def ping():
    return "OK;"


@app.post("/payload")
async def payload(
        request: Request,
        x_github_event: Union[str, None] = Header(default=None)
):
    print("🦁x_github_event", x_github_event)

    if x_github_event == "ping":
        return "pong"
    elif x_github_event == "pull_request":
        request_json = await request.json()
        action_redirector: Redirect = Redirect.parse_obj(request_json)
        action = action_redirector.action

        print("🦁action", action)
        if action == "opened":
            return await on_pr_open(request_json)
    elif x_github_event == "issue_comment":
        request_json = await request.json()
        action_redirector: Redirect = Redirect.parse_obj(request_json)
        action = action_redirector.action

        print("🦁action", action)
        if action == "created":
            return await on_issue_comment(request_json)

    return {}
