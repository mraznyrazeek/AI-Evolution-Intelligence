import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


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

# --------------------------------------------------
# Study period
# --------------------------------------------------

START_YEAR = 2023
END_YEAR = 2026
END_MONTH = 8

# Stop collection when quota reaches this level.
MIN_QUOTA = 100

# Store each month separately.
OUTPUT_DIR = Path(
    "data/raw/stackoverflow/monthly"
)


# --------------------------------------------------
# Date utilities
# --------------------------------------------------

def to_unix(date_string):
    """
    Convert YYYY-MM-DD into a Unix timestamp.
    """

    dt = datetime.strptime(
        date_string,
        "%Y-%m-%d"
    ).replace(
        tzinfo=timezone.utc
    )

    return int(dt.timestamp())


def get_month_period(year, month):
    """
    Return the start and end date for a month.

    Example:
        2023-01 → 2023-01-01 to 2023-02-01
    """

    start_date = (
        f"{year}-{month:02d}-01"
    )

    if month == 12:

        next_year = year + 1
        next_month = 1

    else:

        next_year = year
        next_month = month + 1

    end_date = (
        f"{next_year}-{next_month:02d}-01"
    )

    return start_date, end_date


# --------------------------------------------------
# Stack Overflow query collection
# --------------------------------------------------

def collect_query(
    query,
    start_date,
    end_date
):
    """
    Collect all available pages for one query
    within one monthly period.
    """

    records = []

    page = 1
    quota_remaining = None

    while True:

        params = {
            "site": SITE,
            "q": query,
            "fromdate": to_unix(start_date),
            "todate": to_unix(end_date),
            "sort": "creation",
            "order": "asc",
            "pagesize": 100,
            "page": page,
        }

        try:

            response = requests.get(
                API_URL,
                params=params,
                timeout=30,
            )

        except requests.exceptions.RequestException as error:

            print(
                f"Request failed for query "
                f"{query}: {error}"
            )

            return records, None

        print(
            f"Query={query} | "
            f"Period={start_date} to {end_date} | "
            f"Page={page} | "
            f"HTTP={response.status_code}"
        )

        # --------------------------------------------------
        # Handle HTTP errors
        # --------------------------------------------------

        if response.status_code != 200:

            print(
                "API response:"
            )

            print(
                response.text[:500]
            )

            return records, None

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        data = response.json()

        # --------------------------------------------------
        # Handle Stack Exchange backoff
        # --------------------------------------------------

        if "backoff" in data:

            backoff_seconds = data["backoff"]

            print(
                f"API requested backoff: "
                f"{backoff_seconds} seconds"
            )

            time.sleep(
                backoff_seconds
            )

        # --------------------------------------------------
        # Read quota
        # --------------------------------------------------

        quota_remaining = data.get(
            "quota_remaining"
        )

        items = data.get(
            "items",
            []
        )

        print(
            f"Records returned: "
            f"{len(items)} | "
            f"Quota remaining: "
            f"{quota_remaining}"
        )

        # --------------------------------------------------
        # Store records
        # --------------------------------------------------

        for item in items:

            record = {
                "source": "stackoverflow",

                "search_query": query,

                "collection_period_start": (
                    start_date
                ),

                "collection_period_end": (
                    end_date
                ),

                "collection_timestamp": (
                    datetime.now(
                        timezone.utc
                    ).isoformat()
                ),

                "data": item,
            }

            records.append(
                record
            )

        # --------------------------------------------------
        # Stop if quota is low
        # --------------------------------------------------

        if (
            quota_remaining is not None
            and quota_remaining <= MIN_QUOTA
        ):

            print(
                "\nWARNING: API quota is low."
            )

            print(
                f"Remaining quota: "
                f"{quota_remaining}"
            )

            return (
                records,
                quota_remaining
            )

        # --------------------------------------------------
        # Check pagination
        # --------------------------------------------------

        if not data.get(
            "has_more",
            False
        ):

            break

        page += 1

        # Small delay between pages.
        time.sleep(0.5)

    return (
        records,
        quota_remaining
    )


# --------------------------------------------------
# Monthly collection
# --------------------------------------------------

