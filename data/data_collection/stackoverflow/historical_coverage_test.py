import requests
from datetime import datetime, timezone


API_URL = "https://api.stackexchange.com/2.3/search/advanced"

SITE = "stackoverflow"

QUERIES = [
    "openai",
    "claude",
    "gemini",
    "llm",
    "rag",
    "ai-agent",
    "mcp",
]

PERIODS = [
    ("2023", "2023-01-01", "2023-12-31"),
    ("2024", "2024-01-01", "2024-12-31"),
    ("2025", "2025-01-01", "2025-12-31"),
    ("2026", "2026-01-01", "2026-08-31"),
]


def to_unix(date_string):

    dt = datetime.strptime(
        date_string,
        "%Y-%m-%d"
    ).replace(tzinfo=timezone.utc)

    return int(dt.timestamp())


def main():

    print("=" * 70)
    print("Stack Overflow Historical Coverage Test")
    print("=" * 70)

    for year, start_date, end_date in PERIODS:

        print(f"\n### {year}")

        from_timestamp = to_unix(start_date)
        to_timestamp = to_unix(end_date)

        for query in QUERIES:

            params = {
                "site": SITE,
                "q": query,
                "fromdate": from_timestamp,
                "todate": to_timestamp,
                "sort": "creation",
                "order": "desc",
                "pagesize": 1,
                "page": 1,
            }

            response = requests.get(
                API_URL,
                params=params,
                timeout=30,
            )

            response.raise_for_status()

            data = response.json()

            items = data.get("items", [])

            if items:

                question = items[0]

                creation_timestamp = question.get(
                    "creation_date"
                )

                creation_date = datetime.fromtimestamp(
                    creation_timestamp,
                    tz=timezone.utc
                ).strftime("%Y-%m-%d")

                print(
                    f"{query:10} "
                    f"FOUND "
                    f"example_date={creation_date} "
                    f"quota={data.get('quota_remaining')}"
                )

            else:

                print(
                    f"{query:10} "
                    f"NO RESULTS "
                    f"quota={data.get('quota_remaining')}"
                )


if __name__ == "__main__":
    main()