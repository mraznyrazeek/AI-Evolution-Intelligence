# AI Evolution Intelligence — Project Blueprint

> **Status:** Living project blueprint  
> **Project period:** January 2023 → August 2026  
> **Primary objective:** Identify, explain, and forecast emerging AI technology momentum using multi-source ecosystem signals.

---

## 1. Project Title

**AI Evolution Intelligence: A Multi-Source System for Detecting and Forecasting Emerging Artificial Intelligence Technology Trends**

---

## 2. Project Overview

AI Evolution Intelligence is a data-driven intelligence system designed to analyse how artificial intelligence technologies emerge, grow, and become adopted over time.

The system integrates historical information from three complementary ecosystems:

- **GitHub** — what developers are building.
- **Stack Overflow** — what developers are asking about, discussing, and trying to solve.
- **Hugging Face** — what AI models and AI-related technologies are being developed.

Rather than simply predicting that "AI will grow", the project focuses on identifying **which specific AI technologies are gaining momentum, how their signals develop across different ecosystems, and whether historical multi-source patterns can provide useful indications of future technology momentum.**

---

## 3. Core Research Problem

AI technologies evolve rapidly. Technologies such as LLMs, RAG, multimodal AI, AI agents, reasoning models, MCP, embeddings, and generative AI can move through different stages of experimentation and adoption.

No single platform provides a complete view of this evolution.

A technology may first appear as:

1. Something developers are building on GitHub.
2. A topic developers increasingly ask about on Stack Overflow.
3. A growing area of model development on Hugging Face.

The project therefore investigates whether these independent ecosystem signals can be combined to understand and detect AI technology evolution.

---

## 4. Main Research Question

> **Can multi-source ecosystem signals from software development, developer discourse, and open-model activity be used to identify emerging AI technologies and forecast their future momentum?**

### Supporting Research Questions

**RQ1.** How has AI technology activity evolved from 2023 to 2026?

**RQ2.** Which AI technologies demonstrate the strongest emerging momentum?

**RQ3.** Do GitHub, Stack Overflow, and Hugging Face provide complementary or lagged signals of technology adoption?

**RQ4.** Can multi-source signals improve forecasting of future technology momentum compared with single-source approaches?

**RQ5.** Which factors contribute most strongly to the system's predictions?

---

## 5. What the System Is NOT Trying to Predict

The project is **not** primarily trying to answer:

> "Will AI continue to grow?"

That is already broadly expected and would provide limited research value.

Instead, the system aims to answer questions such as:

- Which AI technology is gaining momentum?
- Which technologies are emerging unusually quickly?
- Does activity appear first on one ecosystem and later on another?
- Which technologies are moving from experimentation toward broader adoption?
- Which technologies are likely to gain momentum in the next 1–3 months?
- Why does the system make that prediction?

---

## 6. Three-Source Data Strategy

### 6.1 GitHub

GitHub provides signals related to **developer building activity**.

Potential indicators include:

- AI-related repository creation
- repository count
- stars
- forks
- topics
- languages
- repository growth
- technology/category growth

Interpretation:

> **GitHub provides a signal of what developers are building.**

---

### 6.2 Stack Overflow

Stack Overflow provides signals related to **developer questions, problems, and interest**.

Potential indicators include:

- AI-related questions
- question growth
- views
- scores
- answers
- tags
- technology/category activity
- question/answer activity

Interpretation:

> **Stack Overflow provides a signal of what developers are trying to understand or solve.**

---

### 6.3 Hugging Face

Hugging Face provides signals related to **open-model development and the model ecosystem**.

Potential indicators include:

- total models
- AI-relevant models
- model creation
- downloads
- likes
- pipeline categories
- libraries
- tags
- LLM activity
- text-generation activity
- multimodal activity
- reasoning activity
- embedding activity

Interpretation:

> **Hugging Face provides a signal of what AI models and model-related technologies are being developed.**

---

## 7. Historical Coverage

### Overall project study period

**January 2023 → August 2026**

### Source-specific coverage

