import os
import re
from typing import List, Tuple, Optional

from pydantic import BaseModel


class JiraLink(BaseModel):
    label: str
    link: str
    orig: str


full_match = re.compile(r'(\[(.+?)]\((.+?jira.+?)\))')
short_match = re.compile(r'([A-Z]+-[0-9]+)')


def find_jira_links(body: str) -> List[JiraLink]:
    matches = full_match.findall(body)

    if matches is None:
        return []

    links: List[JiraLink] = []

    for match in matches:
        print(match)
        links.append(JiraLink(
            orig=match[0],
            label=match[1],
            link=match[2]
        ))

    return links


def replace_jira_links_with_shield(body: str, links: List[JiraLink]) -> str:
    replacements = []

    shields = os.environ["SHIELDS_ENDPOINT"]

    for link in links:
        parts = link.label.split("-")
        label = "NF"
        number = "???"

        if len(parts) == 1:
            label = parts[0]
        elif len(parts) > 1:
            label, number = parts

        shield_link = f"[![DXUSG-423]({shields}/static/v1?color=4078c0&label={label}&message={number}&logo=jira&style=flat-square)]({link.link})"

        replacements.append((link.orig, shield_link))

    result = body

    for s_from, s_to in replacements:
        result = result.replace(s_from, s_to)

    return result


def get_jira_from_title(title: str) -> Optional[Tuple[str, str]]:
    matches = short_match.search(title)

    if matches is None:
        return None

    first_match = matches.group()
    parts = first_match.split("-")
    label = "NP"
    number = "???"

    if len(parts) == 1:
        label = parts[0]
    elif len(parts) > 1:
        label, number = parts

    return label, number
