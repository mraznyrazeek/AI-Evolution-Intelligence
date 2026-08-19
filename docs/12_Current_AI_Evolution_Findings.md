# Current AI Evolution Findings

## 1. Purpose

This document records the current findings from **AI Evolution Index
V1** after completion of the unified data pipeline, feature engineering,
index construction, validation, and initial visualization.

This is a project checkpoint for the current version of the methodology.
It is not the final research findings, because advanced analysis and
forecasting have not yet been completed.

## 2. Current Dataset

The unified processed dataset contains:

-   **264 rows**
-   **12 columns** in `monthly_ai_signals.csv`
-   **44 months**
-   **6 AI technology categories**
-   Date range: **2023-01 to 2026-08**

The six technologies are:

1.  `ai_agents`
2.  `llm`
3.  `mcp`
4.  `multimodal_ai`
5.  `rag`
6.  `reasoning_ai`

Expected structure: **44 months × 6 technologies = 264 rows**.

## 3. Data Sources

The current index combines signals from three sources:

### GitHub

-   GitHub activity
-   Stars
-   Forks
-   Issues

### Stack Overflow

-   Questions
-   Views
-   Answers
-   Score

### Hugging Face

-   Model counts

Hugging Face historical coverage begins in **2024-07** in the current
dataset. Earlier months are represented as unavailable rather than being
incorrectly treated as zero model counts.

Current coverage:

-   **26 months with Hugging Face coverage**
-   **18 months without Hugging Face coverage**

The `huggingface_available` field is retained to distinguish these
cases.

## 4. AI Evolution Index V1

The current index contains three source-level components:

-   `development_score`
-   `developer_interest_score`
-   `model_ecosystem_score`

These are combined into:

-   `ai_evolution_score`

The index uses a **0--100 scale**.

Across all 264 technology-month observations:

-   Mean: **50.32**
-   Standard deviation: **23.66**
-   Minimum: **0.30**
-   Maximum: **99.65**

## 5. Latest Technology Ranking

Latest available month: **2026-08**

    Rank Technology        AI Evolution Score
  ------ --------------- --------------------
       1 LLM                            66.73
       2 AI Agents                      49.52
       3 RAG                            39.08
       4 MCP                            39.01
       5 Multimodal AI                  38.94
       6 Reasoning AI                   35.13

LLM has the highest current composite score, followed by AI Agents.

## 6. Long-Term Average Ranking

    Rank Technology        Average Score
  ------ --------------- ---------------
       1 LLM                       87.08
       2 AI Agents                 59.17
       3 RAG                       52.82
       4 MCP                       48.33
       5 Multimodal AI             29.79
       6 Reasoning AI              24.74

LLM has a substantially higher long-term average score than the other
technology categories.

## 7. Rank Stability

Average monthly ranks from validation:

  Technology        Mean Rank
  --------------- -----------
  LLM                    1.00
  AI Agents              2.45
  RAG                    3.25
  MCP                    3.43
  Multimodal AI          5.20
  Reasoning AI           5.66

LLM remained rank 1 throughout the observed period. AI Agents were
generally second, while RAG and MCP competed in the middle positions.

## 8. Source Contribution

  Component                     Mean   Standard Deviation
  -------------------------- ------- --------------------
  Development Score            65.98                25.66
  Developer Interest Score     35.78                31.25
  Model Ecosystem Score        50.29                30.26

Correlation with the final AI Evolution Score:

  Component                    Correlation
  -------------------------- -------------
  Development Score                  0.821
  Developer Interest Score           0.867
  Model Ecosystem Score              0.487

Developer Interest Score currently has the strongest correlation with
the final composite score.

## 9. Weight Sensitivity

The validation included alternative weighting tests:

-   Baseline vs. GitHub 40% weighting rank correlation: **0.9974**
-   Baseline vs. Stack Overflow 40% weighting rank correlation:
    **0.9969**

These very high correlations indicate that rankings are highly stable
under the tested alternative weighting schemes.

## 10. Recent Momentum