| Source | Intended/verified coverage |
|---|---|
| GitHub | January 2023 → August 2026 |
| Stack Overflow | January 2023 → August 2026 |
| Hugging Face Models | July 2024 → August 2026 |

### Hugging Face limitation

The Hugging Face live API was investigated for historical reconstruction. Current Hub search results are not sufficient to reconstruct a complete historical model snapshot for January 2023.

The `hfmlsoc/hub_weekly_snapshots` dataset provides reliable historical model snapshots beginning with the verified **2024-07-24** snapshot.

Therefore:

- The overall study period remains **January 2023 → August 2026**.
- GitHub and Stack Overflow support the longer historical analysis.
- Three-platform comparisons involving Hugging Face are restricted to the common period beginning in **July 2024**.
- Missing Hugging Face historical observations will **not** be fabricated.

This limitation will be documented explicitly in the methodology and limitations sections.

---

## 8. Data Collection Architecture

The project uses a raw-data-first approach.

```text
                    RAW DATA
                       |
        +--------------+--------------+
        |              |              |
      GitHub       Stack Overflow   Hugging Face
        |              |              |
        +--------------+--------------+
                       |
                DATA VALIDATION
                       |
                 DATA CLEANING
                       |
               TEMPORAL ALIGNMENT
                       |
              MONTHLY AGGREGATION
                       |
              FEATURE ENGINEERING
                       |
             AI EVOLUTION DATASET
```

The raw data remains available for reproducibility while derived monthly datasets are created for analysis and modelling.

---

## 9. Current Data Collection Strategy

### Stack Overflow

Historical collection is being performed in monthly periods.

The collector is designed to:

- collect multiple AI-related queries
- paginate results
- deduplicate questions
- save monthly files
- resume without overwriting completed months
- stop safely when API quota becomes low

Example queries include:

- openai
- claude
- gemini
- llm
- rag
- ai-agent
- mcp

---

### GitHub

GitHub historical searches are being collected using an authenticated API.

Historical coverage testing confirmed the availability of AI-related repository results across 2023, 2024, 2025, and 2026.

The GitHub collector should use:

- authenticated requests
- rate-limit awareness
- pagination
- duplicate protection
- resumable collection
- historical date ranges

---

### Hugging Face

Hugging Face model snapshots are being collected from the `hfmlsoc/hub_weekly_snapshots` dataset.

Instead of downloading the entire historical repository, the collector selects **one representative weekly snapshot per month**.

Current strategy:

> Select the last available snapshot within each target month.

The current verified snapshot availability is:

**2024-07-24 → 2026-08-12**

with monthly observations selected from:

**2024-07 → 2026-08**

The collector is resumable and skips existing monthly files.

---

## 10. Hugging Face Monthly Snapshot Strategy

The current selected snapshots include:

```text
2024-07 → 2024-07-31
2024-08 → 2024-08-28
2024-09 → 2024-09-25
2024-10 → 2024-10-30
2024-11 → 2024-11-27
2024-12 → 2024-12-25

2025-01 → 2025-01-29
2025-02 → 2025-02-26
2025-03 → 2025-03-26
2025-04 → 2025-04-30
2025-05 → 2025-05-28
2025-06 → 2025-06-25
2025-07 → 2025-07-30
2025-08 → 2025-08-27
2025-09 → 2025-09-24
2025-10 → 2025-10-29
2025-11 → 2025-11-26
2025-12 → 2025-12-31

2026-01 → 2026-01-28
2026-02 → 2026-02-25
2026-03 → 2026-03-25
2026-04 → 2026-04-29
2026-05 → 2026-05-27
2026-06 → 2026-06-24
2026-07 → 2026-07-29
2026-08 → 2026-08-12
```

This gives approximately 26 monthly Hugging Face observations.

---

## 11. AI Technology Categories

The initial cross-source technology vocabulary includes:

- LLM
- RAG
- AI Agents
- MCP
- Multimodal AI
- Reasoning AI
- Text Generation
- Embeddings

