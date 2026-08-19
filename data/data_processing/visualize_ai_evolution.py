from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# AI EVOLUTION INTELLIGENCE
# HISTORICAL VISUALIZATION
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
    / "figures"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("AI EVOLUTION INTELLIGENCE")
print("HISTORICAL VISUALIZATION")
print("=" * 70)

df = pd.read_csv(INPUT_FILE)

df["month"] = pd.to_datetime(
    df["month"]
)

df = df.sort_values(
    ["month", "technology"]
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
# TECHNOLOGIES
# ============================================================

technologies = sorted(
    df["technology"].unique()
)


# ============================================================
# 1. AI EVOLUTION SCORE OVER TIME
# ============================================================

print("\nCreating Figure 1...")

plt.figure(
    figsize=(14, 8)
)

for technology in technologies:

    subset = df[
        df["technology"]
        == technology
    ]

    plt.plot(
        subset["month"],
        subset["ai_evolution_score"],
        marker="o",
        markersize=3,
        linewidth=2,
        label=technology
    )

plt.title(
    "AI Evolution Score Over Time",
    fontsize=16
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "AI Evolution Score (0–100)"
)

plt.grid(
    alpha=0.3
)

plt.legend(
    title="Technology"
)

plt.tight_layout()

figure1 = (
    OUTPUT_DIR
    / "01_ai_evolution_score_over_time.png"
)

plt.savefig(
    figure1,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 2. SOURCE DIMENSIONS OVER TIME
# ============================================================

print("Creating Figure 2...")

source_columns = {
    "Development Activity":
        "development_score",

    "Developer Interest":
        "developer_interest_score",

    "Model Ecosystem":
        "model_ecosystem_score",
}

for title, column in source_columns.items():

    plt.figure(
        figsize=(14, 8)
    )

    for technology in technologies:

        subset = df[
            df["technology"]
            == technology
        ]

        plt.plot(
            subset["month"],
            subset[column],
            marker="o",
            markersize=2,
            linewidth=1.8,
            label=technology
        )

    plt.title(
        f"{title} Over Time",
        fontsize=16
    )

    plt.xlabel(
        "Month"
    )

    plt.ylabel(
        "Score (0–100)"
    )

    plt.grid(
        alpha=0.3
    )

    plt.legend(
        title="Technology"
    )

    plt.tight_layout()

    safe_name = (
        title
        .lower()
        .replace(
            " ",
            "_"
        )
    )

    output_file = (
        OUTPUT_DIR
        / f"02_{safe_name}_over_time.png"
    )

    plt.savefig(
        output_file,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close()


# ============================================================
# 3. TECHNOLOGY RANKING HEATMAP
# ============================================================

print("Creating Figure 3...")

ranking = (
    df[
        [
            "month",
            "technology",
            "ai_evolution_score",
        ]
    ]
    .copy()
)

ranking["rank"] = (
    ranking
    .groupby("month")[
        "ai_evolution_score"
    ]
    .rank(
        ascending=False,
        method="min"
    )
)

rank_matrix = (
    ranking
    .pivot(
        index="technology",
        columns="month",
        values="rank"
    )
)

plt.figure(
    figsize=(18, 6)
)

plt.imshow(
    rank_matrix,
    aspect="auto",
    interpolation="nearest"
)

plt.colorbar(
    label="Rank"
)

plt.yticks(
    range(len(rank_matrix.index)),
    rank_matrix.index
)

# Reduce number of x-axis labels
step = max(
    1,
    len(rank_matrix.columns) // 12
)

x_positions = range(
    0,
    len(rank_matrix.columns),
    step
)

x_labels = [
    rank_matrix.columns[i].strftime(
        "%Y-%m"
    )
    for i in x_positions
]

plt.xticks(
    x_positions,
    x_labels,
    rotation=45,
    ha="right"
)

plt.title(
    "Monthly Technology Ranking",
    fontsize=16
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Technology"
)

plt.tight_layout()

figure3 = (
    OUTPUT_DIR
    / "03_technology_ranking_heatmap.png"
)

plt.savefig(
    figure3,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 4. LATEST TECHNOLOGY COMPARISON
# ============================================================

print("Creating Figure 4...")

latest_month = (
    df["month"].max()
)

latest = (
    df[
        df["month"]
        == latest_month
    ]
    .sort_values(
        "ai_evolution_score",
        ascending=False
    )
)

plt.figure(
    figsize=(12, 7)
)

plt.bar(
    latest["technology"],
    latest["ai_evolution_score"]
)

plt.title(
    f"AI Evolution Score — "
    f"{latest_month:%Y-%m}",
    fontsize=16
)

plt.xlabel(
    "Technology"
)

plt.ylabel(
    "AI Evolution Score (0–100)"
)

plt.xticks(
    rotation=30,
    ha="right"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

figure4 = (
    OUTPUT_DIR
    / "04_latest_technology_comparison.png"
)

plt.savefig(
    figure4,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 5. LONG-TERM AVERAGE COMPARISON
# ============================================================

print("Creating Figure 5...")

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

plt.figure(
    figsize=(12, 7)
)

plt.bar(
    average_scores.index,
    average_scores.values
)

plt.title(
    "Average AI Evolution Score "
    "Across Study Period",
    fontsize=16
)

plt.xlabel(
    "Technology"
)

plt.ylabel(
    "Average Score (0–100)"
)

plt.xticks(
    rotation=30,
    ha="right"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

figure5 = (
    OUTPUT_DIR
    / "05_long_term_average_comparison.png"
)

plt.savefig(
    figure5,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 6. RECENT MOMENTUM
# ============================================================

print("Creating Figure 6...")

recent_cutoff = (
    df["month"].max()
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

plt.figure(
    figsize=(12, 7)
)

plt.bar(
    recent_momentum.index,
    recent_momentum.values
)

plt.axhline(
    0,
    linewidth=1
)

plt.title(
    "Average Recent Momentum "
    "— Last 6 Months",
    fontsize=16
)

plt.xlabel(
    "Technology"
)

plt.ylabel(
    "Average Monthly Score Change"
)

plt.xticks(
    rotation=30,
    ha="right"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

figure6 = (
    OUTPUT_DIR
    / "06_recent_momentum.png"
)

plt.savefig(
    figure6,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 7. HUGGING FACE COVERAGE
# ============================================================

print("Creating Figure 7...")

hf_monthly = (
    df.groupby(
        "month"
    )[
        "huggingface_available"
    ]
    .first()
)

plt.figure(
    figsize=(14, 4)
)

plt.step(
    hf_monthly.index,
    hf_monthly.values,
    where="post",
    linewidth=2
)

plt.yticks(
    [0, 1],
    [
        "Unavailable",
        "Available"
    ]
)

plt.title(
    "Hugging Face Data Availability",
    fontsize=16
)

plt.xlabel(
    "Month"
)

plt.ylabel(
    "Coverage"
)

plt.grid(
    alpha=0.3
)

plt.tight_layout()

figure7 = (
    OUTPUT_DIR
    / "07_huggingface_coverage.png"
)

plt.savefig(
    figure7,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# SAVE LATEST RANKING TABLE
# ============================================================

latest_output = (
    latest[
        [
            "technology",
            "development_score",
            "developer_interest_score",
            "model_ecosystem_score",
            "ai_evolution_score",
            "evolution_momentum",
        ]
    ]
    .copy()
)

latest_output[
    "rank"
] = range(
    1,
    len(latest_output) + 1
)

latest_output.to_csv(
    OUTPUT_DIR
    / "latest_technology_ranking.csv",
    index=False
)


# ============================================================
# SAVE MONTHLY RANKING MATRIX
# ============================================================

rank_matrix.to_csv(
    OUTPUT_DIR
    / "technology_ranking_matrix.csv"
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("VISUALIZATION COMPLETE")
print("=" * 70)

print(
    f"\nFigures saved to:"
)

print(
    OUTPUT_DIR
)

print("\nGenerated figures:")

for file in sorted(
    OUTPUT_DIR.glob("*.png")
):

    print(
        f"  - {file.name}"
    )

print("\nGenerated tables:")

print(
    "  - latest_technology_ranking.csv"
)

print(
    "  - technology_ranking_matrix.csv"
)

print("\n" + "=" * 70)