from pathlib import Path
import json
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

GITHUB_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "github"
    / "monthly"
)

STACKOVERFLOW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "stackoverflow"
    / "monthly"
)

HUGGINGFACE_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "huggingface"
    / "monthly"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "monthly_ai_signals.csv"
)


# ============================================================
# RESEARCH TAXONOMY
# ============================================================

TECHNOLOGIES = [
    "ai_agents",
    "llm",
    "mcp",
    "multimodal_ai",
    "rag",
    "reasoning_ai",
]


# ============================================================
# HELPERS
# ============================================================

def load_json(path):
    """Load a JSON file safely."""

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def normalize_text(value):
    """Normalize text for keyword matching."""

    if value is None:
        return ""

    return str(value).strip().lower()


def record_text(record):
    """
    Build searchable text from Hugging Face metadata.

    We use categories, tags, pipeline tag, library name,
    model ID and model metadata.
    """

    categories = record.get(
        "categories",
        []
    )

    tags = record.get(
        "tags",
        []
    )

    if not isinstance(categories, list):
        categories = [categories]

    if not isinstance(tags, list):
        tags = [tags]

    values = []

    values.extend(categories)
    values.extend(tags)

    values.append(
        record.get("pipeline_tag", "")
    )

    values.append(
        record.get("library_name", "")
    )

    values.append(
        record.get("model_id", "")
    )

    return " ".join(
        normalize_text(value)
        for value in values
        if value is not None
    )


# ============================================================
# HUGGING FACE CLASSIFICATION
# ============================================================

def classify_huggingface_record(record):
    """
    Determine which research technologies a Hugging Face
    model belongs to.

    IMPORTANT:
    We do NOT assume that text_generation == every LLM
    or embedding == RAG.

    Instead, explicit category mappings and meaningful
    tags are used.
    """

    categories = record.get(
        "categories",
        []
    )

    tags = record.get(
        "tags",
        []
    )

    if not isinstance(categories, list):
        categories = [categories]

    if not isinstance(tags, list):
        tags = [tags]

    categories = {
        normalize_text(value)
        for value in categories
    }

    tags = {
        normalize_text(value)
        for value in tags
    }

    text = record_text(record)

    matched = set()

    # --------------------------------------------------------
    # LLM
    # --------------------------------------------------------
    #
    # Hugging Face explicitly uses:
    #   llm
    #   text_generation
    #
    # We count text-generation models as part of the LLM
    # ecosystem because the dataset is measuring modern
    # foundation/generative model activity.
    # --------------------------------------------------------

    if (
        "llm" in categories
        or "text_generation" in categories
        or "text-generation" in tags
        or "llm" in tags
    ):
        matched.add("llm")

    # --------------------------------------------------------
    # MULTIMODAL AI
    # --------------------------------------------------------

    if (
        "multimodal" in categories
        or "multimodal" in tags
        or "multimodal-ai" in tags
        or "multimodal_ai" in tags
    ):
        matched.add("multimodal_ai")

    # --------------------------------------------------------
    # REASONING AI
    # --------------------------------------------------------

    if (
        "reasoning" in categories
        or "reasoning" in tags
        or "reasoning-ai" in tags
        or "reasoning_ai" in tags
    ):
        matched.add("reasoning_ai")

    # --------------------------------------------------------
    # RAG
    # --------------------------------------------------------

    rag_keywords = {
        "rag",
        "retrieval-augmented-generation",
        "retrieval_augmented_generation",
        "retrieval augmented generation",
    }

    if (
        categories.intersection(rag_keywords)
        or tags.intersection(rag_keywords)
        or "retrieval-augmented-generation" in text
        or "retrieval_augmented_generation" in text
    ):
        matched.add("rag")

    # --------------------------------------------------------
    # AI AGENTS
    # --------------------------------------------------------

    agent_keywords = {
        "agent",
        "agents",
        "ai-agent",
        "ai-agents",
        "ai_agent",
        "ai_agents",
        "agentic",
        "agentic-ai",
        "agentic_ai",
    }

    if (
        categories.intersection(agent_keywords)
        or tags.intersection(agent_keywords)
    ):
        matched.add("ai_agents")

    # --------------------------------------------------------
    # MCP
    # --------------------------------------------------------

    mcp_keywords = {
        "mcp",
        "model-context-protocol",
        "model_context_protocol",
        "model context protocol",
    }

    if (
        categories.intersection(mcp_keywords)
        or tags.intersection(mcp_keywords)
        or "model context protocol" in text
        or "model-context-protocol" in text
    ):
        matched.add("mcp")

    return matched


# ============================================================
# GITHUB
# ============================================================

