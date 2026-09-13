from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# AI EVOLUTION INTELLIGENCE
# AI EVOLUTION INDEX ROBUSTNESS ANALYSIS
# Leave-One-Source-Out Analysis
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_features.csv"
)

INDEX_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_evolution_index.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analysis"
    / "robustness"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

TECHNOLOGY_COLUMN = "technology"
MONTH_COLUMN = "month"

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

HF_METRICS = [
    "huggingface_models",
]


# ============================================================
# HELPERS
# ============================================================

def safe_log(series):
    """
    Apply log1p safely.

    For non-negative values:
        log1p(x)

    For series containing negative values:
        shift by the minimum value first.
    """

    series = pd.to_numeric(series, errors="coerce")

    minimum = series.min(skipna=True)

    if pd.isna(minimum):
        return pd.Series(np.nan, index=series.index)

    if minimum < 0:
        return np.log1p(series - minimum)

    return np.log1p(series)


def robust_normalize(series):
    """
    Robust normalization using the 5th and 95th percentiles.
    """

    series = pd.to_numeric(series, errors="coerce")

    valid = series.dropna()

    if valid.empty:
        return pd.Series(np.nan, index=series.index)

    lower = valid.quantile(0.05)
    upper = valid.quantile(0.95)

    if upper <= lower:
        return pd.Series(0.5, index=series.index)

    normalized = (series - lower) / (upper - lower)

    return normalized.clip(0, 1)


def build_normalized_metric(df, metric):
    """
    Log-transform and robust-normalize a metric.
    """

    transformed = safe_log(df[metric])

    return robust_normalize(transformed)


def calculate_source_index(df, metrics):
    """
    Calculate the mean normalized score across a source's metrics.
    """

    normalized_columns = []

    for metric in metrics:

        normalized_column = f"_norm_{metric}"

        df[normalized_column] = build_normalized_metric(
            df,
            metric,
        )

        normalized_columns.append(normalized_column)

    return df[normalized_columns].mean(axis=1)


def rank_series(df, score_column):
    """
    Rank technologies within each month.
    Rank 1 = highest score.
    """

    return (
        df.groupby(MONTH_COLUMN)[score_column]
        .rank(
            ascending=False,
            method="min",
        )
    )


def spearman_correlation(x, y):
    """
    Calculate Spearman rank correlation without scipy.
    """

    x = pd.Series(x)
    y = pd.Series(y)

    valid = x.notna() & y.notna()

    if valid.sum() < 2:
        return np.nan

    return x[valid].rank().corr(
        y[valid].rank(),
        method="pearson",
    )


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION INDEX ROBUSTNESS ANALYSIS")
print("=" * 70)

print("\nLoading datasets...")

features = pd.read_csv(INPUT_FILE)
baseline = pd.read_csv(INDEX_FILE)

print(f"Features: {features.shape[0]} rows × {features.shape[1]} columns")
print(f"Baseline index: {baseline.shape[0]} rows × {baseline.shape[1]} columns")


# ============================================================
# PREPARE DATA
# ============================================================

required_columns = [
    MONTH_COLUMN,
    TECHNOLOGY_COLUMN,
    *GITHUB_METRICS,
    *STACKOVERFLOW_METRICS,
    *HF_METRICS,
]

missing_columns = [
    column
    for column in required_columns
    if column not in features.columns
]

if missing_columns:
    raise ValueError(
        "Missing required columns:\n"
        + "\n".join(missing_columns)
    )


df = features[
    required_columns
].copy()


# Convert numeric columns

numeric_columns = [
    *GITHUB_METRICS,
    *STACKOVERFLOW_METRICS,
    *HF_METRICS,
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )


# ============================================================
# BUILD SOURCE INDICES
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
    HF_METRICS,
)


# ============================================================
# BASELINE SOURCE AVAILABILITY
# ============================================================

github_available = (
    df[GITHUB_METRICS]
    .notna()
    .any(axis=1)
)

stackoverflow_available = (
    df[STACKOVERFLOW_METRICS]
    .notna()
    .any(axis=1)
)

hf_available = (
    df[HF_METRICS]
    .notna()
    .any(axis=1)
)


# ============================================================
# BUILD ALTERNATIVE INDICES
# ============================================================

print("\nBuilding leave-one-source-out indices...")


