# AI Evolution Intelligence
## Data Collection, Provenance & Validation Report

**Project status:** Research data acquisition and validation completed  
**Prepared:** August 2026  
**Study focus:** AI ecosystem evolution, emerging technology signals, and future trend forecasting

---

## 1. Executive Summary

AI Evolution Intelligence studies the evolution of AI technologies by combining signals from three complementary ecosystems:

1. **GitHub** — software development and repository activity
2. **Stack Overflow** — developer questions and technical interest
3. **Hugging Face** — AI model ecosystem and model creation activity

The purpose is not merely to show that AI is growing. The research will investigate whether complementary ecosystem signals can identify technology momentum, detect emerging AI technologies, and support short-term forecasting.

The raw datasets have now been collected, stored, and independently validated.

**Reddit has been excluded from the final research pipeline.**

---

# 2. Final Data Sources

## 2.1 GitHub

GitHub provides a development-oriented signal through monthly repository searches around:

- RAG
- LLM
- AI Agents
- MCP
- Multimodal AI
- Reasoning AI

Repository records include identifiers, repository names, descriptions, URLs, dates, stars, watchers, forks, issues, languages, topics, licenses, and repository status fields.

**Coverage:** January 2023 → August 2026  
**Monthly files:** 44  
**Validated records:** 20,514

The collector tracks both raw results and unique repository counts, allowing deduplication to be documented.

---

## 2.2 Stack Overflow

Stack Overflow provides a developer-interest and developer-question signal.

Queries used:

- openai
- claude
- gemini
- llm
- rag
- ai-agent
- mcp

Question records include tags, question ID, title, creation date, last activity date, views, answers, score, answered status, license, and URL.

**Coverage:** January 2023 → August 2026  
**Monthly files:** 44  
**Validated records:** 7,693

January 2023 uses a legacy metadata structure. The raw file was deliberately preserved rather than rewritten; the validator recognizes the legacy schema.

---

## 2.3 Hugging Face

Hugging Face provides a model-ecosystem signal through monthly Hub snapshots filtered to AI-relevant models.

Relevant categories include:

- LLM
- text generation
- multimodal
- reasoning
- embedding

**Coverage:** July 2024 → August 2026  
**Monthly files:** 26  
**Validated records:** 13,595,404

The August 2026 snapshot contained 2,984,779 total snapshot rows and 854,999 AI-relevant models.

---

# 3. Why Three Sources?

The sources measure different layers of the AI ecosystem:

| Source | Primary signal |
|---|---|
| GitHub | Development activity |
| Stack Overflow | Developer questions / technical interest |
| Hugging Face | Model ecosystem activity |

This creates a multi-source research design rather than relying on one popularity metric.

The planned research will investigate whether these signals move together, diverge, or potentially lead/lag one another.

---

# 4. Reddit Exclusion

Reddit was considered as a possible additional source but has been **excluded from the final research dataset and modelling pipeline**.

The final research therefore focuses on:

> **GitHub + Stack Overflow + Hugging Face**

No Reddit data should be added to the unified research dataset unless the research design is explicitly changed and documented.

---

# 5. Data Storage Architecture

Large raw datasets were moved from the system drive to E:.

Project/code location:

```text
C:\Projects\AI-Evolution-Intelligence
```

Raw-data physical storage:

```text
E:\AI-Evolution-Intelligence
```

The project maintains junctions so existing code can continue using:

```text
data/raw/github
data/raw/stackoverflow
data/raw/huggingface
```

while the actual large files reside on E:.

The Hugging Face working cache was also moved to:

```text
E:\AI-Evolution-Intelligence\huggingface-cache
```

with Hugging Face cache environment variables configured for E:.

---

# 6. Data Validation

Each source was independently validated for:

- valid JSON
- expected structure
- required identifiers
- missing critical fields
- valid dates
- duplicate records
- monthly-file coverage
- source-specific metadata consistency

Raw source files were not rewritten merely to satisfy validation.

---

# 7. GitHub Validation Result

```text
Files:                 44
Passed:                44
Warnings:               0
Failed:                 0
Total records:     20,514
Duplicate IDs:          0
```

Additional checks found no missing repository IDs, missing repository names, invalid `created_at` values, or invalid `updated_at` values.

**Status: GITHUB DATA — PASS**

---

# 8. Stack Overflow Validation Result

```text
Files:                 44
Passed:                44
Failed:                 0
Legacy metadata:        1
Total records:       7,693
Duplicate IDs:          0
```

Additional checks found:

- no missing question IDs
- no missing titles
- no invalid/missing tags
- no missing search queries
- no invalid creation dates
- no invalid activity dates

**Status: STACK OVERFLOW DATA — PASS**

---

# 9. Hugging Face Validation Result

```text
Files:             26
Passed:            26
Failed:             0
```

A corrupted November 2024 JSON file was identified during validation. The November snapshot was recollected successfully and the corrected file passed validation.