Latest-month momentum values:

  Technology        Latest Momentum
  --------------- -----------------
  LLM                        -20.68
  AI Agents                  -16.10
  MCP                         -9.29
  Multimodal AI               -6.67
  Reasoning AI                -8.39
  RAG                         -6.43

Negative momentum should **not** be interpreted as proof that these
technologies are declining in absolute importance. It indicates that
their index scores decreased relative to the preceding period.

Further analysis is required to determine whether these changes are
temporary fluctuations, normalization effects, or meaningful ecosystem
changes.

## 11. Model Ecosystem Finding

Latest model ecosystem scores:

  Technology        Model Ecosystem Score
  --------------- -----------------------
  LLM                              100.00
  AI Agents                         59.89
  Multimodal AI                     77.46
  Reasoning AI                      75.19
  RAG                               44.05
  MCP                               26.90

The model ecosystem differs substantially between technology categories,
with LLM showing the strongest ecosystem score in the current index.

## 12. Important Data-Quality Observation

A notable issue was identified in the Developer Interest Score.

Reasoning AI remains near the lower normalization boundary for much of
the study period, with a minimum value of approximately **0.60**.

This may be associated with weak or unavailable Stack Overflow activity
rather than necessarily representing genuinely negligible developer
interest.

Therefore, this behaviour should be investigated before final
forecasting or lifecycle analysis.

The current index should not be rebuilt solely from this observation.
The next stage should diagnose the underlying source-level values and
normalization behaviour first.

## 13. Current Limitations

1.  The study contains six technology categories.
2.  The historical period contains 44 monthly observations per
    technology.
3.  Hugging Face data is available only from 2024-07 onward.
4.  Stack Overflow activity varies substantially between technologies.
5.  Source measurements are not perfectly comparable across platforms.
6.  Composite scores depend on the selected normalization and weighting
    methodology.
7.  Recent momentum can be affected by short-term fluctuations.
8.  The index measures observable ecosystem signals rather than the
    complete real-world importance of an AI technology.

## 14. Current Visualizations

Initial visualizations have been generated for:

-   AI Evolution Score over time
-   Model Ecosystem over time
-   Monthly technology ranking heatmap
-   Latest technology comparison
-   Long-term average technology comparison
-   Recent momentum
-   Hugging Face data availability
-   Developer Interest over time
-   Development Activity over time

## 15. Current Project Status

### Completed

-   [x] Raw data collection
-   [x] Data source validation
-   [x] Unified monthly dataset
-   [x] Feature engineering
-   [x] AI Evolution Index V1
-   [x] Structural validation
-   [x] Score-range validation
-   [x] Missing-value validation
-   [x] Hugging Face coverage validation
-   [x] Source contribution analysis
-   [x] Rank stability analysis
-   [x] Weight sensitivity testing
-   [x] Initial visualizations

### Next Stage

The next stage is **Advanced AI Evolution Analysis**:

1.  Growth-rate analysis
2.  Acceleration and deceleration analysis
3.  Turning-point detection
4.  Ranking transitions
5.  Source contribution analysis
6.  Technology lifecycle analysis
7.  Diagnosis of Developer Interest normalization
8.  Time-series forecasting
9.  Forecast evaluation
10. Integration of final intelligence results into the application

## 16. Checkpoint Conclusion

AI Evolution Index V1 has successfully produced a structured monthly
intelligence dataset covering six AI technology categories from
**2023-01 through 2026-08**.

The index produces differentiated technology scores, stable rankings
under the tested alternative weighting schemes, and interpretable
development, developer-interest, and model-ecosystem components.

At the current stage, **LLM has the strongest long-term and latest
composite position**, while AI Agents consistently occupy the
next-highest position. RAG and MCP form a middle group, with Multimodal
AI and Reasoning AI generally ranking lower in the composite index.

These findings represent a **validated V1 baseline**, not the final
conclusion of the project.

The next objective is to move from descriptive measurement toward
**advanced evolutionary analysis and forecasting**.
