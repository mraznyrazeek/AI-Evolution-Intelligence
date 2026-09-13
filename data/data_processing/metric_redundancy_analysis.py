from pathlib import Path

import numpy as np
import pandas as pd


# ============================================================
# AI EVOLUTION INTELLIGENCE
# METRIC REDUNDANCY / CORRELATION ANALYSIS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "monthly_ai_signals.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "analysis"
    / "metric_redundancy"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# METRIC GROUPS
# ============================================================

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

ALL_METRICS = (
    GITHUB_METRICS
    + STACKOVERFLOW_METRICS
    + HF_METRICS
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION METRIC REDUNDANCY ANALYSIS")
print("=" * 70)

print("\nLoading monthly signals...")

df = pd.read_csv(INPUT_FILE)

print(
    f"Dataset: {df.shape[0]} rows × "
    f"{df.shape[1]} columns"
)


# ============================================================
# VALIDATE COLUMNS
# ============================================================

missing = [
    column
    for column in ALL_METRICS
    if column not in df.columns
]

if missing:
    raise ValueError(
        "Missing required columns:\n"
        + "\n".join(missing)
    )


# ============================================================
# NUMERIC CONVERSION
# ============================================================

for column in ALL_METRICS:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce",
    )


# ============================================================
# LOG TRANSFORMATION
# ============================================================

print("\nApplying log transformation...")

log_df = pd.DataFrame(index=df.index)

for column in ALL_METRICS:

    series = df[column]

    minimum = series.min(skipna=True)

    if pd.isna(minimum):
        log_df[column] = np.nan

    elif minimum < 0:
        log_df[column] = np.log1p(
            series - minimum
        )

    else:
        log_df[column] = np.log1p(series)


# ============================================================
# PEARSON CORRELATION
# ============================================================

print("\nCalculating Pearson correlations...")

pearson_matrix = log_df.corr(
    method="pearson"
)

pearson_file = (
    OUTPUT_DIR
    / "metric_pearson_correlation.csv"
)

pearson_matrix.to_csv(
    pearson_file
)


# ============================================================
# SPEARMAN CORRELATION
# ============================================================

print("Calculating Spearman correlations...")

spearman_matrix = log_df.corr(
    method="spearman"
)

spearman_file = (
    OUTPUT_DIR
    / "metric_spearman_correlation.csv"
)

spearman_matrix.to_csv(
    spearman_file
)


# ============================================================
# SOURCE-SPECIFIC CORRELATION MATRICES
# ============================================================

source_groups = {
    "github": GITHUB_METRICS,
    "stackoverflow": STACKOVERFLOW_METRICS,
    "huggingface": HF_METRICS,
}


for source, metrics in source_groups.items():

    if len(metrics) < 2:
        continue

    source_matrix = spearman_matrix.loc[
        metrics,
        metrics,
    ]

    source_file = (
        OUTPUT_DIR
        / f"{source}_spearman_correlation.csv"
    )

    source_matrix.to_csv(
        source_file
    )


# ============================================================
# PAIRWISE CORRELATION TABLE
# ============================================================

print("\nBuilding pairwise correlation table...")

pairs = []

for i in range(len(ALL_METRICS)):

    for j in range(i + 1, len(ALL_METRICS)):

        metric_a = ALL_METRICS[i]
        metric_b = ALL_METRICS[j]

        pairs.append(
            {
                "metric_a": metric_a,
                "metric_b": metric_b,

                "pearson_correlation": (
                    pearson_matrix.loc[
                        metric_a,
                        metric_b,
                    ]
                ),

                "spearman_correlation": (
                    spearman_matrix.loc[
                        metric_a,
                        metric_b,
                    ]
                ),
            }
        )


pairwise = pd.DataFrame(pairs)


# ============================================================
# ABSOLUTE CORRELATION
# ============================================================

pairwise[
    "absolute_spearman_correlation"
] = pairwise[
    "spearman_correlation"
].abs()

pairwise[
    "absolute_pearson_correlation"
] = pairwise[
    "pearson_correlation"
].abs()