The category system may be refined during data validation and exploratory analysis.

Important principle:

> Categories should be determined from the data and documented rules, rather than being changed simply to produce an expected result.

---

## 12. Data Cleaning and Validation

Before modelling, each source will undergo validation for:

- duplicate records
- missing values
- invalid dates
- malformed records
- inconsistent categories
- impossible values
- API artifacts
- duplicate repositories/questions/models

Each source will retain its raw layer, while cleaned/derived datasets will be stored separately.

---

## 13. Temporal Alignment

The raw data from the three ecosystems will be transformed into a common monthly time scale.

Conceptually:

```text
2023-01
2023-02
2023-03
...
2024-07
2024-08
...
2026-08
```

For the three-platform analysis:

```text
2024-07 → 2026-08
```

will be the primary common comparison period.

---

## 14. Feature Engineering

Potential monthly features include:

### Activity

- total activity
- new activity
- activity growth
- activity share

### Growth

- month-over-month growth
- rolling growth
- growth acceleration

### Popularity

- stars
- forks
- views
- downloads
- likes

### Cross-platform

- GitHub activity
- Stack Overflow activity
- Hugging Face activity
- cross-platform agreement
- cross-platform divergence
- lead/lag relationships

### Technology-specific

- LLM activity
- RAG activity
- AI-agent activity
- MCP activity
- multimodal activity
- reasoning activity
- embedding activity
- text-generation activity

---

# 15. Emerging Technology Detection

This is one of the core intelligence components.

The system should not merely count technologies.

It should determine whether a technology is showing signs of **emergence**.

Potential Emergence Score components:

```text
Emergence Score
|
+-- Growth rate
+-- Growth acceleration
+-- Cross-platform adoption
+-- Developer interest
+-- Model ecosystem growth
+-- Persistence
+-- Novelty
```

A technology that is rapidly growing, accelerating, persistent, and visible across multiple ecosystems should receive a stronger emergence signal.

The exact formula and weighting will be determined experimentally and documented.

---

## 16. Technology Momentum Score

The system will distinguish between popularity and momentum.

A technology can be popular without currently accelerating.

Potential momentum components:

```text
Momentum
|
+-- Recent growth
+-- Acceleration
+-- Cross-platform confirmation
+-- Persistence
```

The output could be normalized to a score such as:

```text
0–100
```

but the final scale and methodology will be determined after exploratory analysis.

---

## 17. Technology Lifecycle Detection

The system may classify technologies into stages such as:

```text
Emerging
    ↓
Experimentation
    ↓
Adoption
    ↓
Mature
    ↓
Declining
```

The lifecycle classification should be derived from measurable historical behaviour rather than manually assigned.

This allows the system to answer:

> Where does a technology currently appear to be in its development/adoption lifecycle?

---

## 18. Cross-Platform Signal and Lead/Lag Analysis

One of the most important research components is investigating whether signals appear at different times across ecosystems.

Example hypothesis:

```text
GitHub activity
      ↓
Stack Overflow interest
      ↓
Hugging Face model activity
```

However, this ordering must **not** be assumed.

The project will test possible relationships using methods such as:

- correlation
- lagged correlation
- cross-correlation
- regression
- time-series analysis

Potential output:

```text
Technology: Example Technology

GitHub → Stack Overflow: +2 months
GitHub → Hugging Face:   +3 months
Stack Overflow → HF:     +1 month
```

These values are examples only and must be derived from the actual data.

---

## 19. Anomaly Detection

The system may identify unusually rapid changes.

Example:

```text
Normal growth:
+5%
+7%
+6%
+8%

Sudden change:
+74%
```

This could trigger an:

> **Emerging Technology / Unusual Activity Alert**

Possible causes can then be investigated using the underlying data.

---

## 20. Forecasting Objective

The forecasting objective is **not** to predict whether AI will grow in general.

The preferred target is:

> **Future technology momentum.**

The system may forecast:

- technology momentum
- category growth
- next-month activity
- short-term 1–3 month momentum

