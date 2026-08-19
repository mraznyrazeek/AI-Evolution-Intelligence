import json
import time
from datetime import datetime, timezone
from pathlib import Path

from datasets import load_dataset
from huggingface_hub import HfApi


# ============================================================
# AI Evolution Intelligence
# Hugging Face Monthly Snapshot Collector
# ============================================================

REPO_ID = "hfmlsoc/hub_weekly_snapshots"

START_YEAR = 2024
START_MONTH = 7

END_YEAR = 2026
END_MONTH = 8

OUTPUT_DIR = Path(
    "data/raw/huggingface/monthly"
)

CACHE_DIR = Path(
    "data/raw/huggingface/cache"
)


# ------------------------------------------------------------
# AI technology classification
# ------------------------------------------------------------

CATEGORY_KEYWORDS = {

    "llm": [
        "llm",
        "language-model",
        "large-language-model",
        "chat",
        "chatbot",
        "conversational",
        "instruction",
        "instruct",
    ],

    "text_generation": [
        "text-generation",
        "text_generation",
        "causal-lm",
        "causal-language-model",
    ],

    "multimodal": [
        "multimodal",
        "vision-language",
        "vision-language-model",
        "image-text",
        "image-text-to-text",
        "audio-text",
        "video-text",
    ],

    "reasoning": [
        "reasoning",
        "chain-of-thought",
        "cot",
        "math",
        "reasoner",
    ],

    "embedding": [
        "embedding",
        "text-embedding",
        "sentence-similarity",
        "feature-extraction",
    ],
}


def classify_model(
    pipeline_tag,
    tags,
):

    values = []

    if pipeline_tag:
        values.append(
            str(pipeline_tag).lower()
        )

    if tags:

        values.extend(
            str(tag).lower()
            for tag in tags
        )

    combined_text = " ".join(
        values
    )

    categories = []

    for category, keywords in (
        CATEGORY_KEYWORDS.items()
    ):

        for keyword in keywords:

            if keyword in combined_text:

                categories.append(
                    category
                )

                break

    if not categories:

        return ["other"]

    return categories


def get_available_snapshots():

    print(
        "\nChecking available "
        "Hugging Face snapshots..."
    )

    api = HfApi()

    files = api.list_repo_files(
        repo_id=REPO_ID,
        repo_type="dataset",
    )

    snapshots = []

    for file_path in files:

        if not (
            file_path.startswith(
                "models/"
            )
            and file_path.endswith(
                "/models.parquet"
            )
        ):

            continue

        parts = file_path.split("/")

        if len(parts) != 3:

            continue

        date_string = parts[1]

        try:

            datetime.strptime(
                date_string,
                "%Y-%m-%d"
            )

            snapshots.append(
                date_string
            )

        except ValueError:

            continue

    snapshots = sorted(
        set(snapshots)
    )

    return snapshots


def target_months():

    months = []

    year = START_YEAR
    month = START_MONTH

    while True:

        months.append(
            f"{year}-{month:02d}"
        )

        if (
            year == END_YEAR
            and month == END_MONTH
        ):

            break

        month += 1

        if month == 13:

            month = 1
            year += 1

    return months


def choose_monthly_snapshots(
    available_snapshots
):

    selected = {}

    for month in target_months():

        matching = [
            date
            for date in available_snapshots
            if date.startswith(month)
        ]

        if not matching:

            print(
                f"WARNING: No snapshot "
                f"available for {month}"
            )

            continue

        # ----------------------------------------------------
        # Choose the last available weekly snapshot
        # within the month.
        # ----------------------------------------------------

        selected[month] = matching[-1]

    return selected


