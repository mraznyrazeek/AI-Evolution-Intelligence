from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_signals.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_features.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION INTELLIGENCE")
print("FEATURE ENGINEERING")
print("=" * 70)

print("\nLoading unified dataset:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

print(f"\nRows: {len(df)}")
print(f"Columns: {len(df.columns)}")


# ============================================================
# BASIC PREPARATION
# ============================================================

df["month"] = pd.to_datetime(
    df["month"]
)

df = df.sort_values(
    ["technology", "month"]
).reset_index(
    drop=True
)


# ============================================================
# 1. TOTAL ACTIVITY
# ============================================================

df["github_total_activity"] = (
    df["github_activity"]
)

df["stackoverflow_activity"] = (
    df["stackoverflow_questions"]
)


# ============================================================
# 2. NORMALIZED SIGNALS
# ============================================================

# GitHub
github_columns = [
    "github_activity",
    "github_stars",
    "github_forks",
    "github_issues",
]

for column in github_columns:

    df[f"{column}_log"] = np.log1p(
        df[column].clip(lower=0)
    )


# Stack Overflow
stackoverflow_columns = [
    "stackoverflow_questions",
    "stackoverflow_views",
    "stackoverflow_answers",
]

for column in stackoverflow_columns:

    df[f"{column}_log"] = np.log1p(
        df[column].clip(lower=0)
    )


# Hugging Face
#
# NaN before July 2024 means unavailable,
# so we preserve NaN here.

df["huggingface_models_log"] = np.log1p(
    df["huggingface_models"]
)


# ============================================================
# 3. MONTH-OVER-MONTH GROWTH
# ============================================================

growth_columns = [
    "github_activity",
    "github_stars",
    "github_forks",
    "github_issues",
    "stackoverflow_questions",
    "stackoverflow_views",
    "stackoverflow_answers",
    "huggingface_models",
]

for column in growth_columns:

    df[f"{column}_growth"] = (
        df
        .groupby("technology")[column]
        .pct_change()
    )


# ============================================================
# 4. ROLLING TRENDS
# ============================================================

rolling_columns = [
    "github_activity",
    "github_stars",
    "stackoverflow_questions",
    "stackoverflow_views",
    "huggingface_models",
]

for column in rolling_columns:

    df[f"{column}_rolling_3m"] = (
        df
        .groupby("technology")[column]
        .transform(
            lambda x:
            x.rolling(
                window=3,
                min_periods=2
            ).mean()
        )
    )


# ============================================================
# 5. TECHNOLOGY SHARE
# ============================================================

share_columns = [
    "github_activity",
    "github_stars",
    "stackoverflow_questions",
    "stackoverflow_views",
]

for column in share_columns:

    total_by_month = (
        df.groupby("month")[column]
        .transform("sum")
    )

    df[f"{column}_share"] = np.where(
        total_by_month > 0,
        df[column] / total_by_month,
        0
    )


# ============================================================
# 6. HUGGING FACE SHARE
# ============================================================

hf_total = (
    df.groupby("month")[
        "huggingface_models"
    ].transform("sum")
)

df["huggingface_share"] = np.where(
    (
        df["huggingface_available"] == 1
    ) & (
        hf_total > 0
    ),
    df["huggingface_models"] / hf_total,
    np.nan
)


# ============================================================
# 7. TIME FEATURES
# ============================================================

df["year"] = (
    df["month"].dt.year
)

df["month_number"] = (
    df["month"].dt.month
)

# Cyclical month representation

df["month_sin"] = np.sin(
    2 * np.pi *
    df["month_number"] / 12
)

df["month_cos"] = np.cos(
    2 * np.pi *
    df["month_number"] / 12
)


# ============================================================
# 8. DATA SOURCE COVERAGE
# ============================================================

df["github_available"] = (
    (
        df[
            "github_activity"
        ] > 0
    )
    .astype(int)
)

df["stackoverflow_available"] = (
    (
        df[
            "stackoverflow_questions"
        ] > 0
    )
    .astype(int)
)


# ============================================================
# 9. COMBINED ACTIVITY SIGNAL
# ============================================================

# We deliberately keep this simple at this stage.
#
# The final AI Evolution Index will be constructed
# separately after examining the distributions.

df["community_activity"] = (
    df["github_activity"]
    + df["stackoverflow_questions"]
)


# ============================================================
# 10. SAVE
# ============================================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("FEATURE ENGINEERING COMPLETE")
print("=" * 70)

print(
    f"\nOutput: {OUTPUT_FILE}"
)

print(
    f"Rows: {len(df)}"
)

print(
    f"Columns: {len(df.columns)}"
)

print("\nTechnologies:")

print(
    df["technology"]
    .value_counts()
    .sort_index()
)

print("\nDate range:")

print(
    df["month"].min().strftime("%Y-%m"),
    "→",
    df["month"].max().strftime("%Y-%m")
)

print("\nMissing values:")

missing = (
    df.isna()
    .sum()
)

print(
    missing[
        missing > 0
    ]
)

print("\nSample:")

print(
    df.head(12).to_string(
        index=False
    )
)

print("\n" + "=" * 70)
print("PROCESSING COMPLETE")
print("=" * 70)