The final target will be selected after examining the quality and stability of the aggregated time series.

---

## 21. Forecasting Features

Potential forecasting inputs include:

- previous momentum
- recent growth
- growth acceleration
- GitHub activity
- Stack Overflow activity
- Hugging Face activity
- category growth
- cross-platform signals
- lagged signals
- rolling averages
- previous technology momentum

---

## 22. Model Development

Potential baseline and machine-learning models include:

### Baselines

- Naive forecast
- historical average
- linear trend

### Machine Learning

- Linear Regression
- Ridge Regression
- Random Forest
- Gradient Boosting
- XGBoost/LightGBM if appropriate

### Time-Series

- ARIMA or other suitable time-series approaches

The final model will be selected based on empirical performance rather than predetermined preference.

---

## 23. Multi-Source vs Single-Source Experiment

A particularly important experiment is to determine whether combining the three sources actually improves forecasting.

Possible comparison:

```text
Model A
Historical momentum only

Model B
+ GitHub

Model C
+ GitHub + Stack Overflow

Model D
+ GitHub + Stack Overflow + Hugging Face
```

If the multi-source model performs better, this can provide evidence supporting the project's central hypothesis.

If it does not, that is also a meaningful research finding and should be reported honestly.

---

## 24. Time-Aware Validation

Because this is a forecasting problem, random train/test splitting should not be the primary validation strategy.

Instead, use chronological/walk-forward validation.

Conceptually:

```text
Train: 2024 ───────── 2025
Test:                    2026

Then expand:

Train: 2024 ─────────── 2026-01
Test:                              2026-02

Then:

Train: 2024 ─────────── 2026-02
Test:                              2026-03
```

This better represents the real-world forecasting situation.

---

## 25. Evaluation Metrics

Potential metrics:

- MAE
- RMSE
- MAPE
- R² where appropriate
- directional accuracy where appropriate

The selected metrics will depend on the final prediction target.

---

## 26. Explainable AI

Predictions should be explainable.

The system should answer:

> **Why does it think this technology will gain momentum?**

Potential explanation methods:

- feature importance
- SHAP
- contribution analysis

Example output:

```text
Forecast: High Momentum

Main contributing signals:
GitHub agent growth          +31%
Stack Overflow activity     +22%
Hugging Face model growth   +28%
Recent acceleration         +14%
Cross-platform agreement     +5%
```

The numerical example above is illustrative only.

---

## 27. Confidence and Uncertainty

The forecasting system should avoid presenting predictions as certainty.

Possible outputs:

```text
Forecast:
High Momentum

Predicted score:
92

Expected range:
86–97

Confidence:
High
```

The exact confidence/interval methodology will depend on the selected model.

---

## 28. Dashboard / Final Application

The final application may provide:

### AI Evolution Overview

- current ecosystem momentum
- overall trends
- source-level activity

### Emerging Technologies

- ranked emerging technologies
- emergence score
- momentum score
- lifecycle stage

### Cross-Platform Analysis

- GitHub vs Stack Overflow vs Hugging Face
- lead/lag relationships
- agreement/divergence

### Forecast

- 1-month forecast
- 3-month forecast
- technology-specific forecasts
- uncertainty

### Explainability

- major factors behind predictions
- feature importance
- SHAP explanations where appropriate

### Historical Exploration

- timeline
- category trends
- source comparisons
- technology growth

---

## 29. Proposed System Architecture

```text
                     DATA SOURCES
                          |
          +---------------+---------------+
          |               |               |
       GitHub        Stack Overflow   Hugging Face
          |               |               |
          +---------------+---------------+
                          |
                    DATA COLLECTION
                          |
                    RAW DATA STORE
                          |
                    DATA VALIDATION
                          |
                     DATA CLEANING
                          |
                  TEMPORAL ALIGNMENT
                          |
                  FEATURE ENGINEERING
                          |
                 MONTHLY FEATURE STORE
                          |
             +------------+------------+
             |            |            |
             ↓            ↓            ↓
         Trend        Emergence     Anomaly
        Analysis      Detection     Detection
             |            |            |
             +------------+------------+
                          |
                   MOMENTUM ENGINE
                          |
                 CROSS-SIGNAL ANALYSIS
                          |
                    ML FORECASTING
                          |
                   EXPLAINABLE AI
                          |
                    BACKEND API
                          |
                    WEB DASHBOARD
```