def process_snapshot(
    month,
    snapshot_date,
):

    output_file = (
        OUTPUT_DIR
        / f"huggingface_{month}.json"
    )

    # --------------------------------------------------------
    # Resume protection
    # --------------------------------------------------------

    if output_file.exists():

        print()
        print(
            f"SKIPPING {month}"
        )

        print(
            "Already collected:"
        )

        print(
            output_file
        )

        return "skipped"

    print()
    print("=" * 70)

    print(
        f"COLLECTING: {month}"
    )

    print(
        f"Snapshot: {snapshot_date}"
    )

    print("=" * 70)

    file_path = (
        f"models/"
        f"{snapshot_date}/"
        f"models.parquet"
    )

    try:

        dataset = load_dataset(
            REPO_ID,
            data_files={
                "models": file_path
            },
            cache_dir=str(
                CACHE_DIR
            ),
        )

    except Exception as error:

        print()
        print(
            "ERROR loading snapshot:"
        )

        print(error)

        return "error"

    models = dataset["models"]

    print(
        f"Snapshot rows: "
        f"{len(models)}"
    )

    records = []

    category_counts = {}

    # --------------------------------------------------------
    # Process models
    # --------------------------------------------------------

    for row in models:

        pipeline_tag = row.get(
            "pipeline_tag"
        )

        tags = row.get(
            "tags"
        ) or []

        categories = classify_model(
            pipeline_tag,
            tags,
        )

        # ----------------------------------------------------
        # Keep AI-relevant models only.
        # ----------------------------------------------------

        if categories == ["other"]:

            continue

        created_at = row.get(
            "createdAt"
        )

        record = {

            "source": (
                "huggingface"
            ),

            "snapshot_date": (
                snapshot_date
            ),

            "analysis_month": month,

            "model_id": row.get(
                "id"
            ),

            "model_id_original": row.get(
                "modelId"
            ),

            "created_at": (
                created_at.isoformat()
                if hasattr(created_at, "isoformat")
                else created_at
            ),

            "likes": row.get(
                "likes"
            ),

            "downloads": row.get(
                "downloads"
            ),

            "pipeline_tag": (
                pipeline_tag
            ),

            "library_name": row.get(
                "library_name"
            ),

            "tags": tags,

            "categories": categories,

            "private": row.get(
                "private"
            ),
        }

        records.append(
            record
        )

        for category in categories:

            category_counts[
                category
            ] = (
                category_counts.get(
                    category,
                    0
                ) + 1
            )

    # --------------------------------------------------------
    # Output metadata
    # --------------------------------------------------------

    output = {

        "metadata": {

            "source": (
                "Hugging Face Hub"
            ),

            "dataset": REPO_ID,

            "collection_type": (
                "monthly_snapshot"
            ),

            "analysis_month": month,

            "snapshot_date": (
                snapshot_date
            ),

            "snapshot_total_rows": (
                len(models)
            ),

            "ai_relevant_rows": (
                len(records)
            ),

            "category_counts": (
                category_counts
            ),

            "collection_timestamp": (
                datetime.now(
                    timezone.utc
                ).isoformat()
            ),
        },

        "records": records,
    }

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

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

    print()

    print(
        "AI-relevant models:"
    )

    print(
        len(records)
    )

    print()

    print(
        "Category counts:"
    )

    for category, count in sorted(
        category_counts.items()
    ):

        print(
            f"  {category}: "
            f"{count}"
        )

    print()

    print(
        f"Saved to: {output_file}"
    )

    return "completed"


def main():

    print("=" * 70)

    print(
        "AI Evolution Intelligence"
    )

    print(
        "Hugging Face Monthly Snapshot Collector"
    )

    print("=" * 70)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    CACHE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # --------------------------------------------------------
    # Discover available snapshots
    # --------------------------------------------------------

    available_snapshots = (
        get_available_snapshots()
    )

    print()

    print(
        f"Available model snapshots: "
        f"{len(available_snapshots)}"
    )

    if available_snapshots:

        print(
            f"Earliest available: "
            f"{available_snapshots[0]}"
        )

        print(
            f"Latest available: "
            f"{available_snapshots[-1]}"
        )

    # --------------------------------------------------------
    # Select one snapshot per month
    # --------------------------------------------------------

    selected = (
        choose_monthly_snapshots(
            available_snapshots
        )
    )

    print()
    print("=" * 70)
    print("SELECTED MONTHLY SNAPSHOTS")
    print("=" * 70)

    for month, snapshot in selected.items():

        print(
            f"{month} → {snapshot}"
        )

    # --------------------------------------------------------
    # Collect
    # --------------------------------------------------------

    for month, snapshot in (
        selected.items()
    ):

        status = process_snapshot(
            month,
            snapshot
        )

        if status == "error":

            print()
            print(
                "Collection stopped because "
                "a snapshot could not be loaded."
            )

            return

        time.sleep(1)

    print()
    print("=" * 70)
    print(
        "HUGGING FACE COLLECTION COMPLETE"
    )
    print("=" * 70)


if __name__ == "__main__":

    main()