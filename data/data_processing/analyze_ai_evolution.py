from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# AI EVOLUTION INTELLIGENCE
# HISTORICAL AI EVOLUTION ANALYSIS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
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
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
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
print("HISTORICAL AI EVOLUTION ANALYSIS")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

df["month"] = pd.to_datetime(
    df["month"]
)

df = df.sort_values(
    ["technology", "month"]
).reset_index(drop=True)

print(
    f"\nRows: {len(df)}"
)

print(
    f"Date range: "
    f"{df['month'].min():%Y-%m} "
    f"→ "
    f"{df['month'].max():%Y-%m}"
)


# ============================================================
# 1. MONTHLY TECHNOLOGY RANKINGS
# ============================================================

print("\n" + "-" * 70)
print("1. MONTHLY TECHNOLOGY RANKINGS")
print("-" * 70)

monthly_rankings = (
    df[
        [
            "month",
            "technology",
            "ai_evolution_score",
        ]
    ]
    .copy()
)

monthly_rankings[
    "rank"
] = (
    monthly_rankings
    .groupby("month")[
        "ai_evolution_score"
    ]
    .rank(
        ascending=False,
        method="min"
    )
)

monthly_rankings = (
    monthly_rankings
    .sort_values(
        [
            "month",
            "rank"
        ]
    )
)

monthly_rankings.to_csv(
    OUTPUT_DIR
    / "monthly_technology_rankings.csv",
    index=False
)


# ============================================================
# 2. TECHNOLOGY SUMMARY
# ============================================================

print("\n" + "-" * 70)
print("2. TECHNOLOGY HISTORICAL SUMMARY")
print("-" * 70)

technology_summary = (
    df.groupby(
        "technology"
    )
    .agg(
        average_score=(
            "ai_evolution_score",
            "mean"
        ),
        median_score=(
            "ai_evolution_score",
            "median"
        ),
        minimum_score=(
            "ai_evolution_score",
            "min"
        ),
        maximum_score=(
            "ai_evolution_score",
            "max"
        ),
        volatility=(
            "ai_evolution_score",
            "std"
        ),
        average_momentum=(
            "evolution_momentum",
            "mean"
        ),
    )
    .sort_values(
        "average_score",
        ascending=False
    )
)

print(
    technology_summary.to_string()
)

technology_summary.to_csv(
    OUTPUT_DIR
    / "technology_historical_summary.csv"
)


# ============================================================
# 3. START → END CHANGE
# ============================================================

print("\n" + "-" * 70)
print("3. START → END EVOLUTION")
print("-" * 70)

start_month = (
    df["month"].min()
)

end_month = (
    df["month"].max()
)

start_scores = (
    df[
        df["month"]
        == start_month
    ]
    [
        [
            "technology",
            "ai_evolution_score",
        ]
    ]
    .rename(
        columns={
            "ai_evolution_score":
                "start_score"
        }
    )
)

end_scores = (
    df[
        df["month"]
        == end_month
    ]
    [
        [
            "technology",
            "ai_evolution_score",
        ]
    ]
    .rename(
        columns={
            "ai_evolution_score":
                "end_score"
        }
    )
)

evolution_change = (
    start_scores
    .merge(
        end_scores,
        on="technology"
    )
)

evolution_change[
    "absolute_change"
] = (
    evolution_change[
        "end_score"
    ]
    -
    evolution_change[
        "start_score"
    ]
)

evolution_change[
    "percentage_change"
] = np.where(
    evolution_change[
        "start_score"
    ] != 0,

    (
        evolution_change[
            "absolute_change"
        ]
        /
        evolution_change[
            "start_score"
        ]
    )
    * 100,

    np.nan
)

evolution_change = (
    evolution_change
    .sort_values(
        "absolute_change",
        ascending=False
    )
)

print(
    evolution_change.to_string(
        index=False
    )
)

evolution_change.to_csv(
    OUTPUT_DIR
    / "technology_start_end_change.csv",
    index=False
)


# ============================================================
# 4. PEAK ANALYSIS
# ============================================================

