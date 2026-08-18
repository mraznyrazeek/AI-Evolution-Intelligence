import os
import requests


API_URL = "https://api.github.com/search/repositories"

QUERIES = [
    "rag",
    "llm",
    "ai agents",
    "mcp",
    "multimodal ai",
    "reasoning ai",
]

PERIODS = [
    ("2023", "2023-01-01", "2023-12-31"),
    ("2024", "2024-01-01", "2024-12-31"),
    ("2025", "2025-01-01", "2025-12-31"),
    ("2026", "2026-01-01", "2026-08-31"),
]


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
    print("GitHub Historical Coverage Test")
    print("Authenticated API")
    print("=" * 70)

    for year, start_date, end_date in PERIODS:

        print(f"\n### {year}")

        for query in QUERIES:

            search_query = (
                f"{query} "
                f"created:{start_date}..{end_date}"
            )

            params = {
                "q": search_query,
                "per_page": 1,
                "page": 1,
            }

            response = requests.get(
                API_URL,
                headers=headers,
                params=params,
                timeout=30,
            )

            print(
                f"{query:18} "
                f"HTTP={response.status_code}",
                end=" "
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
                    f"matching={total} "
                    f"example={repository.get('full_name')}"
                )

            elif total > 0:

                print(
                    f"FOUND "
                    f"matching={total}"
                )

            else:

                print("NO RESULTS")


if __name__ == "__main__":
    main()