# ------------------------------------------------------------
# 1. BASELINE
# ------------------------------------------------------------

baseline_calc = pd.DataFrame()

baseline_calc[MONTH_COLUMN] = df[MONTH_COLUMN]
baseline_calc[TECHNOLOGY_COLUMN] = df[TECHNOLOGY_COLUMN]

baseline_calc["github"] = df["development_index"]
baseline_calc["stackoverflow"] = df["developer_interest_index"]
baseline_calc["huggingface"] = df["model_ecosystem_index"]

source_values = pd.concat(
    [
        df["development_index"],
        df["developer_interest_index"],
        df["model_ecosystem_index"],
    ],
    axis=1,
)

baseline_calc["baseline_score"] = (
    source_values.mean(axis=1)
    * 100
)


# ------------------------------------------------------------
# 2. REMOVE GITHUB
# ------------------------------------------------------------

print("  • Removing GitHub source...")

github_removed = pd.DataFrame()

github_removed[MONTH_COLUMN] = df[MONTH_COLUMN]
github_removed[TECHNOLOGY_COLUMN] = df[TECHNOLOGY_COLUMN]

github_removed["alternative_score"] = (
    pd.concat(
        [
            df["developer_interest_index"],
            df["model_ecosystem_index"],
        ],
        axis=1,
    )
    .mean(axis=1)
    * 100
)

github_removed["scenario"] = "without_github"


# ------------------------------------------------------------
# 3. REMOVE STACK OVERFLOW
# ------------------------------------------------------------

print("  • Removing Stack Overflow source...")

stackoverflow_removed = pd.DataFrame()

stackoverflow_removed[MONTH_COLUMN] = df[MONTH_COLUMN]
stackoverflow_removed[TECHNOLOGY_COLUMN] = df[TECHNOLOGY_COLUMN]

stackoverflow_removed["alternative_score"] = (
    pd.concat(
        [
            df["development_index"],
            df["model_ecosystem_index"],
        ],
        axis=1,
    )
    .mean(axis=1)
    * 100
)

stackoverflow_removed["scenario"] = "without_stackoverflow"


# ------------------------------------------------------------
# 4. REMOVE HUGGING FACE
# ------------------------------------------------------------

print("  • Removing Hugging Face source...")

hf_removed = pd.DataFrame()

hf_removed[MONTH_COLUMN] = df[MONTH_COLUMN]
hf_removed[TECHNOLOGY_COLUMN] = df[TECHNOLOGY_COLUMN]

hf_removed["alternative_score"] = (
    pd.concat(
        [
            df["development_index"],
            df["developer_interest_index"],
        ],
        axis=1,
    )
    .mean(axis=1)
    * 100
)

hf_removed["scenario"] = "without_huggingface"


# ============================================================
# MERGE WITH BASELINE INDEX
# ============================================================

baseline_scores = baseline[
    [
        MONTH_COLUMN,
        TECHNOLOGY_COLUMN,
        "ai_evolution_score",
    ]
].copy()

baseline_scores = baseline_scores.rename(
    columns={
        "ai_evolution_score": "baseline_score_file",
    }
)


def merge_scenario(scenario_df):

    merged = scenario_df.merge(
        baseline_scores,
        on=[
            MONTH_COLUMN,
            TECHNOLOGY_COLUMN,
        ],
        how="left",
    )

    merged["score_difference"] = (
        merged["alternative_score"]
        - merged["baseline_score_file"]
    )

    merged["absolute_score_difference"] = (
        merged["score_difference"].abs()
    )

    merged["baseline_rank"] = rank_series(
        merged,
        "baseline_score_file",
    )

    merged["alternative_rank"] = rank_series(
        merged,
        "alternative_score",
    )

    merged["rank_change"] = (
        merged["alternative_rank"]
        - merged["baseline_rank"]
    )

    merged["absolute_rank_change"] = (
        merged["rank_change"].abs()
    )

    return merged


scenarios = [
    merge_scenario(github_removed),
    merge_scenario(stackoverflow_removed),
    merge_scenario(hf_removed),
]

robustness_detail = pd.concat(
    scenarios,
    ignore_index=True,
)


# ============================================================
# SCENARIO SUMMARY
# ============================================================

print("\nCalculating scenario summaries...")

scenario_summary = []