print("\n" + "-" * 70)
print("4. PEAK ANALYSIS")
print("-" * 70)

peak_records = []

for technology in TECHNOLOGIES:

    subset = df[
        df["technology"]
        == technology
    ].copy()

    peak_row = subset.loc[
        subset[
            "ai_evolution_score"
        ].idxmax()
    ]

    peak_records.append(
        {
            "technology": technology,
            "peak_month":
                peak_row[
                    "month"
                ],
            "peak_score":
                peak_row[
                    "ai_evolution_score"
                ],
        }
    )


peak_analysis = pd.DataFrame(
    peak_records
)

peak_analysis = (
    peak_analysis
    .sort_values(
        "peak_score",
        ascending=False
    )
)

print(
    peak_analysis.to_string(
        index=False
    )
)

peak_analysis.to_csv(
    OUTPUT_DIR
    / "technology_peak_analysis.csv",
    index=False
)


# ============================================================
# 5. LOWEST POINT ANALYSIS
# ============================================================

print("\n" + "-" * 70)
print("5. LOWEST POINT ANALYSIS")
print("-" * 70)

low_records = []

for technology in TECHNOLOGIES:

    subset = df[
        df["technology"]
        == technology
    ].copy()

    low_row = subset.loc[
        subset[
            "ai_evolution_score"
        ].idxmin()
    ]

    low_records.append(
        {
            "technology": technology,
            "lowest_month":
                low_row[
                    "month"
                ],
            "lowest_score":
                low_row[
                    "ai_evolution_score"
                ],
        }
    )


low_analysis = pd.DataFrame(
    low_records
)

low_analysis = (
    low_analysis
    .sort_values(
        "lowest_score"
    )
)

print(
    low_analysis.to_string(
        index=False
    )
)

low_analysis.to_csv(
    OUTPUT_DIR
    / "technology_lowest_analysis.csv",
    index=False
)


# ============================================================
# 6. INFLECTION / ACCELERATION ANALYSIS
# ============================================================

print("\n" + "-" * 70)
print("6. STRONGEST POSITIVE MOVEMENTS")
print("-" * 70)

positive_movements = (
    df[
        [
            "month",
            "technology",
            "ai_evolution_score",
            "evolution_change",
            "evolution_momentum",
        ]
    ]
    .dropna(
        subset=[
            "evolution_change"
        ]
    )
    .sort_values(
        "evolution_change",
        ascending=False
    )
    .head(20)
)

print(
    positive_movements.to_string(
        index=False
    )
)

positive_movements.to_csv(
    OUTPUT_DIR
    / "strongest_positive_movements.csv",
    index=False
)


# ============================================================
# 7. STRONGEST NEGATIVE MOVEMENTS
# ============================================================

print("\n" + "-" * 70)
print("7. STRONGEST NEGATIVE MOVEMENTS")
print("-" * 70)

negative_movements = (
    df[
        [
            "month",
            "technology",
            "ai_evolution_score",
            "evolution_change",
            "evolution_momentum",
        ]
    ]
    .dropna(
        subset=[
            "evolution_change"
        ]
    )
    .sort_values(
        "evolution_change"
    )
    .head(20)
)

print(
    negative_movements.to_string(
        index=False
    )
)

negative_movements.to_csv(
    OUTPUT_DIR
    / "strongest_negative_movements.csv",
    index=False
)


# ============================================================
# 8. TECHNOLOGY CROSSOVERS
# ============================================================

print("\n" + "-" * 70)
print("8. TECHNOLOGY RANK CROSSOVERS")
print("-" * 70)

rank_pivot = (
    monthly_rankings
    .pivot(
        index="month",
        columns="technology",
        values="rank"
    )
)

crossover_records = []

