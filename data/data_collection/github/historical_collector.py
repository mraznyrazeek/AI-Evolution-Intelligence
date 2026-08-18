import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests


# ============================================================
# AI Evolution Intelligence
# GitHub Historical Collector
# ============================================================

API_URL = "https://api.github.com/search/repositories"

SITE_NAME = "github"

# ------------------------------------------------------------
# Technology categories
# ------------------------------------------------------------

QUERIES = {
    "rag": "rag",
    "llm": "llm",
    "ai_agents": "ai agents",
    "mcp": "mcp",
    "multimodal_ai": "multimodal ai",
    "reasoning_ai": "reasoning ai",
}


# ------------------------------------------------------------
# Historical period
# ------------------------------------------------------------

START_YEAR = 2023
END_YEAR = 2026
END_MONTH = 8


# ------------------------------------------------------------
# Collection settings
# ------------------------------------------------------------

PER_PAGE = 100

# We only collect the first page for each
# technology/month combination.
#
# GitHub search results expose a total_count, so
# we can preserve both the actual sampled repositories
# and the broader matching count.
MAX_PAGES_PER_QUERY = 1

# Safety threshold for GitHub search API.
MIN_SEARCH_REMAINING = 5

# Delay between search requests.
REQUEST_DELAY = 2.5

# Request timeout.
REQUEST_TIMEOUT = 30


# ------------------------------------------------------------
# Output
# ------------------------------------------------------------

OUTPUT_DIR = Path(
    "data/raw/github/monthly"
)


# ============================================================
# Authentication
# ============================================================

def get_headers():
    """
    Read GITHUB_TOKEN from the environment.

    Never hard-code the token into this file.
    """

    token = os.getenv("GITHUB_TOKEN")

    if not token:

        print(
            "ERROR: GITHUB_TOKEN is not set."
        )

        print(
            "Set it in PowerShell before running "
            "the collector."
        )

        return None

    return {
        "Accept": (
            "application/vnd.github+json"
        ),

        "Authorization": (
            f"Bearer {token}"
        ),

        "X-GitHub-Api-Version": (
            "2026-03-10"
        ),

        "User-Agent": (
            "AI-Evolution-Intelligence"
        ),
    }


# ============================================================
# Rate limit
# ============================================================

def get_search_rate_limit(headers):
    """
    Check GitHub search API rate limit.

    /rate_limit does not consume the REST API quota.
    """

    try:

        response = requests.get(
            "https://api.github.com/rate_limit",
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )

    except requests.exceptions.RequestException as error:

        print(
            f"Rate-limit request failed: {error}"
        )

        return None

    if response.status_code != 200:

        print(
            "Unable to read GitHub rate limit."
        )

        print(
            response.text[:500]
        )

        return None

    data = response.json()

    search_data = (
        data
        .get("resources", {})
        .get("search", {})
    )

    return search_data


# ============================================================
# Search one technology for one month
# ============================================================