for scenario, group in robustness_detail.groupby("scenario"):

    scenario_summary.append(
        {
            "scenario": scenario,

            "rows": len(group),

            "mean_absolute_score_difference": (
                group["absolute_score_difference"]
                .mean()
            ),

            "max_absolute_score_difference": (
                group["absolute_score_difference"]
                .max()
            ),

            "mean_absolute_rank_change": (
                group["absolute_rank_change"]
                .mean()
            ),

            "max_absolute_rank_change": (
                group["absolute_rank_change"]
                .max()
            ),

            "rank_correlation": (
                spearman_correlation(
                    group["baseline_score_file"],
                    group["alternative_score"],
                )
            ),

            "exact_rank_match_rate": (
                group["rank_change"].eq(0).mean()
            ),
        }
    )


scenario_summary = pd.DataFrame(
    scenario_summary
)


# ============================================================
# TECHNOLOGY-LEVEL ROBUSTNESS
# ============================================================

technology_summary = (
    robustness_detail
    .groupby(
        [
            "scenario",
            TECHNOLOGY_COLUMN,
        ]
    )
    .agg(
        mean_absolute_score_difference=(
            "absolute_score_difference",
            "mean",
        ),

        max_absolute_score_difference=(
            "absolute_score_difference",
            "max",
        ),

        mean_absolute_rank_change=(
            "absolute_rank_change",
            "mean",
        ),

        max_absolute_rank_change=(
            "absolute_rank_change",
            "max",
        ),

        exact_rank_match_rate=(
            "rank_change",
            lambda x: (x == 0).mean(),
        ),
    )
    .reset_index()
)


# ============================================================
# LATEST-MONTH ROBUSTNESS
# ============================================================

latest_month = df[MONTH_COLUMN].max()

latest = robustness_detail[
    robustness_detail[MONTH_COLUMN] == latest_month
].copy()


latest_comparison = latest[
    [
        MONTH_COLUMN,
        TECHNOLOGY_COLUMN,
        "scenario",
        "baseline_score_file",
        "alternative_score",
        "score_difference",
        "baseline_rank",
        "alternative_rank",
        "rank_change",
    ]
].sort_values(
    [
        "scenario",
        "alternative_rank",
    ]
)


# ============================================================
# TECHNOLOGY RANK STABILITY
# ============================================================

rank_stability = (
    robustness_detail
    .groupby(
        [
            "scenario",
            TECHNOLOGY_COLUMN,
        ]
    )
    .agg(
        average_baseline_rank=(
            "baseline_rank",
            "mean",
        ),

        average_alternative_rank=(
            "alternative_rank",
            "mean",
        ),

        average_rank_change=(
            "rank_change",
            "mean",
        ),

        mean_absolute_rank_change=(
            "absolute_rank_change",
            "mean",
        ),

        maximum_rank_change=(
            "absolute_rank_change",
            "max",
        ),
    )
    .reset_index()
)


# ============================================================
# SAVE RESULTS
# ============================================================

detail_file = (
    OUTPUT_DIR
    / "leave_one_source_out_detail.csv"
)

summary_file = (
    OUTPUT_DIR
    / "leave_one_source_out_summary.csv"
)

technology_file = (
    OUTPUT_DIR
    / "leave_one_source_out_technology_summary.csv"
)

latest_file = (
    OUTPUT_DIR
    / "leave_one_source_out_latest_comparison.csv"
)

rank_file = (
    OUTPUT_DIR
    / "leave_one_source_out_rank_stability.csv"
)


robustness_detail.to_csv(
    detail_file,
    index=False,
)

scenario_summary.to_csv(
    summary_file,
    index=False,
)

technology_summary.to_csv(
    technology_file,
    index=False,
)

latest_comparison.to_csv(
    latest_file,
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
print("ROBUSTNESS ANALYSIS RESULTS")
print("=" * 70)

print("\nScenario summary:")
print(
    scenario_summary.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)

print("\nLatest-month comparison:")
print(
    latest_comparison.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)

print("\nTechnology-level robustness:")
print(
    technology_summary.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


print("\nFiles created:")

for file in [
    detail_file,
    summary_file,
    technology_file,
    latest_file,
    rank_file,
]:

    print(f"  ✓ {file}")


print("\n" + "=" * 70)
print("ROBUSTNESS ANALYSIS COMPLETE")
print("=" * 70)