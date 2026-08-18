# Data Source Evaluation

**Project:** AI Evolution Intelligence

**Date:** 18 August 2026

## 1. Objective

Multiple online technology ecosystems were evaluated as potential data sources for the AI Evolution Intelligence platform.

The objective was to identify sources capable of providing reliable and reproducible historical data for analysing AI technology evolution between 1 January 2023 and 31 August 2026.

## 2. Source Evaluation

| Source | Primary Role | Historical Access | Decision |
|---|---|---|---|
| Stack Overflow | Developer demand | Strong | Primary |
| GitHub | Open-source ecosystem | Strong | Primary |
| Hugging Face | Model ecosystem | Limited historical querying | Complementary |
| Reddit | Community discussion | Restricted / unsuitable for reproducible historical collection | Excluded |

## 3. Reddit Evaluation

Reddit was evaluated as a potential community-discussion data source.

An unauthenticated Reddit JSON endpoint was tested during the feasibility assessment.

The request returned HTTP 403.

Further investigation showed that current Reddit API access is subject to stricter authentication and platform-access requirements. In addition, the normal API approach does not provide a sufficiently straightforward and reproducible mechanism for arbitrary historical post retrieval across the complete study period.

Therefore Reddit was excluded from the primary longitudinal dataset.

This decision was made to preserve reproducibility, data provenance, and methodological reliability.

## 4. Final Data Source Strategy

The primary longitudinal dataset will use:

1. Stack Overflow
2. GitHub

Hugging Face will be investigated as a complementary model-ecosystem source.

Reddit will not be used in the primary longitudinal dataset.

## 5. Study Period

The primary longitudinal study period is:

**1 January 2023 – 31 August 2026**

The period will be applied consistently to Stack Overflow and GitHub historical collection.