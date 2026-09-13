from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# SOURCE-BALANCED METRIC REDUCTION ANALYSIS
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
    / "source_balanced_reduction"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# ORIGINAL V1 METRICS
# ============================================================

V1_METRICS = {
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


# ============================================================
# REDUCED CONFIGURATIONS
# ============================================================
#
# These configurations are based on the earlier redundancy
# analysis.
#
# IMPORTANT:
# These are EXPERIMENTAL configurations.
# V1 is not changed.
#
# GitHub:
#   github_activity was relatively distinct.
#   stars/forks/issues were more correlated.
#
# Stack Overflow:
#   questions/views/answers/score were highly correlated.
#
# Hugging Face:
#   only one metric exists.
#
# ============================================================

CONFIGURATIONS = {

    # --------------------------------------------------------
    # Baseline
    # --------------------------------------------------------

    "v1_all_metrics": {
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
    },

    # --------------------------------------------------------
    # Reduced GitHub
    # --------------------------------------------------------

    "reduced_github": {
        "github": [
            "github_activity",
            "github_stars",
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
    },

    # --------------------------------------------------------
    # Reduced Stack Overflow
    # --------------------------------------------------------

    "reduced_stackoverflow": {
        "github": [
            "github_activity",
            "github_stars",
            "github_forks",
            "github_issues",
        ],
        "stackoverflow": [
            "stackoverflow_questions",
            "stackoverflow_score",
        ],
        "huggingface": [
            "huggingface_models",
        ],
    },

    # --------------------------------------------------------
    # Reduced GitHub + Stack Overflow
    # --------------------------------------------------------

    "reduced_github_stackoverflow": {
        "github": [
            "github_activity",
            "github_stars",
        ],
        "stackoverflow": [
            "stackoverflow_questions",
            "stackoverflow_score",
        ],
        "huggingface": [
            "huggingface_models",
        ],
    },

    # --------------------------------------------------------
    # One representative metric per source
    # --------------------------------------------------------

    "one_metric_per_source": {
        "github": [
            "github_activity",
        ],
        "stackoverflow": [
            "stackoverflow_questions",
        ],
        "huggingface": [
            "huggingface_models",
        ],
    },
}


# ============================================================
# FUNCTIONS
# ============================================================

def safe_log(series):
    """
    Apply log1p transformation.

    For negative-valued series, shift by the minimum
    valid value before applying log1p.
    """

    series = pd.to_numeric(
        series,
        errors="coerce"
    )

    valid = series.dropna()

    if valid.empty:
        return pd.Series(
            np.nan,
            index=series.index
        )

    minimum = valid.min()

    if minimum < 0:
        return np.log1p(
            series - minimum
        )

    return np.log1p(series)


def robust_normalize(series):
    """
    Robust normalization using the 5th and 95th
    percentiles.
    """

    series = pd.to_numeric(
        series,
        errors="coerce"
    )

    valid = series.dropna()

    if valid.empty:
        return pd.Series(
            np.nan,
            index=series.index
        )

    lower = valid.quantile(0.05)
    upper = valid.quantile(0.95)

    if upper <= lower:
        return pd.Series(
            np.where(
                series.notna(),
                0.5,
                np.nan
            ),
            index=series.index
        )

    normalized = (
        series - lower
    ) / (
        upper - lower
    )

    return normalized.clip(0, 1)


def build_index(df, configuration):
    """
    Build an index using the supplied metric configuration.

    Source-level scores are calculated first.

    When Hugging Face is available:
        GitHub = 1/3
        Stack Overflow = 1/3
        Hugging Face = 1/3

    Before Hugging Face coverage:
        GitHub = 1/2
        Stack Overflow = 1/2
    """

    result = df[
        [
            "month",
            "technology",
        ]
    ].copy()

    source_scores = {}

    for source, metrics in configuration.items():

        metric_scores = []

        for metric in metrics:

            transformed = safe_log(
                df[metric]
            )

            normalized = robust_normalize(
                transformed
            )

            metric_scores.append(
                normalized
            )

        if metric_scores:

            source_scores[source] = (
                pd.concat(
                    metric_scores,
                    axis=1
                ).mean(axis=1)
            )

        else:

            source_scores[source] = (
                pd.Series(
                    np.nan,
                    index=df.index
                )
            )

    result["development_score"] = (
        source_scores["github"]
    )

    result["developer_interest_score"] = (
        source_scores["stackoverflow"]
    )

    result["model_ecosystem_score"] = (
        source_scores["huggingface"]
    )

    # --------------------------------------------------------
    # Final source-balanced index
    # --------------------------------------------------------

    final_scores = []

    for _, row in result.iterrows():

        github = row["development_score"]
        stackoverflow = row[
            "developer_interest_score"
        ]
        huggingface = row[
            "model_ecosystem_score"
        ]

        values = []

        if pd.notna(github):
            values.append(github)

        if pd.notna(stackoverflow):
            values.append(stackoverflow)

        if pd.notna(huggingface):
            values.append(huggingface)

        if values:
            final_scores.append(
                np.mean(values) * 100
            )
        else:
            final_scores.append(
                np.nan
            )

    result["ai_evolution_score"] = (
        final_scores
    )

    # --------------------------------------------------------
    # Monthly ranking
    # --------------------------------------------------------

    result["rank"] = (
        result.groupby("month")[
            "ai_evolution_score"
        ]
        .rank(
            ascending=False,
            method="min"
        )
    )

    return result


def compare_to_v1(
    candidate,
    baseline
):
    """
    Compare candidate configuration with V1.
    """

    base = baseline[
        [
            "month",
            "technology",
            "ai_evolution_score",
            "rank",
        ]
    ].copy()

    base = base.rename(
        columns={
            "ai_evolution_score":
                "baseline_score",
            "rank":
                "baseline_rank",
        }
    )

    comparison = candidate.merge(
        base,
        on=[
            "month",
            "technology",
        ],
        how="inner"
    )

    comparison[
        "score_difference"
    ] = (
        comparison["ai_evolution_score"]
        - comparison["baseline_score"]
    )

    comparison[
        "absolute_score_difference"
    ] = (
        comparison["score_difference"]
        .abs()
    )

    comparison[
        "rank_change"
    ] = (
        comparison["rank"]
        - comparison["baseline_rank"]
    )

    comparison[
        "absolute_rank_change"
    ] = (
        comparison["rank_change"]
        .abs()
    )

    comparison[
        "exact_rank_match"
    ] = (
        comparison["rank"]
        == comparison["baseline_rank"]
    )

    comparison["rank_change_direction"] = np.where(
        comparison["rank_change"] < 0,
        "improved",
        np.where(
            comparison["rank_change"] > 0,
            "declined",
            "unchanged"
        )
    )

    return comparison


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION INTELLIGENCE")
print("SOURCE-BALANCED METRIC REDUCTION ANALYSIS")
print("=" * 70)

print("\nLoading feature dataset...")

df = pd.read_csv(
    INPUT_FILE
)

df["month"] = pd.to_datetime(
    df["month"],
    errors="coerce"
)

df = df.sort_values(
    [
        "month",
        "technology",
    ]
).reset_index(
    drop=True
)

print(
    f"Rows: {len(df):,}"
)

print(
    f"Columns: {len(df.columns):,}"
)


# ============================================================
# VALIDATE METRICS
# ============================================================

all_required_metrics = set()

for config in CONFIGURATIONS.values():

    for metrics in config.values():

        all_required_metrics.update(
            metrics
        )

missing = [
    metric
    for metric in all_required_metrics
    if metric not in df.columns
]

if missing:

    raise ValueError(
        "Missing required metrics:\n"
        + "\n".join(missing)
    )


# ============================================================
# LOAD V1
# ============================================================

print("\nLoading V1 baseline...")

baseline = pd.read_csv(
    BASELINE_FILE
)

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
    baseline.groupby("month")[
        "ai_evolution_score"
    ]
    .rank(
        ascending=False,
        method="min"
    )
)

print(
    f"Baseline rows: {len(baseline):,}"
)


# ============================================================
# RUN CONFIGURATIONS
# ============================================================

summary_rows = []
detail_results = []

latest_results = []

latest_month = baseline[
    "month"
].max()

print("\n" + "=" * 70)
print("RUNNING REDUCTION CONFIGURATIONS")
print("=" * 70)


for configuration_name, configuration in (
    CONFIGURATIONS.items()
):

    print(
        f"\nTesting: {configuration_name}"
    )

    candidate = build_index(
        df,
        configuration
    )

    comparison = compare_to_v1(
        candidate,
        baseline
    )

    comparison[
        "configuration"
    ] = configuration_name

    detail_results.append(
        comparison
    )

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
    # Summary
    # --------------------------------------------------------

    summary_rows.append(
        {
            "configuration":
                configuration_name,

            "total_metrics":
                sum(
                    len(metrics)
                    for metrics
                    in configuration.values()
                ),

            "github_metrics":
                len(
                    configuration[
                        "github"
                    ]
                ),

            "stackoverflow_metrics":
                len(
                    configuration[
                        "stackoverflow"
                    ]
                ),

            "huggingface_metrics":
                len(
                    configuration[
                        "huggingface"
                    ]
                ),

            "rows":
                len(comparison),

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

    # --------------------------------------------------------
    # Latest month
    # --------------------------------------------------------

    latest = comparison[
        comparison["month"]
        == latest_month
    ].copy()

    latest_results.append(
        latest
    )


# ============================================================
# SAVE DETAIL
# ============================================================

detail_df = pd.concat(
    detail_results,
    ignore_index=True
)

detail_file = (
    OUTPUT_DIR
    / "source_reduction_detail.csv"
)

detail_df.to_csv(
    detail_file,
    index=False
)


# ============================================================
# SAVE SUMMARY
# ============================================================

summary_df = pd.DataFrame(
    summary_rows
)

summary_df = summary_df.sort_values(
    "mean_abs_rank_change"
)

summary_file = (
    OUTPUT_DIR
    / "source_reduction_summary.csv"
)

summary_df.to_csv(
    summary_file,
    index=False
)


# ============================================================
# TECHNOLOGY-LEVEL SUMMARY
# ============================================================

technology_rows = []

for (
    configuration,
    group
) in detail_df.groupby(
    "configuration"
):

    for (
        technology,
        tech_group
    ) in group.groupby(
        "technology"
    ):

        technology_rows.append(
            {
                "configuration":
                    configuration,

                "technology":
                    technology,

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
    / "source_reduction_technology_summary.csv"
)

technology_df.to_csv(
    technology_file,
    index=False
)


# ============================================================
# SAVE LATEST COMPARISON
# ============================================================

latest_df = pd.concat(
    latest_results,
    ignore_index=True
)

latest_df = latest_df.sort_values(
    [
        "configuration",
        "rank",
    ]
)

latest_file = (
    OUTPUT_DIR
    / "source_reduction_latest_comparison.csv"
)

latest_df.to_csv(
    latest_file,
    index=False
)


# ============================================================
# PRINT SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SOURCE REDUCTION SUMMARY")
print("=" * 70)

print(
    summary_df[
        [
            "configuration",
            "total_metrics",
            "mean_abs_score_difference",
            "max_abs_score_difference",
            "mean_abs_rank_change",
            "max_abs_rank_change",
            "rank_correlation",
            "exact_rank_match",
        ]
    ].to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# LATEST RANKINGS
# ============================================================

print("\n" + "=" * 70)
print(
    f"LATEST MONTH COMPARISON "
    f"({latest_month.strftime('%Y-%m')})"
)
print("=" * 70)

for configuration in CONFIGURATIONS:

    print(
        f"\n{configuration}"
    )

    latest = latest_df[
        latest_df[
            "configuration"
        ] == configuration
    ].sort_values(
        "rank"
    )

    print(
        latest[
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
# BEST REDUCED CONFIGURATION
# ============================================================

non_baseline = summary_df[
    summary_df[
        "configuration"
    ] != "v1_all_metrics"
].copy()

best = non_baseline.sort_values(
    [
        "mean_abs_rank_change",
        "mean_abs_score_difference",
    ]
).iloc[0]

print("\n" + "=" * 70)
print("BEST REDUCED CONFIGURATION")
print("=" * 70)

print(
    f"Configuration: "
    f"{best['configuration']}"
)

print(
    f"Metrics used: "
    f"{int(best['total_metrics'])}"
)

print(
    f"Mean absolute rank change: "
    f"{best['mean_abs_rank_change']:.4f}"
)

print(
    f"Rank correlation: "
    f"{best['rank_correlation']:.4f}"
)

print(
    f"Exact rank agreement: "
    f"{best['exact_rank_match']:.2%}"
)


# ============================================================
# OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("ANALYSIS COMPLETE")
print("=" * 70)

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nFiles created:")
print(
    f"  - {detail_file.name}"
)
print(
    f"  - {summary_file.name}"
)
print(
    f"  - {technology_file.name}"
)
print(
    f"  - {latest_file.name}"
)

print("\nV1 baseline was NOT modified.")