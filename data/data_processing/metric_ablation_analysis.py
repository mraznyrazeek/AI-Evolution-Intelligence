from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# INDIVIDUAL METRIC ABLATION ANALYSIS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_features.csv"
)

BASELINE_FILE = (
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
    / "metric_ablation"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# CONFIGURATION
# ============================================================

SOURCE_METRICS = {
    "github": [
        "github_activity",
        "github_stars",
        "github_forks",
        "github_issues",
    ],
    "stackoverflow": [
        "stackoverflow_questions",
        "stackoverflow_views",
        "stackoverflow_answers",
        "stackoverflow_score",
    ],
    "huggingface": [
        "huggingface_models",
    ],
}

ALL_METRICS = [
    metric
    for metrics in SOURCE_METRICS.values()
    for metric in metrics
]


# ============================================================
# FUNCTIONS
# ============================================================

def safe_log(series):
    """
    Apply log1p transformation.

    Positive/non-negative metrics:
        log1p(x)

    Metrics containing negative values:
        shift by the minimum valid value first.
    """
    series = pd.to_numeric(series, errors="coerce")

    valid = series.dropna()

    if valid.empty:
        return pd.Series(np.nan, index=series.index)

    minimum = valid.min()

    if minimum < 0:
        return np.log1p(series - minimum)

    return np.log1p(series)


def robust_normalize(series):
    """
    Robust percentile normalization using
    5th and 95th percentiles.

    Result is clipped to [0, 1].
    """
    series = pd.to_numeric(series, errors="coerce")

    valid = series.dropna()

    if valid.empty:
        return pd.Series(np.nan, index=series.index)

    lower = valid.quantile(0.05)
    upper = valid.quantile(0.95)

    if upper <= lower:
        return pd.Series(
            np.where(series.notna(), 0.5, np.nan),
            index=series.index,
        )

    normalized = (series - lower) / (upper - lower)

    return normalized.clip(0, 1)


def build_ablation_index(df, removed_metric=None):
    """
    Build an AI Evolution Index after removing one metric.

    If removed_metric is None:
        all metrics are used (baseline).

    Source-level weighting remains:

        GitHub      = 1/3
        StackOverflow = 1/3
        HuggingFace = 1/3

    when Hugging Face is available.

    Before Hugging Face coverage:
        GitHub      = 1/2
        StackOverflow = 1/2
    """

    result = df[["month", "technology"]].copy()

    source_scores = {}

    for source, metrics in SOURCE_METRICS.items():

        active_metrics = [
            metric
            for metric in metrics
            if metric != removed_metric
        ]

        metric_scores = []

        for metric in active_metrics:

            transformed = safe_log(df[metric])
            normalized = robust_normalize(transformed)

            metric_scores.append(normalized)

        if metric_scores:
            source_scores[source] = pd.concat(
                metric_scores,
                axis=1
            ).mean(axis=1)

        else:
            source_scores[source] = pd.Series(
                np.nan,
                index=df.index
            )

    result["development_score"] = source_scores["github"]
    result["developer_interest_score"] = source_scores["stackoverflow"]
    result["model_ecosystem_score"] = source_scores["huggingface"]

    # --------------------------------------------------------
    # Final index
    # --------------------------------------------------------

    source_columns = [
        "development_score",
        "developer_interest_score",
        "model_ecosystem_score",
    ]

    final_scores = []

    for _, row in result.iterrows():

        github = row["development_score"]
        stackoverflow = row["developer_interest_score"]
        huggingface = row["model_ecosystem_score"]

        values = []

        if pd.notna(github):
            values.append(github)

        if pd.notna(stackoverflow):
            values.append(stackoverflow)

        if pd.notna(huggingface):
            values.append(huggingface)

        if not values:
            final_scores.append(np.nan)

        else:
            final_scores.append(np.mean(values))

    result["ai_evolution_score"] = (
        pd.Series(final_scores, index=result.index) * 100
    )

    # --------------------------------------------------------
    # Monthly ranking
    # --------------------------------------------------------

    result["rank"] = (
        result.groupby("month")["ai_evolution_score"]
        .rank(
            ascending=False,
            method="min"
        )
    )

    return result


def compare_with_baseline(ablation_df, baseline_df, scenario):
    """
    Compare one ablation scenario against V1 baseline.
    """

    baseline = baseline_df[
        [
            "month",
            "technology",
            "ai_evolution_score",
            "rank",
        ]
    ].copy()

    baseline = baseline.rename(
        columns={
            "ai_evolution_score": "baseline_score",
            "rank": "baseline_rank",
        }
    )

    comparison = ablation_df.merge(
        baseline,
        on=["month", "technology"],
        how="inner",
    )

    comparison["scenario"] = scenario

    comparison["score_difference"] = (
        comparison["ai_evolution_score"]
        - comparison["baseline_score"]
    )

    comparison["absolute_score_difference"] = (
        comparison["score_difference"].abs()
    )

    comparison["rank_change"] = (
        comparison["rank"]
        - comparison["baseline_rank"]
    )

    comparison["absolute_rank_change"] = (
        comparison["rank_change"].abs()
    )

    comparison["exact_rank_match"] = (
        comparison["rank"]
        == comparison["baseline_rank"]
    )

    return comparison


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION INTELLIGENCE")
print("INDIVIDUAL METRIC ABLATION ANALYSIS")
print("=" * 70)

print("\nLoading feature dataset...")

df = pd.read_csv(INPUT_FILE)

df["month"] = pd.to_datetime(
    df["month"],
    errors="coerce"
)

df = df.sort_values(
    ["month", "technology"]
).reset_index(drop=True)

print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns):,}")


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

