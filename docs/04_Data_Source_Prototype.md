# Data Source Prototyping and Historical Data Collection

**Project:** Machine Learning-Based AI Technology Evolution Analysis and Future Trend Prediction Platform

**Document Version:** 1.0

**Date:** 18 August 2026

**Status:** Initial Prototyping

## 1. M4 Objectives

## 2. Prototype Strategy

## 3. Stack Overflow Prototype

## 4. GitHub Prototype

## 5. AI Model and Release Prototype

## 6. Benchmark Prototype

## 7. Hugging Face Prototype

## 8. Cross-Source Entity Testing

## 9. Historical Data Collection

## 10. Data Quality Findings

## 11. Prototype Results

## 12. M4 Decisions

## 1. M4 Objectives

The purpose of this milestone is to validate the feasibility of the selected data sources using small-scale real-data prototypes before implementing the complete production data collection system.

The main objectives are:

1. Test access to the selected data sources.
2. Retrieve representative sample records.
3. Inspect the actual structure and quality of the returned data.
4. Identify fields that are useful for the project.
5. Identify fields that are unavailable or unreliable.
6. Test historical data retrieval.
7. Test pagination and API limitations.
8. Identify potential data-cleaning requirements.
9. Validate the proposed normalised data entities.
10. Refine the database schema based on real data.
11. Determine realistic historical coverage.
12. Establish the minimum viable dataset required for machine learning.

## 2. Prototype Strategy

The project will use a staged prototyping approach rather than immediately performing large-scale data collection.

Each source will initially be tested using a small sample.

The prototype process will be:

```text
Source
  ↓
Small API / Data Request
  ↓
Raw Sample
  ↓
Inspect Structure
  ↓
Identify Useful Fields
  ↓
Validate Data Quality
  ↓
Test Historical Retrieval
  ↓
Update Data Model

### 3.4 Prototype Result

The Stack Overflow API prototype successfully returned HTTP 200 responses and structured question records.

A one-month historical test covering January 2024 returned 97 records using a page size of 100. This demonstrates that the selected API query can retrieve a meaningful historical dataset for AI-related developer activity analysis.

The returned records contained useful fields including question ID, title, tags, creation date, score, answer count, and view count.

The dataset also demonstrated substantial technology diversity. In addition to OpenAI-related tags, records contained technologies and concepts including LangChain, RAG, Hugging Face, AutoGen, Azure OpenAI, GPT-3, GPT-4, function calling, image generation, text-to-speech, vector search, Pinecone, and semantic search.

### 3.5 Data Quality Observations

Stack Overflow tags provide a useful structured representation of technologies associated with developer questions.

The combination of tags and question titles provides two potential sources for technology identification.

Engagement indicators such as views, answers, and scores provide additional measures of developer activity.

The prototype also demonstrated that technology relationships can be derived from co-occurring tags. For example, OpenAI-related questions may also contain LangChain, RAG, tool-related, or vector-search tags.

These relationships may later be used to construct technology co-occurrence networks and technology evolution features.

### 3.6 Historical Retrieval Test

Historical retrieval was successfully tested for January 2024.

The test returned 97 records within the selected date range, confirming that historical Stack Overflow data can be retrieved for time-series analysis.

Additional historical periods will be tested before full collection to determine the appropriate time range and total data volume.

### 3.7 Pagination Test

A page size of 100 was tested successfully.

The January 2024 query returned fewer than 100 records, meaning that the selected query did not require a second page for this specific period.

However, production collection will implement pagination because other technologies, date ranges, or queries may return more than one page.

### 3.8 Prototype Decision

**Decision: APPROVED FOR LARGE-SCALE COLLECTION**

Stack Overflow is approved as a core data source.

The production collector must support:

- Historical date ranges.
- Pagination.
- Duplicate detection.
- Raw-data preservation.
- Rate-limit handling.
- Collection timestamps.
- Incremental collection.
- Technology extraction.
- Source identification.

## 4. GitHub Prototype

### 4.1 Prototype Objective

The GitHub prototype was created to evaluate the accessibility, structure, and usefulness of GitHub repository metadata for analysing AI open-source ecosystem evolution.

The initial prototype used the GitHub repository search API with the search term `artificial intelligence` and retrieved the 10 highest-starred matching repositories.

### 4.2 Prototype Result

The prototype successfully returned an HTTP 200 response and 10 repository records.

The API reported 107,207 matching repositories for the broad search query.

The returned records contained useful metadata including:

- Repository name
- Repository owner
- Description
- Star count
- Fork count
- Open issue count
- Primary programming language
- Topics
- Creation date
- Last update date
- Repository URL

### 4.3 Data Quality Observations

The prototype demonstrated that GitHub provides rich structured metadata that can potentially support open-source ecosystem analysis.

However, the broad `artificial intelligence` search produced repositories with substantially different purposes.

Examples included educational roadmaps, curated resource lists, programming projects, classical AI implementations, generative AI resources, and AI applications.

Therefore, GitHub search results cannot be treated as a direct representation of modern AI technology activity.

A relevance filtering and technology classification process will be required before repository records are included in technology-level analysis.

### 4.4 Technology Identification

Repository topics and descriptions appear to provide useful signals for identifying technologies.

Potential classification inputs include:

- Repository name
- Description
- Topics
- Programming language
- README content
- Other repository metadata where appropriate

Natural language processing and rule-based classification may later be investigated for mapping repositories to AI technologies.

### 4.5 Popularity and Activity Indicators

The prototype confirmed the availability of several potential ecosystem indicators:

- Stars
- Forks
- Open issues
- Repository age
- Last update date
- Last push date
- Programming language
- Topics

These indicators may be transformed into technology-level measures such as repository count, popularity, activity, and growth.

### 4.6 Important Limitation

Raw star counts cannot be treated as direct historical growth measurements.

A repository may have accumulated a large number of stars over several years, while a newer repository may have fewer stars but a substantially higher growth rate.

Therefore, the project will investigate historical activity or alternative growth indicators before using GitHub data for time-series prediction.

### 4.7 Rate Limit Observation

The prototype returned a low remaining search/API quota during testing.

This demonstrates that GitHub API rate limits must be considered in the production architecture.

The final collector should minimise repeated searches, use caching, implement controlled collection, and investigate authenticated API access where appropriate.

### 4.8 Prototype Decision

**Decision: APPROVED WITH RESTRICTIONS**

GitHub is approved as a core data source for open-source ecosystem analysis.

However, the project will not treat broad keyword search results as direct technology measurements.

Before large-scale collection, the project will implement:

- Controlled technology queries.
- Repository relevance filtering.
- Technology classification.
- Duplicate detection.
- Pagination.
- Rate-limit handling.
- Historical activity investigation.
- Raw-data preservation.

### 4.9 Technology-Specific Search Test

A second GitHub prototype was performed using the search term `RAG`.

The query returned 10 repositories and reported a large number of matching repositories.

The results were substantially more relevant to modern AI technologies than the broad `artificial intelligence` query.

The returned repositories included Dify, Open WebUI, LangChain, RAGFlow, and other projects associated with RAG, LLMs, AI agents, MCP, knowledge graphs, and related technologies.

### 4.10 Technology Relationship Observation

The prototype demonstrated that individual repositories can contain multiple AI technology signals simultaneously.

For example, repositories may contain combinations of:

- RAG
- AI agents
- LLMs
- MCP
- LangChain
- OpenAI
- Claude
- Gemini
- Knowledge graphs
- Prompt engineering

This indicates that GitHub data may support technology co-occurrence and relationship analysis in addition to simple repository counting.

### 4.11 Repository Relevance Problem

The technology-specific search also demonstrated that a repository containing a technology keyword or topic is not necessarily primarily an implementation of that technology.

Repositories may represent:

- Core implementations
- Frameworks
- Applications
- Research projects
- Educational resources
- Tutorials
- Curated lists
- Supporting tools

Therefore, repository relevance and role classification will be required before calculating technology-level ecosystem indicators.

### 4.12 Proposed GitHub Classification

The project will investigate classifying repositories into categories such as:

- Core implementation
- Framework
- Application
- Research implementation
- Educational resource
- Tutorial
- Curated resource
- Other

Repository classification may use:

- Repository name
- Description
- Topics
- README content
- Repository metadata
- NLP-based classification

### 4.13 Prototype Findings

The GitHub prototype demonstrates that the platform provides potentially valuable signals for analysing AI technology ecosystems.

However, raw search-result counts cannot directly represent technology adoption or ecosystem size.

The project will therefore focus on validated repository sets and derived measures such as:

- Repository growth
- Star growth
- Fork growth
- Development activity
- Organisation participation
- Technology co-occurrence
- Repository role distribution

### 4.14 Updated Prototype Decision

**Decision: APPROVED WITH CONTROLLED TECHNOLOGY DISCOVERY**

GitHub remains a core data source.

However, the production pipeline will not rely on unrestricted keyword counts.

Technology-specific discovery, repository relevance filtering, classification, deduplication, and technology aggregation will be required before GitHub data is used for AI evolution analysis.### 4.9 Technology-Specific Search Test

A second GitHub prototype was performed using the search term `RAG`.

The query returned 10 repositories and reported a large number of matching repositories.

The results were substantially more relevant to modern AI technologies than the broad `artificial intelligence` query.

The returned repositories included Dify, Open WebUI, LangChain, RAGFlow, and other projects associated with RAG, LLMs, AI agents, MCP, knowledge graphs, and related technologies.

### 4.10 Technology Relationship Observation

The prototype demonstrated that individual repositories can contain multiple AI technology signals simultaneously.

For example, repositories may contain combinations of:

- RAG
- AI agents
- LLMs
- MCP
- LangChain
- OpenAI
- Claude
- Gemini
- Knowledge graphs
- Prompt engineering

This indicates that GitHub data may support technology co-occurrence and relationship analysis in addition to simple repository counting.

### 4.11 Repository Relevance Problem

The technology-specific search also demonstrated that a repository containing a technology keyword or topic is not necessarily primarily an implementation of that technology.

Repositories may represent:

- Core implementations
- Frameworks
- Applications
- Research projects
- Educational resources
- Tutorials
- Curated lists
- Supporting tools

Therefore, repository relevance and role classification will be required before calculating technology-level ecosystem indicators.

### 4.12 Proposed GitHub Classification

The project will investigate classifying repositories into categories such as:

- Core implementation
- Framework
- Application
- Research implementation
- Educational resource
- Tutorial
- Curated resource
- Other

Repository classification may use:

- Repository name
- Description
- Topics
- README content
- Repository metadata
- NLP-based classification

### 4.13 Prototype Findings

The GitHub prototype demonstrates that the platform provides potentially valuable signals for analysing AI technology ecosystems.

However, raw search-result counts cannot directly represent technology adoption or ecosystem size.

The project will therefore focus on validated repository sets and derived measures such as:

- Repository growth
- Star growth
- Fork growth
- Development activity
- Organisation participation
- Technology co-occurrence
- Repository role distribution

### 4.14 Updated Prototype Decision

**Decision: APPROVED WITH CONTROLLED TECHNOLOGY DISCOVERY**

GitHub remains a core data source.

However, the production pipeline will not rely on unrestricted keyword counts.

Technology-specific discovery, repository relevance filtering, classification, deduplication, and technology aggregation will be required before GitHub data is used for AI evolution analysis.

### 4.15 Historical Star Activity Test

A historical star-activity test was performed using the GitHub stargazers endpoint for the Dify repository.

The request returned HTTP 401 Unauthorized.

The current GitHub API documentation indicates that, since July 2026, access to stargazer listing endpoints is restricted to repository administrators and collaborators.

Therefore, the project will not depend on retrieving individual historical stargazer records for arbitrary public repositories.

### 4.16 Historical Star Data Decision

Historical individual star events will be excluded from the core GitHub data collection strategy.

Current repository star counts may still be used as a snapshot popularity indicator, but they will not be interpreted as historical growth measurements.

This prevents the project from making unsupported assumptions about historical repository adoption.

### 4.17 Revised GitHub Activity Strategy

The project will investigate alternative GitHub activity indicators that are accessible for public repositories, including:

- Repository creation dates
- Repository update dates
- Push activity
- Release activity
- Issue activity
- Pull request activity where appropriate
- Current star count
- Current fork count
- Repository counts
- Technology co-occurrence
- Organisation participation

These indicators will be evaluated individually before being incorporated into the analytical dataset.

### 4.18 Final GitHub Prototype Decision

**Decision: APPROVED AS A CORE SOURCE**

GitHub remains a core data source for analysing the open-source AI ecosystem.

However, the project will not rely on unrestricted historical star-event data.

GitHub will primarily provide:

- Open-source repository ecosystem size
- Repository development activity
- Technology relationships
- Current popularity indicators
- Release activity
- Repository lifecycle information

## 5. AI Model Ecosystem Prototype

### 5.1 Prototype Objective

The AI model ecosystem prototype will investigate whether publicly available model repository information can provide reliable signals for analysing the evolution of AI models and technologies.

The prototype will initially use the Hugging Face Hub as a structured model ecosystem source.

The main objectives are:

- Identify available AI models.
- Retrieve model metadata.
- Identify model creators and organisations.
- Identify model tasks and capabilities.
- Determine model creation dates.
- Determine model update dates.
- Investigate model popularity indicators.
- Identify model technology tags.
- Investigate the feasibility of constructing a historical model ecosystem dataset.

### 5.8 Historical Model Creation Test

A second Hugging Face prototype was performed using `created_at` as the sorting field.

The API successfully returned models ordered by creation date. The test returned models created on 16, 17, and 18 August 2026.

This confirms that model repository creation dates can be used to investigate the historical growth of the model ecosystem.

### 5.9 Model Search Relevance Problem

The historical test also demonstrated that a search term such as `llm` does not produce a clean dataset containing only general-purpose large language models.

Returned records included language models, specialised models, tokenization-related models, research models, converted models, and other repositories containing the `llm` term.

Therefore, search results will require technology classification and relevance filtering before being used in analytical calculations.

### 5.10 Model Lineage Observation

Hugging Face model metadata may contain base-model and fine-tuning relationships.

These relationships provide a potential mechanism for identifying model lineage.

A model lineage structure may allow the project to represent relationships such as:

Base Model → Fine-Tuned Model → Domain-Specific Model

Model lineage will be investigated as a potential AI evolution feature.

### 5.11 Historical Data Decision

Model creation dates are approved as a historical ecosystem indicator.

The project will investigate model creation counts by month or other appropriate time periods.

However, model creation count will not automatically be interpreted as technology adoption or model quality.

Additional indicators such as downloads, likes, capabilities, model lineage, and evaluation information will be considered separately.

### 5.12 Updated Prototype Decision

**Decision: APPROVED AS A CORE SOURCE**

Hugging Face is approved as a core source for AI model ecosystem analysis.

The production pipeline will require:

- Controlled technology discovery.
- Model relevance filtering.
- Technology classification.
- Model-family identification.
- Model lineage extraction where available.
- Creation-date processing.
- Adoption indicators.
- Duplicate detection.
- Raw-data preservation.