---

## 30. Expected Research Contribution

The project aims to contribute a practical framework for studying AI ecosystem evolution using multiple independent data sources.

Potential contributions include:

1. A unified multi-source AI technology dataset.
2. A method for detecting emerging AI technology momentum.
3. Cross-platform analysis of developer activity, developer discourse, and model development.
4. Investigation of lead/lag relationships between ecosystem signals.
5. A forecasting approach for short-term technology momentum.
6. Explainable predictions rather than black-box outputs.
7. A visual intelligence dashboard for exploring AI technology evolution.

These are intended contributions; their validity will depend on the final experimental results.

---

## 31. Important Research Principles

The project will follow these principles:

### No fabricated data

Missing historical observations will not be artificially created simply to make datasets align.

### No predetermined findings

Expected technologies such as AI agents or reasoning models should not automatically be declared winners. The data determines the final findings.

### No unsupported causation

A correlation or lead/lag relationship will not automatically be described as causal.

### Reproducibility

Raw data, collection scripts, processing steps, feature engineering, and model experiments should be preserved.

### Honest evaluation

If multi-source forecasting does not outperform simpler models, the result will be reported rather than hidden.

---

## 32. Current Project Status

### Data collection

- [x] GitHub historical coverage testing
- [x] GitHub API authentication
- [x] Stack Overflow historical coverage testing
- [x] Stack Overflow historical collector
- [x] Hugging Face historical API investigation
- [x] Hugging Face snapshot source identified
- [x] Hugging Face snapshot loading verified
- [x] Hugging Face monthly collector created
- [x] Hugging Face resumable collection implemented
- [ ] Complete Hugging Face monthly collection
- [ ] Complete integrity validation across all monthly files

### Data engineering

- [ ] Clean GitHub dataset
- [ ] Clean Stack Overflow dataset
- [ ] Clean Hugging Face dataset
- [ ] Create monthly aggregation layer
- [ ] Create unified feature dataset

### Analysis

- [ ] Exploratory data analysis
- [ ] Technology trend analysis
- [ ] Growth and acceleration analysis
- [ ] Cross-platform correlation
- [ ] Lead/lag analysis
- [ ] Emerging technology scoring
- [ ] Lifecycle classification
- [ ] Anomaly detection

### Machine Learning

- [ ] Define forecasting target
- [ ] Create baseline models
- [ ] Train ML models
- [ ] Train time-series models where appropriate
- [ ] Walk-forward validation
- [ ] Compare single-source vs multi-source models
- [ ] Feature importance / SHAP
- [ ] Final model selection

### Application

- [ ] Backend API
- [ ] Frontend dashboard
- [ ] Historical trend views
- [ ] Emerging technology view
- [ ] Forecasting view
- [ ] Explainability view
- [ ] Final integration
- [ ] Testing


## 33. Final Concept in Simple Terms

> **GitHub tells us what developers are building.**

> **Stack Overflow tells us what developers are trying to solve.**

> **Hugging Face tells us what AI models and model-related technologies are being developed.**

> **AI Evolution Intelligence combines these signals to discover which AI technologies are gaining momentum, investigate how their signals move across ecosystems, identify unusual emerging activity, and estimate which technologies may gain momentum next.**

The project therefore moves through:

```text
Observe
   ↓
Measure
   ↓
Compare
   ↓
Detect
   ↓
Explain
   ↓
Forecast
```

The ultimate goal is **not to predict that AI will grow**.

The goal is to build an evidence-based system that helps answer:

> **"Which AI technologies are emerging, how strong is their momentum, how is that momentum appearing across different ecosystems, and what does the historical evidence suggest may happen next?"**
