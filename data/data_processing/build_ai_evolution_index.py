from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# AI EVOLUTION INTELLIGENCE
# AI EVOLUTION INDEX V1
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_features.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_evolution_index.csv"
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
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION INTELLIGENCE")
print("AI EVOLUTION INDEX V1")
print("=" * 70)

print("\nLoading:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

df["month"] = pd.to_datetime(df["month"])

df = df.sort_values(
    ["month", "technology"]
).reset_index(drop=True)

print(f"\nRows: {len(df)}")
print(f"Technologies: {df['technology'].nunique()}")


# ============================================================
# LOG-TRANSFORMED SOURCE SIGNALS
#
# We use log1p because several variables are heavily
# right-skewed.
# ============================================================

github_metrics = [
    "github_activity",
    "github_stars",
    "github_forks",
    "github_issues",
]

stackoverflow_metrics = [
    "stackoverflow_questions",
    "stackoverflow_views",
    "stackoverflow_answers",
    "stackoverflow_score",
]


# ============================================================
# SAFE LOG TRANSFORMATION
# ============================================================

def safe_log(series):
    """
    Log transform that safely handles zero and negative values.

    For normal non-negative metrics:
        log(1 + x)

    For Stack Overflow score, negative values exist.
    We shift the complete series before applying log1p.
    """

    minimum = series.min()

    if minimum < 0:

        shifted = series - minimum

        return np.log1p(
            shifted
        )

    return np.log1p(
        series.clip(lower=0)
    )


# ============================================================
# ROBUST MIN-MAX NORMALIZATION
# ============================================================

def robust_normalize(series):
    """
    Normalize a series using the 5th and 95th percentiles.

    This reduces the influence of extreme outliers while
    keeping the resulting signal between 0 and 1.
    """

    valid = series.dropna()

    if len(valid) == 0:
        return pd.Series(
            np.nan,
            index=series.index
        )

    lower = valid.quantile(0.05)
    upper = valid.quantile(0.95)

    if upper <= lower:

        return pd.Series(
            0.5,
            index=series.index
        )

    result = (
        (series - lower)
        / (upper - lower)
    )

    return result.clip(
        lower=0,
        upper=1
    )


# ============================================================
# PREPARE LOG SIGNALS
# ============================================================

for column in github_metrics:

    df[
        f"{column}_index"
    ] = robust_normalize(
        safe_log(
            df[column]
        )
    )


for column in stackoverflow_metrics:

    df[
        f"{column}_index"
    ] = robust_normalize(
        safe_log(
            df[column]
        )
    )


# ============================================================
# HUGGING FACE
# ============================================================

#
# HF is only available from July 2024.
#
# We keep pre-HF months as NaN rather than treating them as
# zero.
#

df[
    "huggingface_models_index"
] = robust_normalize(
    safe_log(
        df[
            "huggingface_models"
        ]
    )
)


# ============================================================
# SOURCE-LEVEL INDICES
# ============================================================

print("\nBuilding source-level indices...")


# ------------------------------------------------------------
# GitHub Development Activity
# ------------------------------------------------------------

github_index_columns = [
    f"{column}_index"
    for column in github_metrics
]

df[
    "development_index"
] = (
    df[
        github_index_columns
    ]
    .mean(
        axis=1,
        skipna=True
    )
)


# ------------------------------------------------------------
# Stack Overflow Developer Interest
# ------------------------------------------------------------

stackoverflow_index_columns = [
    f"{column}_index"
    for column in stackoverflow_metrics
]

df[
    "developer_interest_index"
] = (
    df[
        stackoverflow_index_columns
    ]
    .mean(
        axis=1,
        skipna=True
    )
)


# ------------------------------------------------------------
# Hugging Face Model Ecosystem
# ------------------------------------------------------------

df[
    "model_ecosystem_index"
] = (
    df[
        "huggingface_models_index"
    ]
)


# ============================================================
# AI EVOLUTION INDEX
# ============================================================

#
# Equal source-level weighting:
#
#   Development Activity     = 1/3
#   Developer Interest       = 1/3
#   Model Ecosystem          = 1/3
#
# However, HF was not historically available.
#
# Therefore:
#
# Before July 2024:
#     AI Evolution Index is based on the two available
#     sources and is explicitly marked as pre-HF.
#
# From July 2024:
#     All three sources receive equal weight.
#

df[
    "ai_evolution_index"
] = np.nan

pre_hf = (
    df[
        "huggingface_available"
    ] == 0
)

post_hf = (
    df[
        "huggingface_available"
    ] == 1
)


# ------------------------------------------------------------
# Pre-HF period
# ------------------------------------------------------------

df.loc[
    pre_hf,
    "ai_evolution_index"
] = (
    (
        df.loc[
            pre_hf,
            "development_index"
        ]
        +
        df.loc[
            pre_hf,
            "developer_interest_index"
        ]
    )
    / 2
)


# ------------------------------------------------------------
# HF-covered period
# ------------------------------------------------------------

df.loc[
    post_hf,
    "ai_evolution_index"
] = (
    (
        df.loc[
            post_hf,
            "development_index"
        ]
        +
        df.loc[
            post_hf,
            "developer_interest_index"
        ]
        +
        df.loc[
            post_hf,
            "model_ecosystem_index"
        ]
    )
    / 3
)


# ============================================================
# SCALE INDEX TO 0–100
# ============================================================

df[
    "ai_evolution_score"
] = (
    df[
        "ai_evolution_index"
    ]
    * 100
)


df[
    "development_score"
] = (
    df[
        "development_index"
    ]
    * 100
)


df[
    "developer_interest_score"
] = (
    df[
        "developer_interest_index"
    ]
    * 100
)


df[
    "model_ecosystem_score"
] = (
    df[
        "model_ecosystem_index"
    ]
    * 100
)


# ============================================================
# MONTH-OVER-MONTH EVOLUTION
# ============================================================

df[
    "evolution_change"
] = (
    df
    .groupby("technology")[
        "ai_evolution_score"
    ]
    .diff()
)


df[
    "evolution_growth"
] = (
    df
    .groupby("technology")[
        "ai_evolution_score"
    ]
    .pct_change()
)


# ============================================================
# 3-MONTH ROLLING EVOLUTION
# ============================================================

df[
    "evolution_rolling_3m"
] = (
    df
    .groupby("technology")[
        "ai_evolution_score"
    ]
    .transform(
        lambda x:
        x.rolling(
            window=3,
            min_periods=2
        ).mean()
    )
)


# ============================================================
# MOMENTUM
# ============================================================

df[
    "evolution_momentum"
] = (
    df
    .groupby("technology")[
        "ai_evolution_score"
    ]
    .transform(
        lambda x:
        x.diff(3)
    )
)


# ============================================================
# CURRENT RELATIVE RANK
# ============================================================

df[
    "monthly_rank"
] = (
    df
    .groupby("month")[
        "ai_evolution_score"
    ]
    .rank(
        ascending=False,
        method="min"
    )
)


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

output_columns = [
    "month",
    "technology",

    # Original source availability
    "github_available",
    "stackoverflow_available",
    "huggingface_available",

    # Source indices
    "development_index",
    "developer_interest_index",
    "model_ecosystem_index",

    # 0–100 scores
    "development_score",
    "developer_interest_score",
    "model_ecosystem_score",

    # Final index
    "ai_evolution_index",
    "ai_evolution_score",

    # Temporal features
    "evolution_change",
    "evolution_growth",
    "evolution_rolling_3m",
    "evolution_momentum",

    # Ranking
    "monthly_rank",
]


result = df[
    output_columns
].copy()


# ============================================================
# SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

result.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("AI EVOLUTION INDEX CREATED")
print("=" * 70)

print(
    f"\nOutput: {OUTPUT_FILE}"
)

print(
    f"Rows: {len(result)}"
)

print(
    f"Columns: {len(result.columns)}"
)

print("\nTechnology counts:")

print(
    result[
        "technology"
    ]
    .value_counts()
    .sort_index()
)


print("\nDate range:")

print(
    result["month"].min().strftime("%Y-%m"),
    "→",
    result["month"].max().strftime("%Y-%m")
)


# ============================================================
# SCORE RANGE
# ============================================================

print("\nAI Evolution Score range:")

print(
    result[
        "ai_evolution_score"
    ].describe().to_string()
)


# ============================================================
# LATEST TECHNOLOGY RANKING
# ============================================================

latest_month = (
    result["month"].max()
)

latest = (
    result[
        result["month"]
        == latest_month
    ]
    [
        [
            "technology",
            "ai_evolution_score",
            "development_score",
            "developer_interest_score",
            "model_ecosystem_score",
            "evolution_momentum",
            "monthly_rank",
        ]
    ]
    .sort_values(
        "monthly_rank"
    )
)


print(
    f"\nLatest month: "
    f"{latest_month.strftime('%Y-%m')}"
)

print(
    latest.to_string(
        index=False
    )
)


# ============================================================
# TOP TECHNOLOGY OVERALL
# ============================================================

overall = (
    result
    .groupby("technology")[
        "ai_evolution_score"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

print(
    "\nAverage AI Evolution Score:"
)

print(
    overall.to_string()
)


# ============================================================
# FINAL STRUCTURAL CHECKS
# ============================================================

expected_rows = (
    44
    * len(TECHNOLOGIES)
)

assert len(result) == expected_rows

assert (
    set(
        result[
            "technology"
        ].unique()
    )
    == set(
        TECHNOLOGIES
    )
)

assert (
    result[
        "month"
    ].nunique()
    == 44
)

print("\n" + "=" * 70)
print("VALIDATION PASSED")
print("=" * 70)