for i in range(
    len(TECHNOLOGIES)
):

    for j in range(
        i + 1,
        len(TECHNOLOGIES)
    ):

        tech_a = TECHNOLOGIES[i]
        tech_b = TECHNOLOGIES[j]

        if (
            tech_a not in rank_pivot.columns
            or
            tech_b not in rank_pivot.columns
        ):
            continue

        difference = (
            rank_pivot[
                tech_a
            ]
            -
            rank_pivot[
                tech_b
            ]
        )

        previous = (
            difference.shift(1)
        )

        crossover = (
            (
                (
                    difference
                    > 0
                )
                &
                (
                    previous
                    < 0
                )
            )
            |
            (
                (
                    difference
                    < 0
                )
                &
                (
                    previous
                    > 0
                )
            )
        )

        crossover_months = (
            crossover[
                crossover
            ].index
        )

        for month in crossover_months:

            crossover_records.append(
                {
                    "month": month,
                    "technology_a":
                        tech_a,
                    "technology_b":
                        tech_b,
                }
            )


crossovers = pd.DataFrame(
    crossover_records
)

if len(crossovers) == 0:

    print(
        "No rank crossovers detected."
    )

else:

    print(
        crossovers.to_string(
            index=False
        )
    )


crossovers.to_csv(
    OUTPUT_DIR
    / "technology_rank_crossovers.csv",
    index=False
)


# ============================================================
# 9. RECENT 6-MONTH MOMENTUM
# ============================================================

print("\n" + "-" * 70)
print("9. RECENT MOMENTUM")
print("-" * 70)

recent_cutoff = (
    end_month
    - pd.DateOffset(
        months=5
    )
)

recent = df[
    df["month"]
    >= recent_cutoff
].copy()

recent_momentum = (
    recent.groupby(
        "technology"
    )[
        "evolution_change"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)

print(
    recent_momentum.to_string()
)

recent_momentum.to_csv(
    OUTPUT_DIR
    / "recent_6_month_momentum.csv"
)


# ============================================================
# 10. CONSISTENCY / DIRECTION
# ============================================================

print("\n" + "-" * 70)
print("10. DIRECTIONAL CONSISTENCY")
print("-" * 70)

direction_records = []

for technology in TECHNOLOGIES:

    subset = df[
        df["technology"]
        == technology
    ]

    changes = (
        subset[
            "evolution_change"
        ]
        .dropna()
    )

    positive = (
        changes > 0
    ).sum()

    negative = (
        changes < 0
    ).sum()

    total = len(changes)

    direction_records.append(
        {
            "technology":
                technology,
            "positive_months":
                positive,
            "negative_months":
                negative,
            "positive_ratio":
                positive / total
                if total
                else np.nan,
        }
    )


direction_analysis = pd.DataFrame(
    direction_records
)

print(
    direction_analysis.to_string(
        index=False
    )
)

direction_analysis.to_csv(
    OUTPUT_DIR
    / "directional_consistency.csv",
    index=False
)


# ============================================================
# 11. FINAL ANALYSIS DATASET
# ============================================================

analysis_dataset = df[
    [
        "month",
        "technology",
        "development_score",
        "developer_interest_score",
        "model_ecosystem_score",
        "ai_evolution_score",
        "evolution_change",
        "evolution_growth",
        "evolution_rolling_3m",
        "evolution_momentum",
    ]
].copy()

analysis_dataset.to_csv(
    OUTPUT_DIR
    / "ai_evolution_historical_analysis.csv",
    index=False
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("HISTORICAL ANALYSIS COMPLETE")
print("=" * 70)

print(
    f"\nAnalysis files saved to:"
)

print(
    OUTPUT_DIR
)

print(
    "\nGenerated:"
)

print(
    "  - monthly_technology_rankings.csv"
)

print(
    "  - technology_historical_summary.csv"
)

print(
    "  - technology_start_end_change.csv"
)

print(
    "  - technology_peak_analysis.csv"
)

print(
    "  - technology_lowest_analysis.csv"
)

print(
    "  - strongest_positive_movements.csv"
)

print(
    "  - strongest_negative_movements.csv"
)

print(
    "  - technology_rank_crossovers.csv"
)

print(
    "  - recent_6_month_momentum.csv"
)

print(
    "  - directional_consistency.csv"
)

print(
    "  - ai_evolution_historical_analysis.csv"
)

print("\n" + "=" * 70)