required_columns = [
    "month",
    "technology",
] + ALL_METRICS

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
# LOAD V1 BASELINE
# ============================================================

print("\nLoading V1 baseline...")

baseline = pd.read_csv(BASELINE_FILE)

baseline["month"] = pd.to_datetime(
    baseline["month"],
    errors="coerce"
)

baseline = baseline[
    [
        "month",
        "technology",
        "ai_evolution_score",
    ]
].copy()

baseline["rank"] = (
    baseline.groupby("month")["ai_evolution_score"]
    .rank(
        ascending=False,
        method="min"
    )
)

print(f"Baseline rows: {len(baseline):,}")


# ============================================================
# BASELINE RECONSTRUCTION
# ============================================================

print("\nBuilding baseline using all metrics...")

baseline_reconstructed = build_ablation_index(
    df,
    removed_metric=None
)

baseline_comparison = compare_with_baseline(
    baseline_reconstructed,
    baseline,
    "baseline_reconstructed"
)

baseline_score_difference = (
    baseline_comparison["absolute_score_difference"].mean()
)

print(
    f"Baseline reconstruction mean absolute "
    f"score difference: "
    f"{baseline_score_difference:.6f}"
)


# ============================================================
# RUN ABLATION EXPERIMENTS
# ============================================================

all_details = []
summary_rows = []

print("\n" + "=" * 70)
print("RUNNING METRIC ABLATION EXPERIMENTS")
print("=" * 70)

for metric in ALL_METRICS:

    scenario = f"without_{metric}"

    print(f"\nTesting: {scenario}")

    ablation_index = build_ablation_index(
        df,
        removed_metric=metric
    )

    comparison = compare_with_baseline(
        ablation_index,
        baseline,
        scenario
    )

    all_details.append(comparison)

    # --------------------------------------------------------
    # Rank correlation
    # --------------------------------------------------------

    rank_correlation = (
        comparison["rank"]
        .corr(
            comparison["baseline_rank"],
            method="spearman"
        )
    )

    # --------------------------------------------------------
    # Summary statistics
    # --------------------------------------------------------

    summary_rows.append(
        {
            "scenario": scenario,
            "removed_metric": metric,
            "rows": len(comparison),

            "mean_abs_score_difference":
                comparison[
                    "absolute_score_difference"
                ].mean(),

            "max_abs_score_difference":
                comparison[
                    "absolute_score_difference"
                ].max(),

            "mean_abs_rank_change":
                comparison[
                    "absolute_rank_change"
                ].mean(),

            "max_abs_rank_change":
                comparison[
                    "absolute_rank_change"
                ].max(),

            "rank_correlation":
                rank_correlation,

            "exact_rank_match":
                comparison[
                    "exact_rank_match"
                ].mean(),

            "exact_rank_match_count":
                comparison[
                    "exact_rank_match"
                ].sum(),
        }
    )


# ============================================================
# SAVE DETAIL RESULTS
# ============================================================

detail_df = pd.concat(
    all_details,
    ignore_index=True
)

detail_file = (
    OUTPUT_DIR
    / "metric_ablation_detail.csv"
)

detail_df.to_csv(
    detail_file,
    index=False
)


# ============================================================
# SAVE SUMMARY
# ============================================================

summary_df = pd.DataFrame(summary_rows)

summary_df = summary_df.sort_values(
    "mean_abs_rank_change"
)

