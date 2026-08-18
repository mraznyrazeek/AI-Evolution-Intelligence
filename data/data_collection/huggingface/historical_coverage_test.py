from huggingface_hub import HfApi


api = HfApi()


QUERIES = [
    "llm",
    "text-generation",
    "multimodal",
    "reasoning",
    "embedding",
]


PERIODS = [
    ("2023", "2023-01-01", "2023-12-31"),
    ("2024", "2024-01-01", "2024-12-31"),
    ("2025", "2025-01-01", "2025-12-31"),
    ("2026", "2026-01-01", "2026-08-31"),
]


def check_query(query, start_date, end_date):

    try:

        models = api.list_models(
            search=query,
            sort="created_at",
            limit=100,
        )

        checked = 0

        for model in models:

            checked += 1

            if model.created_at is None:
                continue

            created_date = (
                model.created_at
                .date()
                .isoformat()
            )

            if start_date <= created_date <= end_date:

                return {
                    "found": True,
                    "model": model.id,
                    "created": created_date,
                    "checked": checked,
                }

            # Since results are ordered by creation date,
            # once we move earlier than the target period,
            # there is no need to continue.
            if created_date < start_date:

                break

        return {
            "found": False,
            "checked": checked,
        }

    except Exception as error:

        return {
            "error": str(error),
        }


def main():

    print("=" * 70)
    print("Hugging Face Historical Coverage Test")
    print("Pagination / Historical Validation")
    print("=" * 70)

    for year, start_date, end_date in PERIODS:

        print(f"\n### {year}")

        for query in QUERIES:

            print(f"\nTesting: {query}")

            result = check_query(
                query,
                start_date,
                end_date,
            )

            if "error" in result:

                print(
                    f"ERROR: {result['error']}"
                )

            elif result["found"]:

                print(
                    "FOUND"
                )

                print(
                    f"Model: {result['model']}"
                )

                print(
                    f"Created: {result['created']}"
                )

                print(
                    f"Models checked: {result['checked']}"
                )

            else:

                print(
                    "NO MODEL FOUND"
                )

                print(
                    f"Models checked: {result['checked']}"
                )


if __name__ == "__main__":
    main()