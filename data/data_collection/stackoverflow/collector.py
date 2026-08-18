import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


API_URL = "https://api.stackexchange.com/2.3/search/advanced"

SITE = "stackoverflow"

# Initial controlled technology queries.
QUERIES = [
    "openai",
    "claude",
    "gemini",
    "llm",
    "rag",
    "ai-agent",
    "mcp",
]

PAGE_SIZE = 100
MAX_PAGES_PER_QUERY = 2

OUTPUT_DIR = Path("data/raw/stackoverflow")


def collect_questions(query):
    """
    Collect Stack Overflow questions for one technology query.
    """

    records = []

    for page in range(1, MAX_PAGES_PER_QUERY + 1):

        params = {
            "site": SITE,
            "q": query,
            "page": page,
            "pagesize": PAGE_SIZE,
            "sort": "creation",
            "order": "desc",
        }

        response = requests.get(
            API_URL,
            params=params,
            timeout=30,
        )

        print(
            f"Query={query} | "
            f"Page={page} | "
            f"HTTP={response.status_code}"
        )

        response.raise_for_status()

        data = response.json()

        items = data.get("items", [])

        print(
            f"Records returned: {len(items)} | "
            f"Quota remaining: {data.get('quota_remaining')}"
        )

        for item in items:

            record = {
                "question_id": item.get("question_id"),
                "title": item.get("title"),
                "tags": item.get("tags", []),
                "creation_date": item.get("creation_date"),
                "score": item.get("score"),
                "answer_count": item.get("answer_count"),
                "view_count": item.get("view_count"),
                "is_answered": item.get("is_answered"),
                "accepted_answer_id": item.get(
                    "accepted_answer_id"
                ),
                "link": item.get("link"),
                "owner": item.get("owner"),
                "query": query,
            }

            records.append(record)

        # Respect API limits.
        time.sleep(1)

        # Stop if the API says there are no more pages.
        if not data.get("has_more", False):
            break

    return records


def deduplicate_records(records):
    """
    Remove duplicate Stack Overflow questions.
    """

    unique_records = {}

    for record in records:

        question_id = record.get("question_id")

        if question_id is not None:
            unique_records[question_id] = record

    return list(unique_records.values())


def save_records(records):

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%d_%H%M%S")

    output_file = (
        OUTPUT_DIR
        / f"stackoverflow_ai_{timestamp}.json"
    )

    collection_metadata = {
        "source": "Stack Overflow",
        "collection_timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "queries": QUERIES,
        "pages_per_query": MAX_PAGES_PER_QUERY,
        "page_size": PAGE_SIZE,
        "records_collected": len(records),
    }

    output = {
        "metadata": collection_metadata,
        "records": records,
    }

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return output_file


def main():

    print("=" * 60)
    print("AI Evolution Intelligence")
    print("Stack Overflow Data Collector")
    print("=" * 60)

    all_records = []

    for query in QUERIES:

        print(f"\nCollecting query: {query}")

        records = collect_questions(query)

        all_records.extend(records)

    print("\nRemoving duplicates...")

    unique_records = deduplicate_records(
        all_records
    )

    print(
        f"Records before deduplication: "
        f"{len(all_records)}"
    )

    print(
        f"Records after deduplication: "
        f"{len(unique_records)}"
    )

    output_file = save_records(
        unique_records
    )

    print("\nCollection complete.")

    print(
        f"Raw data saved to: {output_file}"
    )


if __name__ == "__main__":
    main()