def collect_month(
    year,
    month
):
    """
    Collect and save one month.
    """

    start_date, end_date = (
        get_month_period(
            year,
            month
        )
    )

    month_name = (
        f"{year}-{month:02d}"
    )

    output_file = (
        OUTPUT_DIR
        / f"stackoverflow_{month_name}.json"
    )

    # --------------------------------------------------
    # Resume protection
    # --------------------------------------------------

    if output_file.exists():

        print(
            f"\nSKIPPING {month_name}"
        )

        print(
            "Already collected:"
        )

        print(
            output_file
        )

        return "skipped"

    print(
        "\n" + "=" * 70
    )

    print(
        f"COLLECTION PERIOD: "
        f"{start_date} → {end_date}"
    )

    print(
        "=" * 70
    )

    month_records = []

    quota_remaining = None

    # --------------------------------------------------
    # Collect each technology query
    # --------------------------------------------------

    for query in QUERIES:

        records, quota = (
            collect_query(
                query,
                start_date,
                end_date
            )
        )

        month_records.extend(
            records
        )

        if quota is not None:

            quota_remaining = quota

        # --------------------------------------------------
        # Pause collection if quota is low
        # --------------------------------------------------

        if (
            quota_remaining is not None
            and quota_remaining <= MIN_QUOTA
        ):

            print(
                "\nCollection paused because "
                "Stack Exchange API quota is low."
            )

            return "paused"

    # --------------------------------------------------
    # Deduplicate questions
    # --------------------------------------------------

    print(
        "\nRemoving duplicates "
        "within month..."
    )

    unique_records = {}

    for record in month_records:

        question_id = (
            record["data"].get(
                "question_id"
            )
        )

        if question_id is not None:

            unique_records[
                question_id
            ] = record

    final_records = list(
        unique_records.values()
    )

    print(
        f"Records before deduplication: "
        f"{len(month_records)}"
    )

    print(
        f"Records after deduplication: "
        f"{len(final_records)}"
    )

    # --------------------------------------------------
    # Prepare output
    # --------------------------------------------------

    output = {

        "metadata": {

            "source": "Stack Overflow",

            "collection_type": "monthly",

            "period_start": start_date,

            "period_end": end_date,

            "queries": QUERIES,

            "collection_timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),

            "raw_record_count": (
                len(month_records)
            ),

            "unique_record_count": (
                len(final_records)
            ),
        },

        "records": final_records,
    }

    # --------------------------------------------------
    # Create output directory
    # --------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Save monthly file
    # --------------------------------------------------

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            output,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        "\nMonth collection complete."
    )

    print(
        f"Saved to: {output_file}"
    )

    return "completed"


# --------------------------------------------------
# Main collection process
# --------------------------------------------------

def main():

    print(
        "=" * 70
    )

    print(
        "AI Evolution Intelligence"
    )

    print(
        "Stack Overflow Resumable Collector"
    )

    print(
        "=" * 70
    )

    print(
        f"Study period: "
        f"{START_YEAR}-01 "
        f"to "
        f"{END_YEAR}-{END_MONTH:02d}"
    )

    print(
        f"Minimum quota threshold: "
        f"{MIN_QUOTA}"
    )

    print(
        f"Output directory: "
        f"{OUTPUT_DIR}"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------
    # Create output directory
    # --------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------
    # Collect months
    # --------------------------------------------------

    for year in range(
        START_YEAR,
        END_YEAR + 1
    ):

        max_month = (
            END_MONTH
            if year == END_YEAR
            else 12
        )

        for month in range(
            1,
            max_month + 1
        ):

            status = collect_month(
                year,
                month
            )

            # --------------------------------------------------
            # Pause safely
            # --------------------------------------------------

            if status == "paused":

                print(
                    "\n" + "=" * 70
                )

                print(
                    "COLLECTION PAUSED"
                )

                print(
                    "The API quota is too low."
                )

                print(
                    "Run this same command again "
                    "after the quota becomes available."
                )

                print(
                    "=" * 70
                )

                return

    # --------------------------------------------------
    # Finished
    # --------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "ALL AVAILABLE MONTHS COLLECTED"
    )

    print(
        "=" * 70
    )


# --------------------------------------------------
# Program entry point
# --------------------------------------------------

if __name__ == "__main__":

    main()