import os
import requests


API_URL = "https://api.github.com/rate_limit"


def main():

    token = os.getenv("GITHUB_TOKEN")

    if not token:
        print("ERROR: GITHUB_TOKEN is not set.")
        return

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2026-03-10",
    }

    response = requests.get(
        API_URL,
        headers=headers,
        timeout=30,
    )

    print("HTTP Status:", response.status_code)

    response.raise_for_status()

    data = response.json()

    core = data.get("resources", {}).get("core", {})

    print("Authenticated GitHub API")
    print("Rate limit:", core.get("limit"))
    print("Remaining:", core.get("remaining"))
    print("Used:", core.get("used"))


if __name__ == "__main__":
    main()