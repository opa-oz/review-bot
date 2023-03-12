from typing import List, Optional

from pydantic import BaseModel


class Person(BaseModel):
    id: int
    login: str
    name: Optional[str]
    email: Optional[str]


class Repository(BaseModel):
    id: int
    name: str
    full_name: str
    default_branch: str

    private: bool
    archived: bool

    owner: Person

    html_url: str
    git_url: str
    ssh_url: str
    clone_url: str


class Commit(BaseModel):
    label: str
    ref: str
    sha: str

    user: Person
    repo: Repository


class PullRequest(BaseModel):
    id: int
    url: str
    number: int
    state: str

    title: str
    body: str

    draft: bool
    merged: bool

    user: Person
    assignee: Optional[Person]
    assignees: List[Person]
    requested_reviewers: List[Person]

    commits_url: str
    review_comments_url: str
    comments_url: str
    issue_url: str

    head: Commit
    base: Commit


class Comment(BaseModel):
    url: str
    id: int
    user: Person

    body: str


class Label(BaseModel):
    id: int
    url: str
    name: str
    color: str


class Issue(BaseModel):
    url: str
    user: Person
    state: str
    assignee: Optional[Person]

    body: str
    labels: List[Label]
