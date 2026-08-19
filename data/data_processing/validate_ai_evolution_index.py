from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# AI EVOLUTION INTELLIGENCE
# AI EVOLUTION INDEX VALIDATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_evolution_index.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_evolution_index_validation.csv"
)


TECHNOLOGIES = [
    "ai_agents",
    "llm",
    "mcp",
    "multimodal_ai",
    "rag",
    "reasoning_ai",
]


# ============================================================
# LOAD
# ============================================================

print("=" * 70)
print("AI EVOLUTION INTELLIGENCE")
print("AI EVOLUTION INDEX VALIDATION")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

df["month"] = pd.to_datetime(df["month"])

df = df.sort_values(
    ["technology", "month"]
).reset_index(drop=True)

print("\nInput:")
print(INPUT_FILE)

print(f"\nRows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# 1. STRUCTURAL VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("1. STRUCTURAL VALIDATION")
print("-" * 70)

expected_rows = 44 * 6

print(
    f"Expected rows: {expected_rows}"
)

print(
    f"Actual rows:   {len(df)}"
)

assert len(df) == expected_rows

assert (
    df["month"].nunique()
    == 44
)

assert (
    df["technology"].nunique()
    == 6
)

assert set(
    df["technology"].unique()
) == set(
    TECHNOLOGIES
)

print("PASS: Structure is correct.")


# ============================================================
# 2. SCORE RANGE
# ============================================================

print("\n" + "-" * 70)
print("2. SCORE RANGE VALIDATION")
print("-" * 70)

score_columns = [
    "development_score",
    "developer_interest_score",
    "model_ecosystem_score",
    "ai_evolution_score",
]

for column in score_columns:

    minimum = df[column].min()
    maximum = df[column].max()

    print(
        f"{column}: "
        f"{minimum:.3f} → "
        f"{maximum:.3f}"
    )

    if column != "model_ecosystem_score":

        assert minimum >= 0
        assert maximum <= 100

print("PASS: Index scores are within expected range.")


# ============================================================
# 3. MISSING VALUE VALIDATION
# ============================================================

print("\n" + "-" * 70)
print("3. MISSING VALUE VALIDATION")
print("-" * 70)

missing = (
    df[
        [
            "development_score",
            "developer_interest_score",
            "ai_evolution_score",
        ]
    ]
    .isna()
    .sum()
)

print(missing)

assert (
    missing.sum()
    == 0
)

print(
    "PASS: Core index contains no missing values."
)


# ============================================================
# 4. HUGGING FACE COVERAGE
# ============================================================

print("\n" + "-" * 70)
print("4. HUGGING FACE COVERAGE")
print("-" * 70)

hf_coverage = (
    df.groupby(
        "month"
    )[
        "huggingface_available"
    ]
    .first()
)

print(
    "\nFirst HF-covered month:"
)

hf_months = hf_coverage[
    hf_coverage == 1
]

print(
    hf_months.index.min()
)

print(
    "\nHF coverage months:"
)

print(
    hf_months.count()
)

assert (
    hf_months.count()
    == 26
)

print(
    "PASS: Hugging Face coverage = 26 months."
)


# ============================================================
# 5. SOURCE CONTRIBUTION
# ============================================================

print("\n" + "-" * 70)
print("5. SOURCE CONTRIBUTION ANALYSIS")
print("-" * 70)

source_columns = [
    "development_score",
    "developer_interest_score",
    "model_ecosystem_score",
]

source_summary = (
    df[
        source_columns
    ]
    .describe()
    .T
)

print(
    source_summary[
        [
            "mean",
            "std",
            "min",
            "50%",
            "max",
        ]
    ].to_string()
)


# ============================================================
# 6. LATEST RANKING
# ============================================================

print("\n" + "-" * 70)
print("6. LATEST TECHNOLOGY RANKING")
print("-" * 70)

latest_month = (
    df["month"].max()
)

latest = (
    df[
        df["month"]
        == latest_month
    ]
    [
        [
            "technology",
            "development_score",
            "developer_interest_score",
            "model_ecosystem_score",
            "ai_evolution_score",
            "evolution_momentum",
        ]
    ]
    .sort_values(
        "ai_evolution_score",
        ascending=False
    )
)

print(
    f"\nMonth: "
    f"{latest_month.strftime('%Y-%m')}"
)

print(
    latest.to_string(
        index=False
    )
)


# ============================================================
# 7. AVERAGE TECHNOLOGY RANKING
# ============================================================

print("\n" + "-" * 70)
print("7. LONG-TERM AVERAGE RANKING")
print("-" * 70)

average_scores = (
    df.groupby(
        "technology"
    )[
        "ai_evolution_score"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

print(
    average_scores.to_string()
)


# ============================================================
# 8. INDEX VOLATILITY
# ============================================================

print("\n" + "-" * 70)
print("8. INDEX VOLATILITY")
print("-" * 70)

volatility = (
    df.groupby(
        "technology"
    )[
        "ai_evolution_score"
    ]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max",
        ]
    )
    .sort_values(
        "std",
        ascending=False
    )
)

print(
    volatility.to_string()
)


# ============================================================
# 9. SOURCE CORRELATION WITH FINAL INDEX
# ============================================================

print("\n" + "-" * 70)
print("9. SOURCE / INDEX CORRELATION")
print("-" * 70)

correlation_columns = [
    "development_score",
    "developer_interest_score",
    "model_ecosystem_score",
    "ai_evolution_score",
]

correlations = (
    df[
        correlation_columns
    ]
    .corr()
    .round(3)
)

print(
    correlations.to_string()
)


# ============================================================
# 10. RANK STABILITY
# ============================================================

print("\n" + "-" * 70)
print("10. RANK STABILITY")
print("-" * 70)

df["rank"] = (
    df.groupby(
        "month"
    )[
        "ai_evolution_score"
    ]
    .rank(
        ascending=False,
        method="average"
    )
)

rank_summary = (
    df.groupby(
        "technology"
    )[
        "rank"
    ]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max",
        ]
    )
    .sort_values(
        "mean"
    )
)