def process_github():

    print("\n" + "=" * 70)
    print("PROCESSING GITHUB")
    print("=" * 70)

    rows = []

    files = sorted(
        GITHUB_DIR.glob(
            "github_*.json"
        )
    )

    for path in files:

        print(
            f"Reading: {path.name}"
        )

        try:
            document = load_json(path)

        except Exception as error:

            print(
                f"WARNING: Could not read "
                f"{path.name}: {error}"
            )

            continue

        records = document.get(
            "records",
            []
        )

        for record in records:

            technology = record.get(
                "technology"
            )

            if technology not in TECHNOLOGIES:
                continue

            data = record.get(
                "data",
                {}
            )

            month = record.get(
                "collection_period_start",
                ""
            )[:7]

            rows.append({

                "month": month,

                "technology": technology,

                "github_activity": 1,

                "github_stars": data.get(
                    "stargazers_count",
                    0
                ),

                "github_forks": data.get(
                    "forks_count",
                    0
                ),

                "github_issues": data.get(
                    "open_issues_count",
                    0
                ),
            })

    if not rows:
        return pd.DataFrame(
            columns=[
                "month",
                "technology",
                "github_activity",
                "github_stars",
                "github_forks",
                "github_issues",
            ]
        )

    df = pd.DataFrame(rows)

    return (
        df
        .groupby(
            ["month", "technology"],
            as_index=False
        )
        .agg({
            "github_activity": "sum",
            "github_stars": "sum",
            "github_forks": "sum",
            "github_issues": "sum",
        })
    )


# ============================================================
# STACK OVERFLOW
# ============================================================

def process_stackoverflow():

    print("\n" + "=" * 70)
    print("PROCESSING STACK OVERFLOW")
    print("=" * 70)

    rows = []

    files = sorted(
        STACKOVERFLOW_DIR.glob(
            "stackoverflow_*.json"
        )
    )

    for path in files:

        print(
            f"Reading: {path.name}"
        )

        try:
            document = load_json(path)

        except Exception as error:

            print(
                f"WARNING: Could not read "
                f"{path.name}: {error}"
            )

            continue

        records = document.get(
            "records",
            []
        )

        for record in records:

            search_query = normalize_text(
                record.get(
                    "search_query"
                )
            )

            # --------------------------------------------
            # Map Stack Overflow search terms to taxonomy.
            # --------------------------------------------

            if search_query in {
                "ai-agent",
                "ai-agents",
                "agent",
                "agents",
            }:
                technology = "ai_agents"

            elif search_query == "llm":
                technology = "llm"

            elif search_query == "mcp":
                technology = "mcp"

            elif search_query in {
                "multimodal",
                "multimodal-ai",
                "multimodal_ai",
            }:
                technology = "multimodal_ai"

            elif search_query == "rag":
                technology = "rag"

            elif search_query in {
                "reasoning",
                "reasoning-ai",
                "reasoning_ai",
            }:
                technology = "reasoning_ai"

            else:
                continue

            data = record.get(
                "data",
                {}
            )

            month = record.get(
                "collection_period_start",
                ""
            )[:7]

            rows.append({

                "month": month,

                "technology": technology,

                "stackoverflow_questions": 1,

                "stackoverflow_views": data.get(
                    "view_count",
                    0
                ),

                "stackoverflow_answers": data.get(
                    "answer_count",
                    0
                ),

                "stackoverflow_score": data.get(
                    "score",
                    0
                ),
            })

    if not rows:
        return pd.DataFrame(
            columns=[
                "month",
                "technology",
                "stackoverflow_questions",
                "stackoverflow_views",
                "stackoverflow_answers",
                "stackoverflow_score",
            ]
        )

    df = pd.DataFrame(rows)

    return (
        df
        .groupby(
            ["month", "technology"],
            as_index=False
        )
        .agg({
            "stackoverflow_questions": "sum",
            "stackoverflow_views": "sum",
            "stackoverflow_answers": "sum",
            "stackoverflow_score": "sum",
        })
    )


# ============================================================
# HUGGING FACE
# ============================================================

def process_huggingface():

    print("\n" + "=" * 70)
    print("PROCESSING HUGGING FACE")
    print("=" * 70)

    rows = []

    files = sorted(
        HUGGINGFACE_DIR.glob(
            "huggingface_*.json"
        )
    )

    for path in files:

        print(
            f"Reading: {path.name}"
        )

        try:
            document = load_json(path)

        except Exception as error:

            print(
                f"WARNING: Could not read "
                f"{path.name}: {error}"
            )

            continue

        records = document.get(
            "records",
            []
        )

        month = path.stem.replace(
            "huggingface_",
            ""
        )

        counts = {
            technology: 0
            for technology in TECHNOLOGIES
        }

        for record in records:

            matched = classify_huggingface_record(
                record
            )

            for technology in matched:

                if technology in counts:

                    counts[technology] += 1

        for technology in TECHNOLOGIES:

            rows.append({

                "month": month,

                "technology": technology,

                "huggingface_models": counts[
                    technology
                ],

            })

    if not rows:

        return pd.DataFrame(
            columns=[
                "month",
                "technology",
                "huggingface_models",
            ]
        )

    return pd.DataFrame(rows)


# ============================================================
# BUILD COMPLETE MONTH × TECHNOLOGY GRID
# ============================================================