pairwise = pairwise.sort_values(
    "absolute_spearman_correlation",
    ascending=False,
)


pairwise_file = (
    OUTPUT_DIR
    / "metric_pairwise_correlations.csv"
)

pairwise.to_csv(
    pairwise_file,
    index=False,
)


# ============================================================
# HIGH-CORRELATION PAIRS
# ============================================================

print("\nIdentifying highly correlated metric pairs...")

high_correlation = pairwise[
    pairwise[
        "absolute_spearman_correlation"
    ] >= 0.80
].copy()


high_file = (
    OUTPUT_DIR
    / "high_correlation_pairs.csv"
)

high_correlation.to_csv(
    high_file,
    index=False,
)


# ============================================================
# SOURCE INTERNAL REDUNDANCY
# ============================================================

source_summary = []

for source, metrics in source_groups.items():

    if len(metrics) < 2:
        continue

    matrix = spearman_matrix.loc[
        metrics,
        metrics,
    ]

    values = []

    for i in range(len(metrics)):

        for j in range(i + 1, len(metrics)):

            value = matrix.iloc[i, j]

            if pd.notna(value):
                values.append(abs(value))

    if values:

        source_summary.append(
            {
                "source": source,

                "number_of_metrics": len(metrics),

                "mean_absolute_spearman": np.mean(
                    values
                ),

                "maximum_absolute_spearman": np.max(
                    values
                ),

                "minimum_absolute_spearman": np.min(
                    values
                ),

                "high_correlation_pairs": sum(
                    value >= 0.80
                    for value in values
                ),
            }
        )


source_summary = pd.DataFrame(
    source_summary
)


source_summary_file = (
    OUTPUT_DIR
    / "source_redundancy_summary.csv"
)

source_summary.to_csv(
    source_summary_file,
    index=False,
)


# ============================================================
# METRIC MISSINGNESS
# ============================================================

missingness = pd.DataFrame(
    {
        "metric": ALL_METRICS,
        "missing_count": [
            df[column].isna().sum()
            for column in ALL_METRICS
        ],
    }
)

missingness["missing_percentage"] = (
    missingness["missing_count"]
    / len(df)
    * 100
)


missingness_file = (
    OUTPUT_DIR
    / "metric_missingness.csv"
)

missingness.to_csv(
    missingness_file,
    index=False,
)


# ============================================================
# PRINT RESULTS
# ============================================================

print("\n" + "=" * 70)
print("CORRELATION RESULTS")
print("=" * 70)

print("\nAll metric pair correlations:")
print(
    pairwise.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


print("\n" + "=" * 70)
print("HIGH-CORRELATION PAIRS (|Spearman| >= 0.80)")
print("=" * 70)

if high_correlation.empty:

    print(
        "\nNo metric pairs reached the "
        "0.80 correlation threshold."
    )

else:

    print(
        high_correlation.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


print("\n" + "=" * 70)
print("SOURCE REDUNDANCY SUMMARY")
print("=" * 70)

print(
    source_summary.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}",
    )
)


print("\n" + "=" * 70)
print("METRIC MISSINGNESS")
print("=" * 70)

print(
    missingness.to_string(
        index=False,
        float_format=lambda x: f"{x:.2f}",
    )
)


# ============================================================
# INTERPRETATION GUIDE
# ============================================================

print("\n" + "=" * 70)
print("INTERPRETATION GUIDE")
print("=" * 70)

print(
    """
Spearman correlation guidelines:

  0.00–0.39  = weak relationship
  0.40–0.59  = moderate relationship
  0.60–0.79  = strong relationship
  0.80–1.00  = very strong relationship

A very strong correlation does NOT automatically mean
a metric should be removed.

It means we should investigate whether multiple metrics
are measuring substantially the same underlying signal.
"""
)


print("\nFiles created:")

for file in [
    pearson_file,
    spearman_file,
    pairwise_file,
    high_file,
    source_summary_file,
    missingness_file,
]:

    print(f"  ✓ {file}")


print("\n" + "=" * 70)
print("METRIC REDUNDANCY ANALYSIS COMPLETE")
print("=" * 70)