print(
    rank_summary.to_string()
)


# ============================================================
# 11. MOMENTUM SUMMARY
# ============================================================

print("\n" + "-" * 70)
print("11. MOMENTUM SUMMARY")
print("-" * 70)

momentum_summary = (
    df.groupby(
        "technology"
    )[
        "evolution_momentum"
    ]
    .agg(
        [
            "mean",
            "std",
            "min",
            "max",
        ]
    )
)

print(
    momentum_summary.to_string()
)


# ============================================================
# 12. SENSITIVITY TEST
# ============================================================

print("\n" + "-" * 70)
print("12. WEIGHT SENSITIVITY TEST")
print("-" * 70)

#
# Test alternative source weights.
#
# Baseline:
#   GitHub       1/3
#   StackOverflow 1/3
#   HuggingFace   1/3
#
# Alternative:
#   GitHub       0.40
#   StackOverflow 0.30
#   HuggingFace  0.30
#
# Another:
#   GitHub       0.30
#   StackOverflow 0.40
#   HuggingFace  0.30
#

def weighted_score(
    row,
    github_weight,
    so_weight,
    hf_weight,
):

    if row[
        "huggingface_available"
    ] == 1:

        return (
            row[
                "development_score"
            ]
            * github_weight
            +
            row[
                "developer_interest_score"
            ]
            * so_weight
            +
            row[
                "model_ecosystem_score"
            ]
            * hf_weight
        )

    # Pre-HF period
    total_weight = (
        github_weight
        + so_weight
    )

    return (
        row[
            "development_score"
        ]
        * github_weight
        +
        row[
            "developer_interest_score"
        ]
        * so_weight
    ) / total_weight


df[
    "score_github40"
] = df.apply(
    lambda row:
    weighted_score(
        row,
        0.40,
        0.30,
        0.30
    ),
    axis=1
)

df[
    "score_so40"
] = df.apply(
    lambda row:
    weighted_score(
        row,
        0.30,
        0.40,
        0.30
    ),
    axis=1
)


# ============================================================
# RANK CORRELATION
# ============================================================

baseline_ranks = (
    df[
        "ai_evolution_score"
    ].rank()
)

github40_ranks = (
    df[
        "score_github40"
    ].rank()
)

so40_ranks = (
    df[
        "score_so40"
    ].rank()
)

baseline_github40 = (
    baseline_ranks.corr(
        github40_ranks
    )
)

baseline_so40 = (
    baseline_ranks.corr(
        so40_ranks
    )
)

print(
    f"\nBaseline vs GitHub 40% "
    f"rank correlation: "
    f"{baseline_github40:.4f}"
)

print(
    f"Baseline vs Stack Overflow 40% "
    f"rank correlation: "
    f"{baseline_so40:.4f}"
)


# ============================================================
# 13. SAVE VALIDATION DATA
# ============================================================

validation_columns = [
    "month",
    "technology",

    "development_score",
    "developer_interest_score",
    "model_ecosystem_score",

    "ai_evolution_score",

    "evolution_change",
    "evolution_growth",
    "evolution_momentum",

    "rank",

    "score_github40",
    "score_so40",
]

validation = df[
    validation_columns
].copy()

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

validation.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n" + "=" * 70)
print("INDEX VALIDATION COMPLETE")
print("=" * 70)

print(
    f"\nValidation output:"
)

print(
    OUTPUT_FILE
)

print(
    "\nThe index is ready for deeper analysis if:"
)

print(
    "1. Source contributions are balanced."
)

print(
    "2. Rankings remain reasonably stable under"
    " alternative weights."
)

print(
    "3. No source dominates unexpectedly."
)

print(
    "4. Temporal behaviour is interpretable."
)

print(
    "\n" + "=" * 70
)