**Status: HUGGING FACE DATA — PASS**

---

# 10. Final Validation Summary

| Source | Coverage | Files | Records | Validation |
|---|---|---:|---:|---|
| GitHub | 2023-01 → 2026-08 | 44 | 20,514 | PASS |
| Stack Overflow | 2023-01 → 2026-08 | 44 | 7,693 | PASS |
| Hugging Face | 2024-07 → 2026-08 | 26 | 13,595,404 | PASS |

**Combined validated raw-record count: 13,623,611**

This is a sum of source-level observations, not 13.6 million unique technologies or entities. The three sources measure different types of observations.

---

# 11. Coverage Limitation

The sources do not have identical historical coverage.

GitHub and Stack Overflow begin in January 2023.

Hugging Face begins in July 2024 because earlier monthly snapshots were not available from the selected snapshot source.

Therefore:

### Full three-source analysis

```text
July 2024 → August 2026
```

### Extended two-source analysis

```text
January 2023 → June 2024
GitHub + Stack Overflow
```

Missing Hugging Face history must **not** be interpreted as zero activity.

---

# 12. Completed Work

## Data Acquisition

- [x] GitHub collection
- [x] Stack Overflow collection
- [x] Hugging Face collection
- [x] Reddit excluded

## Storage

- [x] Raw datasets moved to E:
- [x] GitHub junction created
- [x] Stack Overflow junction created
- [x] Hugging Face junction created
- [x] Hugging Face cache moved to E:

## Quality Assurance

- [x] GitHub validation
- [x] Stack Overflow validation
- [x] Hugging Face validation
- [x] Corrupted November 2024 Hugging Face file recovered
- [x] Legacy Stack Overflow metadata documented

**Current status: RAW DATA COLLECTION AND VALIDATION COMPLETE**

---

# 13. Next Research Stage

The project should now move from **data acquisition** to **research data engineering**.

The next pipeline is:

```text
RAW DATA
   ↓
Source-specific validation
   ↓
Technology taxonomy / mapping
   ↓
Monthly aggregation
   ↓
Feature engineering
   ↓
Cross-source alignment
   ↓
Exploratory analysis
   ↓
Signal and momentum detection
   ↓
Lag analysis
   ↓
Forecasting
   ↓
Time-based backtesting
   ↓
Research findings
```

The project should **not** immediately train a forecasting model. First, the three sources must be transformed into comparable monthly technology signals.

---

# 14. Planned Research Signals

### GitHub

Potential signals:

- repository count
- repository growth
- stars
- forks
- update/activity frequency
- technology-specific momentum

### Stack Overflow

Potential signals:

- question volume
- tag frequency
- views
- answers
- scores
- question growth
- developer-interest momentum

### Hugging Face

Potential signals:

- model count
- AI-relevant model count
- category distribution
- category growth
- new-model activity
- model-category momentum

These features will be formally defined before modelling.

---

# 15. Core Research Objective

The central research question is:

> **Can complementary signals from software development, developer questions, and AI model ecosystems be combined to detect emerging AI technology momentum and support short-term forecasting?**

The project is therefore not simply asking whether AI is growing.

It will investigate:

1. Which AI technologies are gaining momentum?
2. Do different ecosystems show similar trends?
3. Does activity in one ecosystem precede activity in another?
4. Can multi-source signals identify emerging technologies earlier than individual-source signals?
5. Can historical data support near-term forecasts of technology momentum?
6. How accurate and reliable are those forecasts under time-based backtesting?

---

# 16. Research Integrity Principles

The following principles will guide the next stages:

- Raw source data remains unchanged.
- Transformations are created in separate processed-data layers.
- Source provenance is retained.
- Different source coverage periods are explicitly documented.
- Missing historical coverage is never treated as zero activity.
- Forecasts are evaluated against historical observations.
- Random train/test splitting is avoided for temporal forecasting.
- Correlation is not presented as causation.
- A technology is not labelled “emerging” solely because its absolute volume is high.
- Multi-source agreement is evaluated rather than assumed.
- Negative or weak findings remain valid research findings.

---

# 17. Current Milestone

## DATA FOUNDATION COMPLETE

The project has progressed through:

```text
Research idea
     ↓
Data-source selection
     ↓
Collection pipelines
     ↓
Large-scale raw data acquisition
     ↓
Storage restructuring
     ↓
Source validation
     ↓
Validated research data foundation
```

### Next milestone

> **Unified AI Ecosystem Research Dataset**

This dataset will become the foundation for statistical analysis, emerging-technology detection, cross-platform signal analysis, and forecasting experiments.

---

# 18. Final Status

```text
GitHub              ✅ COMPLETE
Stack Overflow      ✅ COMPLETE
Hugging Face        ✅ COMPLETE
Reddit              ❌ EXCLUDED
Storage migration   ✅ COMPLETE
Validation          ✅ COMPLETE
Raw data foundation ✅ COMPLETE

NEXT:
Cross-source integration and research analysis
```

