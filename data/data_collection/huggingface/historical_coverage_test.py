from datetime import datetime, timezone

from huggingface_hub import HfApi


# ============================================================
# AI Evolution Intelligence
# Hugging Face Historical Test
# January 2023
# ============================================================

api = HfApi()

START_DATE = datetime(
    2023, 1, 1,
    tzinfo=timezone.utc
)

END_DATE = datetime(
    2023, 2, 1,
    tzinfo=timezone.utc
)


QUERIES = {
    "llm": "llm",
    "text_generation": "text-generation",
    "multimodal": "multimodal",
    "reasoning": "reasoning",
    "embedding": "embedding",
}


def is_in_period(model):

    created_at = getattr(
        model,
        "created_at",
        None
    )

    if created_at is None:
        return False

    return (
        START_DATE
        <= created_at
        < END_DATE
    )


def test_query(
    category,
    query
):

    print()
    print("-" * 70)
    print(f"Testing: {category}")
    print(f"Search: {query}")
    print("-" * 70)

    checked = 0

    found = []

    try:

        models = api.list_models(
            search=query,
            sort="createdAt",
            limit=100,
        )

        for model in models:

            checked += 1

            if is_in_period(model):

                found.append(model)

                print(
                    f"FOUND: {model.id}"
                )

                print(
                    f"Created: "
                    f"{model.created_at}"
                )

                print(
                    f"Downloads: "
                    f"{getattr(model, 'downloads', 0)}"
                )

                print(
                    f"Likes: "
                    f"{getattr(model, 'likes', 0)}"
                )

                print()

        print(
            f"Models checked: {checked}"
        )

        print(
            f"Models found in January 2023: "
            f"{len(found)}"
        )

    except Exception as error:

        print(
            f"ERROR: {error}"
        )


def main():

    print("=" * 70)
    print("AI Evolution Intelligence")
    print("Hugging Face Historical Coverage Test")
    print("January 2023")
    print("=" * 70)

    for category, query in QUERIES.items():

        test_query(
            category,
            query
        )

    print()
    print("=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()