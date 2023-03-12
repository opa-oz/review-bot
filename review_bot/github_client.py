import os

from httpx import AsyncClient


class GithubClient(AsyncClient):
    def __init__(self, token: str, **kwargs):
        super().__init__(headers={"Authorization": f"Bearer {token}"}, **kwargs)


def get_github_client():
    token = os.environ.get("PERSONAL_ACCESS_TOKEN_GITHUB")
    print("🦁token", token)

    return GithubClient(token)
