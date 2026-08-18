import os
import time
import requests


API_URL = "https://api.github.com/search/repositories"

QUERIES = [
    "llm",
    "ai agents",
    "mcp",
    "multimodal ai",
    "reasoning ai",
]

START_DATE = "2026-01-01"
END_DATE = "2026-08-31"


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

    print("=" * 70)
    print("GitHub 2026 Historical Coverage Test")
    print("Authenticated API")
    print("=" * 70)

    for query in QUERIES:

        search_query = (
            f"{query} "
            f"created:{START_DATE}..{END_DATE}"
        )

        params = {
            "q": search_query,
            "per_page": 1,
            "page": 1,
        }

        print(f"\nTesting: {query}")

        for attempt in range(1, 4):

            try:

                response = requests.get(
                    API_URL,
                    headers=headers,
                    params=params,
                    timeout=60,
                )

                print(
                    f"HTTP Status: {response.status_code}"
                )

                response.raise_for_status()

                data = response.json()

                total = data.get(
                    "total_count",
                    0
                )

                items = data.get(
                    "items",
                    []
                )

                if total > 0 and items:

                    repository = items[0]

                    print(
                        f"FOUND "
                        f"matching={total}"
                    )

                    print(
                        f"Example: "
                        f"{repository.get('full_name')}"
                    )

                elif total > 0:

                    print(
                        f"FOUND "
                        f"matching={total}"
                    )

                else:

                    print("NO RESULTS")

                break

            except requests.exceptions.Timeout:

                print(
                    f"Request timed out "
                    f"(attempt {attempt}/3)"
                )

                if attempt < 3:
                    time.sleep(5)

            except requests.exceptions.RequestException as error:

                print(
                    f"Request failed: {error}"
                )

                break


if __name__ == "__main__":
    main()