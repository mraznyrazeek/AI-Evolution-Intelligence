"""
Source Weight Sensitivity Analysis
==================================

Tests how sensitive the AI Evolution Index is to different
weights assigned to GitHub, Stack Overflow, and Hugging Face.

V1 baseline:
    GitHub         = 1/3
    Stack Overflow = 1/3
    Hugging Face   = 1/3

For months without Hugging Face coverage, the available
GitHub + Stack Overflow weights are proportionally renormalized.

This script DOES NOT modify the existing V1 index.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_features.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analysis"
    / "source_weight_sensitivity"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

TECHNOLOGY_COL = "technology"
MONTH_COL = "month"


GITHUB_METRICS = [
    "github_activity",
    "github_stars",
    "github_forks",
    "github_issues",
]

STACKOVERFLOW_METRICS = [
    "stackoverflow_questions",
    "stackoverflow_views",
    "stackoverflow_answers",
    "stackoverflow_score",
]

HUGGINGFACE_METRICS = [
    "huggingface_models",
]


WEIGHT_CONFIGURATIONS = {
    "baseline": {
        "github": 1 / 3,
        "stackoverflow": 1 / 3,
        "huggingface": 1 / 3,
    },

    "github_40": {
        "github": 0.40,
        "stackoverflow": 0.30,
        "huggingface": 0.30,
    },

    "stackoverflow_40": {
        "github": 0.30,
        "stackoverflow": 0.40,
        "huggingface": 0.30,
    },

    "huggingface_40": {
        "github": 0.30,
        "stackoverflow": 0.30,
        "huggingface": 0.40,
    },

    "github_50": {
        "github": 0.50,
        "stackoverflow": 0.25,
        "huggingface": 0.25,
    },

    "stackoverflow_50": {
        "github": 0.25,
        "stackoverflow": 0.50,
        "huggingface": 0.25,
    },

    "huggingface_50": {
        "github": 0.25,
        "stackoverflow": 0.25,
        "huggingface": 0.50,
    },
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def safe_log(series):
    """
    Apply log1p safely.

    For non-negative values:
        log1p(x)

    For negative values:
        shift the complete series so the minimum becomes zero,
        then apply log1p.
    """

    values = pd.to_numeric(series, errors="coerce").astype(float)

    valid = values.dropna()

    if valid.empty:
        return pd.Series(np.nan, index=series.index)

    minimum = valid.min()

    if minimum < 0:
        values = values - minimum

    values = values.clip(lower=0)

    return np.log1p(values)


def robust_normalize(series):
    """
    Robust normalization using the 5th and 95th percentiles.

    Values are clipped to [0, 1].
    """

    values = pd.to_numeric(series, errors="coerce").astype(float)

    valid = values.dropna()

    if valid.empty:
        return pd.Series(np.nan, index=series.index)

    lower = valid.quantile(0.05)
    upper = valid.quantile(0.95)

    if upper <= lower:
        result = pd.Series(0.5, index=series.index, dtype=float)
        result[values.isna()] = np.nan
        return result

    result = (values - lower) / (upper - lower)

    return result.clip(0, 1)


def calculate_source_index(df, metrics):
    """
    Calculate a source-level index as the mean of the
    normalized transformed metrics.
    """

    normalized_columns = []

    for metric in metrics:

        if metric not in df.columns:
            continue

        transformed = safe_log(df[metric])
        normalized = robust_normalize(transformed)

        column_name = f"_norm_{metric}"
        df[column_name] = normalized

        normalized_columns.append(column_name)

    if not normalized_columns:
        return pd.Series(np.nan, index=df.index)

    return df[normalized_columns].mean(axis=1)


def calculate_monthly_rank(series):
    """
    Rank technologies within each month.

    Rank 1 = highest score.
    """

    return (
        series.groupby(df[MONTH_COL])
        .rank(method="min", ascending=False)
    )


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("SOURCE WEIGHT SENSITIVITY ANALYSIS")
print("=" * 70)

print("\nLoading:")
print(INPUT_FILE)

df = pd.read_csv(INPUT_FILE)

df[MONTH_COL] = pd.to_datetime(df[MONTH_COL])

print(f"\nRows: {len(df):,}")
print(f"Technologies: {df[TECHNOLOGY_COL].nunique()}")
print(f"Months: {df[MONTH_COL].nunique()}")


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = (
    [TECHNOLOGY_COL, MONTH_COL]
    + GITHUB_METRICS
    + STACKOVERFLOW_METRICS
    + HUGGINGFACE_METRICS
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "Missing required columns:\n"
        + "\n".join(missing_columns)
    )


# ============================================================
# CALCULATE SOURCE INDICES
# ============================================================

print("\nCalculating source-level indices...")

df["development_index"] = calculate_source_index(
    df,
    GITHUB_METRICS,
)

df["developer_interest_index"] = calculate_source_index(
    df,
    STACKOVERFLOW_METRICS,
)

df["model_ecosystem_index"] = calculate_source_index(
    df,
    HUGGINGFACE_METRICS,
)


# ============================================================
# HUGGING FACE COVERAGE
# ============================================================

df["hf_available"] = (
    df["model_ecosystem_index"].notna()
)


# ============================================================
# CALCULATE WEIGHTED INDEX
# ============================================================

all_results = []


for configuration, weights in WEIGHT_CONFIGURATIONS.items():

    print(f"\nProcessing: {configuration}")

    temp = df[
        [
            MONTH_COL,
            TECHNOLOGY_COL,
            "development_index",
            "developer_interest_index",
            "model_ecosystem_index",
            "hf_available",
        ]
    ].copy()

    temp["configuration"] = configuration

    scores = []

    for _, row in temp.iterrows():

        github_score = row["development_index"]
        so_score = row["developer_interest_index"]
        hf_score = row["model_ecosystem_index"]

        github_weight = weights["github"]
        so_weight = weights["stackoverflow"]
        hf_weight = weights["huggingface"]

        # ----------------------------------------------------
        # Hugging Face available
        # ----------------------------------------------------

        if pd.notna(hf_score):

            weighted_score = (
                github_score * github_weight
                + so_score * so_weight
                + hf_score * hf_weight
            )

        # ----------------------------------------------------
        # Hugging Face unavailable
        #
        # Renormalize GitHub + Stack Overflow weights.
        # ----------------------------------------------------

        else:

            available_weight = (
                github_weight
                + so_weight
            )

            if available_weight > 0:

                github_weight_adjusted = (
                    github_weight / available_weight
                )

                so_weight_adjusted = (
                    so_weight / available_weight
                )

                weighted_score = (
                    github_score
                    * github_weight_adjusted
                    + so_score
                    * so_weight_adjusted
                )

            else:
                weighted_score = np.nan

        scores.append(weighted_score)

    temp["weighted_index"] = scores

    temp["score"] = (
        temp["weighted_index"] * 100
    )

    # Monthly rank
    temp["rank"] = (
        temp.groupby(MONTH_COL)["score"]
        .rank(
            method="min",
            ascending=False,
        )
    )

    all_results.append(temp)


results = pd.concat(
    all_results,
    ignore_index=True,
)


# ============================================================
# BASELINE
# ============================================================

baseline = results[
    results["configuration"] == "baseline"
][
    [
        MONTH_COL,
        TECHNOLOGY_COL,
        "score",
        "rank",
    ]
].copy()

baseline = baseline.rename(
    columns={
        "score": "baseline_score",
        "rank": "baseline_rank",
    }
)


# ============================================================
# COMPARE EACH CONFIGURATION AGAINST BASELINE
# ============================================================

comparison = results.merge(
    baseline,
    on=[
        MONTH_COL,
        TECHNOLOGY_COL,
    ],
    how="left",
)

comparison["score_difference"] = (
    comparison["score"]
    - comparison["baseline_score"]
)

comparison["abs_score_difference"] = (
    comparison["score_difference"].abs()
)

comparison["rank_change"] = (
    comparison["rank"]
    - comparison["baseline_rank"]
)

comparison["abs_rank_change"] = (
    comparison["rank_change"].abs()
)

comparison["exact_rank_match"] = (
    comparison["rank"]
    == comparison["baseline_rank"]
)


# ============================================================
# SUMMARY
# ============================================================

summary_rows = []


for configuration, group in comparison.groupby(
    "configuration"
):

    score_difference = (
        group["abs_score_difference"]
        .mean()
    )

    max_score_difference = (
        group["abs_score_difference"]
        .max()
    )

    mean_rank_change = (
        group["abs_rank_change"]
        .mean()
    )

    max_rank_change = (
        group["abs_rank_change"]
        .max()
    )

    exact_rank_match = (
        group["exact_rank_match"]
        .mean()
    )

    # Spearman correlation against V1
    valid = group[
        [
            "score",
            "baseline_score",
        ]
    ].dropna()

    if len(valid) >= 2:

        correlation = spearmanr(
            valid["score"],
            valid["baseline_score"],
        ).statistic

    else:
        correlation = np.nan

    weights = WEIGHT_CONFIGURATIONS[
        configuration
    ]

    summary_rows.append(
        {
            "configuration": configuration,
            "github_weight": weights["github"],
            "stackoverflow_weight": weights[
                "stackoverflow"
            ],
            "huggingface_weight": weights[
                "huggingface"
            ],
            "mean_abs_score_difference":
                score_difference,
            "max_abs_score_difference":
                max_score_difference,
            "mean_abs_rank_change":
                mean_rank_change,
            "max_abs_rank_change":
                max_rank_change,
            "rank_correlation":
                correlation,
            "exact_rank_match":
                exact_rank_match,
        }
    )


summary = pd.DataFrame(summary_rows)


# ============================================================
# LATEST MONTH COMPARISON
# ============================================================

latest_month = results[MONTH_COL].max()

latest = comparison[
    comparison[MONTH_COL] == latest_month
].copy()

latest = latest[
    [
        "configuration",
        MONTH_COL,
        TECHNOLOGY_COL,
        "score",
        "baseline_score",
        "score_difference",
        "rank",
        "baseline_rank",
        "rank_change",
    ]
].sort_values(
    [
        "configuration",
        "rank",
    ]
)


# ============================================================
# TECHNOLOGY-LEVEL SUMMARY
# ============================================================

technology_summary = (
    comparison
    .groupby(
        [
            "configuration",
            TECHNOLOGY_COL,
        ]
    )
    .agg(
        mean_abs_score_difference=(
            "abs_score_difference",
            "mean",
        ),
        max_abs_score_difference=(
            "abs_score_difference",
            "max",
        ),
        mean_abs_rank_change=(
            "abs_rank_change",
            "mean",
        ),
        max_abs_rank_change=(
            "abs_rank_change",
            "max",
        ),
        exact_rank_match=(
            "exact_rank_match",
            "mean",
        ),
    )
    .reset_index()
)


# ============================================================
# RANK STABILITY BY CONFIGURATION
# ============================================================

rank_stability_rows = []


for configuration, group in comparison.groupby(
    "configuration"
):

    for technology, tech_group in group.groupby(
        TECHNOLOGY_COL
    ):

        valid = tech_group[
            [
                "rank",
                "baseline_rank",
            ]
        ].dropna()

        if len(valid) >= 2:

            correlation = spearmanr(
                valid["rank"],
                valid["baseline_rank"],
            ).statistic

        else:
            correlation = np.nan

        rank_stability_rows.append(
            {
                "configuration": configuration,
                "technology": technology,
                "rank_correlation": correlation,
                "mean_abs_rank_change":
                    valid["rank"]
                    .sub(valid["baseline_rank"])
                    .abs()
                    .mean(),
                "exact_rank_match":
                    (
                        valid["rank"]
                        == valid["baseline_rank"]
                    ).mean(),
            }
        )


rank_stability = pd.DataFrame(
    rank_stability_rows
)


# ============================================================
# SAVE OUTPUTS
# ============================================================

detail_file = (
    OUTPUT_DIR
    / "source_weight_sensitivity_detail.csv"
)

summary_file = (
    OUTPUT_DIR
    / "source_weight_sensitivity_summary.csv"
)

latest_file = (
    OUTPUT_DIR
    / "source_weight_sensitivity_latest_comparison.csv"
)

technology_file = (
    OUTPUT_DIR
    / "source_weight_sensitivity_technology_summary.csv"
)

rank_file = (
    OUTPUT_DIR
    / "source_weight_sensitivity_rank_stability.csv"
)


comparison.to_csv(
    detail_file,
    index=False,
)

summary.to_csv(
    summary_file,
    index=False,
)

latest.to_csv(
    latest_file,
    index=False,
)

technology_summary.to_csv(
    technology_file,
    index=False,
)

rank_stability.to_csv(
    rank_file,
    index=False,
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("SOURCE WEIGHT SENSITIVITY SUMMARY")
print("=" * 70)

display_summary = summary.copy()

display_summary[
    "exact_rank_match"
] = (
    display_summary["exact_rank_match"] * 100
)

print(
    display_summary[
        [
            "configuration",
            "github_weight",
            "stackoverflow_weight",
            "huggingface_weight",
            "mean_abs_score_difference",
            "max_abs_score_difference",
            "mean_abs_rank_change",
            "max_abs_rank_change",
            "rank_correlation",
            "exact_rank_match",
        ]
    ].to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


print("\n" + "=" * 70)
print(
    f"LATEST MONTH: "
    f"{latest_month.strftime('%Y-%m')}"
)
print("=" * 70)


for configuration in WEIGHT_CONFIGURATIONS:

    print(f"\n{configuration.upper()}")

    latest_config = latest[
        latest["configuration"]
        == configuration
    ].sort_values("rank")

    print(
        latest_config[
            [
                TECHNOLOGY_COL,
                "score",
                "rank",
                "rank_change",
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


print("\n" + "=" * 70)
print("OUTPUT FILES")
print("=" * 70)

print(detail_file)
print(summary_file)
print(latest_file)
print(technology_file)
print(rank_file)

print("\nAnalysis complete.")