summary_file = (
    OUTPUT_DIR
    / "metric_ablation_summary.csv"
)

summary_df.to_csv(
    summary_file,
    index=False
)


# ============================================================
# TECHNOLOGY-LEVEL ANALYSIS
# ============================================================

technology_rows = []

for scenario, group in detail_df.groupby(
    "scenario"
):

    for technology, tech_group in group.groupby(
        "technology"
    ):

        technology_rows.append(
            {
                "scenario": scenario,
                "removed_metric":
                    tech_group[
                        "scenario"
                    ].iloc[0].replace(
                        "without_",
                        ""
                    ),

                "technology": technology,

                "mean_abs_score_difference":
                    tech_group[
                        "absolute_score_difference"
                    ].mean(),

                "max_abs_score_difference":
                    tech_group[
                        "absolute_score_difference"
                    ].max(),

                "mean_abs_rank_change":
                    tech_group[
                        "absolute_rank_change"
                    ].mean(),

                "max_abs_rank_change":
                    tech_group[
                        "absolute_rank_change"
                    ].max(),

                "exact_rank_match":
                    tech_group[
                        "exact_rank_match"
                    ].mean(),
            }
        )

technology_df = pd.DataFrame(
    technology_rows
)

technology_file = (
    OUTPUT_DIR
    / "metric_ablation_technology_summary.csv"
)

technology_df.to_csv(
    technology_file,
    index=False
)


# ============================================================
# LATEST MONTH COMPARISON
# ============================================================

latest_month = baseline["month"].max()

latest_df = detail_df[
    detail_df["month"] == latest_month
].copy()

latest_df = latest_df.sort_values(
    [
        "scenario",
        "rank"
    ]
)

latest_file = (
    OUTPUT_DIR
    / "metric_ablation_latest_comparison.csv"
)

latest_df.to_csv(
    latest_file,
    index=False
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("METRIC ABLATION SUMMARY")
print("=" * 70)

display_columns = [
    "scenario",
    "mean_abs_score_difference",
    "max_abs_score_difference",
    "mean_abs_rank_change",
    "max_abs_rank_change",
    "rank_correlation",
    "exact_rank_match",
]

print(
    summary_df[
        display_columns
    ].to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# MOST INFLUENTIAL METRICS
# ============================================================

print("\n" + "=" * 70)
print("MOST INFLUENTIAL METRICS")
print("=" * 70)

influential = summary_df.sort_values(
    "mean_abs_rank_change",
    ascending=False
)

for _, row in influential.iterrows():

    print(
        f"{row['removed_metric']:<28} "
        f"Mean rank change: "
        f"{row['mean_abs_rank_change']:.4f} | "
        f"Rank correlation: "
        f"{row['rank_correlation']:.4f} | "
        f"Exact match: "
        f"{row['exact_rank_match']:.2%}"
    )


# ============================================================
# MOST REDUNDANT / LEAST INFLUENTIAL METRICS
# ============================================================

print("\n" + "=" * 70)
print("LEAST INFLUENTIAL METRICS")
print("=" * 70)

least_influential = summary_df.sort_values(
    "mean_abs_rank_change",
    ascending=True
)

for _, row in least_influential.iterrows():

    print(
        f"{row['removed_metric']:<28} "
        f"Mean rank change: "
        f"{row['mean_abs_rank_change']:.4f} | "
        f"Rank correlation: "
        f"{row['rank_correlation']:.4f} | "
        f"Exact match: "
        f"{row['exact_rank_match']:.2%}"
    )


# ============================================================
# LATEST RANKING EFFECT
# ============================================================

print("\n" + "=" * 70)
print(
    f"LATEST MONTH EFFECT ({latest_month.strftime('%Y-%m')})"
)
print("=" * 70)

for scenario in sorted(
    latest_df["scenario"].unique()
):

    scenario_df = latest_df[
        latest_df["scenario"] == scenario
    ].sort_values("rank")

    print(f"\n{scenario}")

    print(
        scenario_df[
            [
                "technology",
                "ai_evolution_score",
                "baseline_score",
                "rank",
                "baseline_rank",
                "rank_change",
            ]
        ].to_string(
            index=False,
            float_format=lambda x: f"{x:.2f}"
        )
    )


# ============================================================
# FINAL OUTPUT INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nFiles created:")

print(f"  - {detail_file.name}")
print(f"  - {summary_file.name}")
print(f"  - {technology_file.name}")
print(f"  - {latest_file.name}")

print("\nV1 baseline was NOT modified.")