def collect_query(
    technology,
    query,
    start_date,
    end_date,
    headers,
):
    """
    Search GitHub repositories created within
    a specific monthly period.
    """

    all_records = []

    page = 1

    while page <= MAX_PAGES_PER_QUERY:

        search_query = (
            f"{query} "
            f"created:{start_date}..{end_date}"
        )

        params = {
            "q": search_query,
            "sort": "stars",
            "order": "desc",
            "per_page": PER_PAGE,
            "page": page,
        }

        try:

            response = requests.get(
                API_URL,
                headers=headers,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

        except requests.exceptions.RequestException as error:

            print(
                f"Request failed for "
                f"{technology}: {error}"
            )

            return (
                all_records,
                None,
                "error"
            )

        # ----------------------------------------------------
        # Read search rate-limit headers
        # ----------------------------------------------------

        remaining_header = (
            response.headers.get(
                "X-RateLimit-Remaining"
            )
        )

        reset_header = (
            response.headers.get(
                "X-RateLimit-Reset"
            )
        )

        print(
            f"Technology={technology} | "
            f"Period={start_date} to {end_date} | "
            f"Page={page} | "
            f"HTTP={response.status_code} | "
            f"Search remaining={remaining_header}"
        )

        # ----------------------------------------------------
        # Handle rate limit
        # ----------------------------------------------------

        if response.status_code in (
            403,
            429,
        ):

            print(
                "\nGitHub search rate limit reached."
            )

            if reset_header:

                try:

                    reset_timestamp = int(
                        reset_header
                    )

                    now_timestamp = int(
                        time.time()
                    )

                    wait_seconds = max(
                        reset_timestamp
                        - now_timestamp
                        + 5,
                        5,
                    )

                    print(
                        f"Waiting approximately "
                        f"{wait_seconds} seconds "
                        f"until reset."
                    )

                    time.sleep(
                        wait_seconds
                    )

                    continue

                except ValueError:

                    pass

            print(
                "Unable to determine reset time."
            )

            return (
                all_records,
                None,
                "rate_limited"
            )

        # ----------------------------------------------------
        # Handle other errors
        # ----------------------------------------------------

        if response.status_code != 200:

            print(
                "GitHub API response:"
            )

            print(
                response.text[:500]
            )

            return (
                all_records,
                None,
                "error"
            )

        # ----------------------------------------------------
        # Parse response
        # ----------------------------------------------------

        data = response.json()

        total_count = data.get(
            "total_count",
            0
        )

        items = data.get(
            "items",
            []
        )

        print(
            f"Matching repositories: "
            f"{total_count}"
        )

        print(
            f"Repositories returned: "
            f"{len(items)}"
        )

        # ----------------------------------------------------
        # Save repository records
        # ----------------------------------------------------

        for item in items:

            record = {

                "source": SITE_NAME,

                "technology": technology,

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

                "data": {

                    "id": item.get("id"),

                    "full_name": item.get(
                        "full_name"
                    ),

                    "name": item.get(
                        "name"
                    ),

                    "owner": (
                        item.get("owner", {})
                        .get("login")
                    ),

                    "description": item.get(
                        "description"
                    ),

                    "html_url": item.get(
                        "html_url"
                    ),

                    "created_at": item.get(
                        "created_at"
                    ),

                    "updated_at": item.get(
                        "updated_at"
                    ),

                    "pushed_at": item.get(
                        "pushed_at"
                    ),

                    "stargazers_count": item.get(
                        "stargazers_count"
                    ),

                    "watchers_count": item.get(
                        "watchers_count"
                    ),

                    "forks_count": item.get(
                        "forks_count"
                    ),

                    "open_issues_count": item.get(
                        "open_issues_count"
                    ),

                    "language": item.get(
                        "language"
                    ),

                    "topics": item.get(
                        "topics",
                        []
                    ),

                    "license": (
                        item.get("license", {})
                        .get("spdx_id")
                        if item.get("license")
                        else None
                    ),

                    "archived": item.get(
                        "archived"
                    ),

                    "disabled": item.get(
                        "disabled"
                    ),

                    "default_branch": item.get(
                        "default_branch"
                    ),
                },
            }

            all_records.append(
                record
            )

        # ----------------------------------------------------
        # Check search quota
        # ----------------------------------------------------

        try:

            remaining = int(
                remaining_header
            )

        except (
            TypeError,
            ValueError,
        ):

            remaining = None

        if (
            remaining is not None
            and remaining <= MIN_SEARCH_REMAINING
        ):

            print(
                "\nWARNING:"
            )

            print(
                "GitHub search quota is low."
            )

            print(
                f"Remaining search requests: "
                f"{remaining}"
            )

            return (
                all_records,
                remaining,
                "low_quota"
            )

        # ----------------------------------------------------
        # Pagination
        # ----------------------------------------------------

        if not data.get(
            "incomplete_results",
            False
        ):

            # We intentionally only collect
            # MAX_PAGES_PER_QUERY.
            pass

        page += 1

        if page <= MAX_PAGES_PER_QUERY:

            time.sleep(
                REQUEST_DELAY
            )

    return (
        all_records,
        remaining,
        "completed"
    )


# ============================================================
# Monthly collection
# ============================================================

def collect_month(
    year,
    month,
    headers,
):
    """
    Collect one complete month.
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

    month_name = (
        f"{year}-{month:02d}"
    )

    output_file = (
        OUTPUT_DIR
        / f"github_{month_name}.json"
    )

    # --------------------------------------------------------
    # Resume protection
    # --------------------------------------------------------

    if output_file.exists():

        print(
            f"\nSKIPPING {month_name}"
        )

        print(
            f"Already collected: "
            f"{output_file}"
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

    technology_statistics = {}

    # --------------------------------------------------------
    # Collect each technology
    # --------------------------------------------------------

    for technology, query in QUERIES.items():

        records, remaining, status = (
            collect_query(
                technology,
                query,
                start_date,
                end_date,
                headers,
            )
        )

        month_records.extend(
            records
        )

        technology_statistics[
            technology
        ] = {

            "query": query,

            "matching_repository_count": (
                None
            ),

            "records_collected": (
                len(records)
            ),
        }

        if status in (
            "rate_limited",
            "low_quota",
            "error",
        ):

            print(
                "\nMonth was not completed."
            )

            print(
                f"Status: {status}"
            )

            print(
                "The month will be retried "
                "on the next run."
            )

            return "paused"

        time.sleep(
            REQUEST_DELAY
        )

    # --------------------------------------------------------
    # Deduplicate repositories
    # --------------------------------------------------------

    print(
        "\nRemoving duplicate repositories..."
    )

    unique_records = {}

    for record in month_records:

        repository_id = (
            record["data"]
            .get("id")
        )

        if repository_id is not None:

            unique_records[
                repository_id
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

    # --------------------------------------------------------
    # Build output
    # --------------------------------------------------------

    output = {

        "metadata": {

            "source": "GitHub",

            "collection_type": (
                "monthly_repository_search"
            ),

            "period_start": start_date,

            "period_end": end_date,

            "technologies": QUERIES,

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

            "pages_per_query": (
                MAX_PAGES_PER_QUERY
            ),

            "per_page": PER_PAGE,
        },

        "technology_statistics": (
            technology_statistics
        ),

        "records": final_records,
    }

    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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


# ============================================================
# Main
# ============================================================

def main():

    print(
        "=" * 70
    )

    print(
        "AI Evolution Intelligence"
    )

    print(
        "GitHub Historical Collector"
    )

    print(
        "=" * 70
    )

    print(
        f"Study period: "
        f"{START_YEAR}-01 → "
        f"{END_YEAR}-{END_MONTH:02d}"
    )

    print(
        f"Technologies: "
        f"{len(QUERIES)}"
    )

    print(
        f"Output directory: "
        f"{OUTPUT_DIR}"
    )

    print(
        "=" * 70
    )

    # --------------------------------------------------------
    # Authentication
    # --------------------------------------------------------

    headers = get_headers()

    if headers is None:

        return

    # --------------------------------------------------------
    # Check authentication/rate limit
    # --------------------------------------------------------

    rate_limit = (
        get_search_rate_limit(
            headers
        )
    )

    if rate_limit:

        print(
            "\nGitHub Search API"
        )

        print(
            f"Limit: "
            f"{rate_limit.get('limit')}"
        )

        print(
            f"Remaining: "
            f"{rate_limit.get('remaining')}"
        )

        reset_timestamp = (
            rate_limit.get("reset")
        )

        if reset_timestamp:

            reset_time = (
                datetime.fromtimestamp(
                    reset_timestamp,
                    tz=timezone.utc
                )
            )

            print(
                f"Reset: "
                f"{reset_time.isoformat()}"
            )

        if (
            rate_limit.get("remaining", 0)
            <= MIN_SEARCH_REMAINING
        ):

            print(
                "\nGitHub search quota is "
                "too low to begin."
            )

            print(
                "Please wait for the reset."
            )

            return

    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Collect historical months
    # --------------------------------------------------------

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
                month,
                headers,
            )

            if status == "paused":

                print(
                    "\n" + "=" * 70
                )

                print(
                    "COLLECTION PAUSED"
                )

                print(
                    "Completed monthly files "
                    "have been preserved."
                )

                print(
                    "Run the same command again "
                    "after the GitHub search "
                    "rate limit resets."
                )

                print(
                    "=" * 70
                )

                return

    # --------------------------------------------------------
    # Finished
    # --------------------------------------------------------

    print(
        "\n" + "=" * 70
    )

    print(
        "ALL AVAILABLE MONTHS COLLECTED"
    )

    print(
        "=" * 70
    )


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":

    main()