def build_grid(
    start_month="2023-01",
    end_month="2026-08"
):

    months = pd.date_range(
        start=start_month,
        end=end_month,
        freq="MS"
    ).strftime(
        "%Y-%m"
    ).tolist()

    grid = pd.MultiIndex.from_product(
        [
            months,
            TECHNOLOGIES
        ],
        names=[
            "month",
            "technology"
        ]
    ).to_frame(
        index=False
    )

    return grid


# ============================================================
# MAIN MERGE
# ============================================================

def main():

    print("=" * 70)
    print("MERGING DATA SOURCES")
    print("=" * 70)

    github = process_github()

    stackoverflow = process_stackoverflow()

    huggingface = process_huggingface()

    # --------------------------------------------------------
    # Build complete 44-month × 6-technology grid
    # --------------------------------------------------------

    unified = build_grid()

    # --------------------------------------------------------
    # Merge GitHub
    # --------------------------------------------------------

    unified = unified.merge(
        github,
        on=[
            "month",
            "technology"
        ],
        how="left"
    )

    # --------------------------------------------------------
    # Merge Stack Overflow
    # --------------------------------------------------------

    unified = unified.merge(
        stackoverflow,
        on=[
            "month",
            "technology"
        ],
        how="left"
    )

    # --------------------------------------------------------
    # Merge Hugging Face
    # --------------------------------------------------------

    unified = unified.merge(
        huggingface,
        on=[
            "month",
            "technology"
        ],
        how="left"
    )

    # --------------------------------------------------------
    # Fill GitHub / Stack Overflow missing values with zero.
    #
    # Hugging Face is handled separately because historical
    # coverage begins in July 2024.
    # --------------------------------------------------------

    github_columns = [
        "github_activity",
        "github_stars",
        "github_forks",
        "github_issues",
    ]

    stackoverflow_columns = [
        "stackoverflow_questions",
        "stackoverflow_views",
        "stackoverflow_answers",
        "stackoverflow_score",
    ]

    for column in (
        github_columns
        + stackoverflow_columns
    ):

        unified[column] = (
            unified[column]
            .fillna(0)
        )

    # --------------------------------------------------------
    # Hugging Face coverage
    # --------------------------------------------------------

    unified["huggingface_available"] = (
        unified["month"] >= "2024-07"
    ).astype(int)

    # IMPORTANT:
    #
    # Do NOT replace pre-July-2024 HF values with zero.
    #
    # NaN means:
    # "Hugging Face historical snapshot unavailable"
    #
    # Zero after July 2024 means:
    # "Snapshot available, but no matching models detected."
    # --------------------------------------------------------

    unified.loc[
        unified["huggingface_available"] == 0,
        "huggingface_models"
    ] = pd.NA

    # --------------------------------------------------------
    # Numeric ordering
    # --------------------------------------------------------

    unified = unified.sort_values(
        [
            "month",
            "technology"
        ]
    ).reset_index(
        drop=True
    )

    # --------------------------------------------------------
    # Output
    # --------------------------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    unified.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ========================================================
    # VALIDATION / REPORT
    # ========================================================

    print("\n" + "=" * 70)
    print("UNIFIED DATASET CREATED")
    print("=" * 70)

    print(
        f"Output: {OUTPUT_FILE}"
    )

    print(
        f"Rows: {len(unified)}"
    )

    print(
        f"Columns: {len(unified.columns)}"
    )

    print("\nColumns:")

    for column in unified.columns:

        print(
            f"  - {column}"
        )

    print("\nTechnology counts:")

    print(
        unified[
            "technology"
        ].value_counts().sort_index()
    )

    print("\nDate range:")

    print(
        f"{unified['month'].min()} "
        f"→ "
        f"{unified['month'].max()}"
    )

    expected_rows = (
        44
        * len(TECHNOLOGIES)
    )

    print("\nExpected rows:")

    print(
        f"44 months × "
        f"{len(TECHNOLOGIES)} technologies "
        f"= {expected_rows}"
    )

    print(
        f"Actual rows: {len(unified)}"
    )

    print("\nHugging Face coverage:")

    print(
        unified[
            "huggingface_available"
        ].value_counts().sort_index()
    )

    print("\nHugging Face model counts:")

    hf_summary = (
        unified[
            unified[
                "huggingface_available"
            ] == 1
        ]
        .groupby(
            "technology"
        )[
            "huggingface_models"
        ]
        .agg(
            [
                "count",
                "sum",
                "min",
                "max"
            ]
        )
    )

    print(
        hf_summary
    )

    print("\nFirst 20 rows:")

    print(
        unified.head(20).to_string(
            index=False
        )
    )

    # --------------------------------------------------------
    # Final structural validation
    # --------------------------------------------------------

    assert len(unified) == expected_rows

    assert set(
        unified["technology"].unique()
    ) == set(
        TECHNOLOGIES
    )

    assert (
        unified[
            "month"
        ].nunique()
        == 44
    )

    print("\n" + "=" * 70)
    print("PROCESSING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()