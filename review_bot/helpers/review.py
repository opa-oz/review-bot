import os


def get_review_label():
    return "Ready to review"


def get_review_shield():
    shields = os.environ["SHIELDS_ENDPOINT"]
    # Ready%20to%20review-%20-success
    return f"![{get_review_label()}]({shields}/badge/-Ready%20to%20review-success)"
