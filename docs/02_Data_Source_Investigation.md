# Data Source Investigation

**Project:** Machine Learning-Based AI Technology Evolution Analysis and Future Trend Prediction Platform

**Document Version:** 1.0

**Date:** 16 August 2026

**Status:** Initial Data Source Investigation

## 3. Stack Overflow

### 3.1 Overview

Stack Overflow is being considered as one of the primary data sources for the project because it contains a large volume of developer-generated technical questions and discussions. The platform can provide useful signals about developer interest, technology usage, technical problems, and changes in the adoption of AI-related technologies.

The Stack Exchange API provides programmatic access to Stack Overflow data and supports querying questions using parameters such as tags, dates, titles, body content, scores, and other question properties.

### 3.2 Relevance to the Project

Stack Overflow can provide a developer-focused signal for analysing AI technology evolution.

The project will not treat Stack Overflow activity as a direct measurement of AI model capability. Instead, it will be used as an indicator of developer activity and technology adoption.

For example, an increasing number of questions associated with an AI technology over time may indicate increasing developer interest or usage. However, this signal will need to be interpreted together with other data sources because discussion volume does not necessarily represent technical superiority or actual market adoption.

### 3.3 Available Data

The Stack Exchange API provides question data containing fields that are potentially useful for the project, including:

- Question ID
- Title
- Body
- Tags
- Creation date
- Last activity date
- Score
- View count
- Answer count
- Accepted answer information
- Question status
- Post link
- Owner information where available

The API documentation also provides search and filtering capabilities that can be used to retrieve questions based on tags, text, dates, answers, scores, and other criteria.

### 3.4 Relevant API Endpoints

The following endpoints are considered particularly relevant:

#### Questions

The `/questions` endpoint can be used to retrieve questions and supports filtering and sorting by relevant fields. Question data can include creation dates, tags, scores, views, answer counts, and accepted-answer information.

#### Advanced Search

The `/search/advanced` endpoint can search questions using criteria such as keywords, tags, title text, body text, minimum answers, and date ranges.

#### Tags

The `/tags` endpoint provides information about tags on the site, including tag counts and activity information.

#### Questions by ID

The `/questions/{ids}` endpoint can be used to retrieve updated information for known questions. This may be useful when maintaining a local dataset and periodically updating previously collected records.

### 3.5 Historical Data Potential

The API supports date-based filtering using parameters such as `fromdate` and `todate`. This makes it possible to construct historical datasets and analyse AI-related activity over defined time periods.

Historical records can potentially be grouped into monthly or weekly periods to create time-series indicators.

For example:

| Period | AI Technology | Questions | Answers | Average Score |
|---|---|---:|---:|---:|
| 2023-01 | Technology A | — | — | — |
| 2023-02 | Technology A | — | — | — |
| 2023-03 | Technology A | — | — | — |
| ... | ... | ... | ... | ... |
| 2026-08 | Technology A | — | — | — |

Actual values will be determined during the data collection stage.

### 3.6 Potential Features

The following features may be derived from Stack Overflow data:

- Number of questions per technology
- Question growth rate
- Number of answers
- Average answers per question
- Average question score
- Average view count
- Accepted-answer rate
- Number of active questions
- Number of unique technologies appearing together
- Technology co-occurrence
- Topic frequency
- Sentiment indicators where applicable
- Monthly and weekly activity
- Changes in activity over time

These features can later contribute to the AI Evolution Index and machine learning models.

### 3.7 Technology Identification

Stack Overflow tags will be an important starting point for identifying technologies because they provide structured information about the technologies associated with questions.

However, tags alone will not be sufficient.

Some AI technologies or models may appear in question titles or bodies without having a dedicated tag. Therefore, natural language processing may later be used to identify additional AI-related technologies and concepts from textual content.

The project will therefore investigate a combination of:

1. Structured tags
2. Titles
3. Question bodies
4. NLP-based entity and keyword extraction

### 3.8 Data Collection Strategy

The initial strategy will be to identify a controlled list of AI-related technologies and model names and use the Stack Exchange API to retrieve relevant historical questions.

Potential search targets may include:

- AI model names
- AI technology names
- AI frameworks
- AI-related programming technologies
- AI capability terms

The final list will be determined after further investigation and exploratory analysis.

Data will be collected in manageable date ranges and stored locally so that the project does not need to repeatedly request the same historical records.

### 3.9 API and Collection Considerations

The Stack Exchange API provides common response metadata including `has_more`, `quota_max`, `quota_remaining`, and `backoff`.

If a `backoff` value is returned, the application is required to wait for the specified number of seconds before making another request to the affected method.

The collection system will therefore need to:

- Monitor API quota information.
- Respect API backoff instructions.
- Implement pagination.
- Store collected records locally.
- Avoid unnecessary repeated requests.
- Support incremental collection.
- Log collection errors and failed requests.

### 3.10 Limitations

Stack Overflow data has several limitations for this project:

- Developer activity does not directly represent AI model capability.
- Not all AI technologies are equally represented through Stack Overflow tags.
- Some newer technologies may have limited historical data.
- Question activity may be influenced by changes in Stack Overflow usage patterns.
- A high number of questions does not necessarily mean that a technology is technically superior.
- Historical API collection may require many requests depending on the selected technologies and time period.
- Textual discussions may contain ambiguous references to AI models or technologies.

### 3.11 Proposed Role in the System

Stack Overflow will initially be classified as a:

**Primary Developer Ecosystem Signal**

Its main purpose will be to provide evidence about:

- Developer interest
- Developer activity
- Technology adoption signals
- Technical problems
- Technology relationships
- Emerging developer trends

It will not be used as a standalone measure of AI capability or future success.

### 3.12 Initial Assessment

**Status: Suitable — Primary Candidate**

Stack Overflow provides structured, queryable, date-based data that is highly relevant to the project's objective of analysing AI technology evolution.

Its strongest value is its developer-focused signal. However, it should be combined with other sources because developer activity alone cannot fully represent the evolution of the broader AI ecosystem.

## 4. Reddit

### 4.1 Overview

Reddit is being investigated as a potential source of community-level information about AI technologies, models, tools, and emerging trends. AI-focused subreddits contain discussions about model releases, technical experiences, new technologies, problems, use cases, comparisons, and community opinions.

Reddit could therefore provide a community-oriented signal that complements the developer-focused information obtained from Stack Overflow.

However, Reddit's current data-access policies and platform changes introduce additional constraints. Therefore, Reddit will not be treated as a guaranteed primary data source until its access requirements and suitability for the project have been confirmed.

### 4.2 Relevance to the Project

Reddit may provide a useful signal for analysing the broader community interest and discussion surrounding AI technologies.

Unlike Stack Overflow, which is primarily focused on technical questions and developer problem solving, Reddit can contain broader discussions including:

- Experiences with AI models
- Discussions about new model releases
- AI tool comparisons
- Opinions and feedback
- Emerging technology discussions
- New use cases
- Community concerns
- Discussions about open-source AI
- Discussions about AI agents and emerging technologies

This makes Reddit potentially useful for identifying changes in community interest and emerging trends.

Reddit activity will not be treated as a direct measurement of technical capability or objective AI performance.

### 4.3 Potential Data

Subject to approved access and applicable usage conditions, the project may investigate data such as:

- Post ID
- Subreddit
- Post title
- Post body
- Creation date
- Score
- Comment count
- Post URL
- Post type
- Comments
- Discussion text
- Relevant metadata

The exact fields available will depend on the approved Reddit access method.

### 4.4 Potential AI Communities

Potential communities for investigation may include AI-focused subreddits such as:

- r/artificial
- r/MachineLearning
- r/OpenAI
- r/ClaudeAI
- r/GeminiAI
- r/LocalLLaMA
- r/ChatGPT
- Other relevant communities identified during the research stage

The final selection will depend on relevance, data accessibility, historical coverage, community activity, and applicable Reddit policies.

### 4.5 Potential Features

If sufficient data can be obtained, the following features may be derived:

- Number of posts mentioning an AI technology
- Growth in discussion volume
- Number of comments
- Average post score
- Engagement rate
- Sentiment distribution
- Topic frequency
- Technology co-occurrence
- Model comparisons
- Community-specific activity
- Emerging technology mentions
- Changes in discussion patterns over time

These features could contribute to the analysis of AI technology evolution and the AI Evolution Index.

### 4.6 NLP Opportunities

Reddit's textual discussions may provide useful information for natural language processing.

Potential NLP tasks include:

- AI model identification
- AI technology identification
- Topic detection
- Sentiment analysis
- Keyword extraction
- Technology relationship extraction
- Emerging-topic detection
- Community-level trend analysis

For example, discussions containing terms such as "AI agents", "MCP", "computer use", or "reasoning models" could be aggregated over time to identify accelerating interest in emerging technologies.

### 4.7 Historical Data Potential

Historical analysis is potentially valuable because Reddit discussions can provide time-based signals of changing community interest.

The project would ideally construct time-series indicators such as:

| Period | Technology | Posts | Comments | Average Score | Sentiment |
|---|---|---:|---:|---:|---:|
| 2023-01 | Technology A | — | — | — | — |
| 2023-02 | Technology A | — | — | — | — |
| 2023-03 | Technology A | — | — | — | — |
| ... | ... | ... | ... | ... | ... |
| 2026-08 | Technology A | — | — | — | — |

The actual historical coverage will depend on the approved access method and available data.

### 4.8 Access and Policy Considerations

Reddit currently provides a Data API for approved developers and requires OAuth authentication for API access.

Reddit's official documentation states that access is subject to its Developer Terms, Data API Terms, and Responsible Builder Policy.

Reddit also states that academic research using Reddit data must use the Reddit for Researchers program rather than ordinary developer tools or unauthorised third-party methods.

The project must therefore investigate the appropriate research-access route before collecting Reddit data.

The project will not bypass Reddit's access controls, scrape Reddit without authorization, or use unauthorised methods to obtain Reddit data.

### 4.9 Current Platform Changes

Reddit announced in August 2026 that it intends to gradually restrict new public API requests and transition third-party applications toward its Developer Platform.

Reddit has stated that this transition is gradual and that limited public API access will continue during the transition period. However, the future availability of particular access methods cannot be assumed.

Because this project is intended to remain maintainable over time, the system architecture will avoid making Reddit a single point of failure.

### 4.10 Limitations

Reddit has several limitations for this project:

- Access to data may require approval.
- Academic research access may require participation in Reddit's research program.
- API access is subject to authentication and rate limits.
- Reddit's data-access policies are changing.
- Historical data availability may be limited.
- Community activity does not represent the entire AI ecosystem.
- Reddit discussions can contain noise, misinformation, duplicates, jokes, and subjective opinions.
- High discussion volume does not necessarily indicate technical superiority.
- Sentiment analysis may be difficult because Reddit discussions can contain sarcasm, slang, and context-dependent language.
- Different subreddits may represent different communities and biases.
- The project cannot assume complete coverage of Reddit discussions.

### 4.11 Proposed Role in the System

Reddit will initially be classified as a:

**Secondary Community Ecosystem Signal**

Its potential role is to provide information about:

- Community interest
- User experiences
- Emerging discussions
- AI technology awareness
- Technology comparisons
- Sentiment
- Community-level trends

Reddit will not be used as the sole source for determining AI technology evolution.

### 4.12 Fallback Strategy

Because Reddit access may be restricted or change during the project, the system will be designed so that Reddit can be added or removed without changing the core machine learning architecture.

The core system will therefore rely on multiple independent data signals.

If approved Reddit research access is obtained, Reddit data can be incorporated as an additional community signal.

If suitable access cannot be obtained, the project will continue using other approved and reliable data sources.

### 4.13 Initial Assessment

**Status: Potentially Suitable — Conditional**

Reddit provides potentially valuable community-level information for analysing AI technology evolution. However, its current access requirements and changing API strategy introduce significant uncertainty.

Therefore, Reddit will be treated as a valuable secondary source rather than a mandatory core dependency until appropriate research access and historical data availability have been confirmed.

## 5. GitHub

### 5.1 Overview

GitHub is being investigated as a potential primary data source for analysing the open-source development and ecosystem growth of AI technologies.

GitHub contains a large ecosystem of open-source AI models, frameworks, libraries, applications, tools, and supporting technologies. Repository activity can therefore provide a useful signal for measuring how technologies develop and gain adoption within the open-source ecosystem.

The GitHub REST API provides programmatic access to public repository information and other GitHub resources. GitHub also provides a GraphQL API for querying structured GitHub data.

### 5.2 Relevance to the Project

GitHub provides a different type of signal from Stack Overflow and Reddit.

Stack Overflow primarily represents developer questions and technical discussions, while Reddit represents broader community discussions. GitHub can provide evidence of actual open-source development and ecosystem activity.

This makes GitHub particularly useful for analysing:

- Open-source AI technology adoption
- Development activity
- Project growth
- Community interest
- Technology ecosystem development
- Relationships between AI technologies
- Development of AI frameworks and tools

GitHub activity will not be treated as a direct measurement of AI model capability. Instead, it will represent an open-source ecosystem signal.

### 5.3 Potential Data

Public repository information may provide fields such as:

- Repository ID
- Repository name
- Full repository name
- Owner or organisation
- Description
- Topics
- Programming language
- Creation date
- Last update date
- Last push date
- Star count
- Fork count
- Open issue count
- Repository size
- Archive status
- License information
- Repository URL

Additional repository activity data may be investigated where it provides useful information for measuring development.

### 5.4 Potential AI Repository Identification

The project will need to identify repositories associated with selected AI models and technologies.

Potential identification methods include:

- Repository names
- Repository descriptions
- Repository topics
- Organisation ownership
- Technology keywords
- README content
- Programming languages
- Dependency information where appropriate

For example, repositories associated with technologies such as RAG, AI agents, MCP, LLMs, model serving, and AI frameworks may be identified and grouped for analysis.

The final repository-selection methodology will be defined during the data collection design stage.

### 5.5 Potential Features

The following features may be derived from GitHub data:

- Number of relevant repositories
- Repository creation rate
- Star count
- Star growth
- Fork count
- Fork growth
- Open issue count
- Contributor count where available
- Commit activity where accessible
- Release activity
- Repository update frequency
- Number of related repositories
- Technology co-occurrence
- Repository survival or archival status
- Open-source ecosystem growth

These indicators may contribute to the AI Evolution Index.

### 5.6 Technology Growth Analysis

GitHub can be used to construct time-based indicators for AI technologies.

For example:

| Period | Technology | Repositories | Stars | Forks | Activity |
|---|---|---:|---:|---:|---:|
| 2023-01 | Technology A | — | — | — | — |
| 2023-06 | Technology A | — | — | — | — |
| 2024-01 | Technology A | — | — | — | — |
| 2025-01 | Technology A | — | — | — | — |
| 2026-08 | Technology A | — | — | — | — |

Actual values will be determined during the data collection stage.

Changes in these indicators may provide evidence of increasing or decreasing open-source ecosystem activity.

### 5.7 Repository-Level Versus Technology-Level Analysis

The project will distinguish between individual repositories and broader technologies.

For example:

A single repository may represent a specific implementation of an AI technology, while hundreds or thousands of repositories may collectively represent the broader ecosystem around that technology.

Therefore, the project may aggregate repository-level information into technology-level indicators.

For example:

Technology: AI Agents

Possible aggregated indicators:

- Number of relevant repositories
- Total stars
- Total forks
- Repository creation rate
- Average repository growth
- Development activity
- Number of related technologies

This aggregated representation can then be used for technology evolution analysis.

### 5.8 Historical Data Considerations

GitHub provides repository metadata containing creation, update, and push timestamps. However, not every current repository metric automatically provides a complete historical time series.

For example, a repository's current star count represents its current accumulated stars rather than a complete historical record of its daily or monthly star growth.

Therefore, the project will distinguish between:

1. Historical information directly available through GitHub.
2. Historical activity that can be reconstructed from available endpoints or datasets.
3. Current repository-level indicators collected periodically by the proposed system.

The system will not assume that all GitHub metrics have unlimited historical coverage.

### 5.9 Star Data Considerations

Stars can be used as an approximate indicator of repository interest.

However, stars should not be treated as a direct measure of technology adoption or quality.

GitHub documentation describes stars as an approximate indication of interest in a repository.

Recent GitHub API changes also restrict access to detailed stargazer listings for many users, meaning the project should not depend on retrieving every individual star event.

Therefore, repository-level star counts and other available indicators will be prioritised over attempting to reconstruct complete individual star histories.

### 5.10 API Access

GitHub provides a REST API and a GraphQL API.

Some public resources can be accessed without authentication, while authentication provides higher rate limits and access to additional capabilities.

The project will investigate the use of an authenticated GitHub API client for reliable data collection.

API credentials will be stored securely and will not be committed to the project repository.

### 5.11 API Rate Limits

GitHub applies rate limits to API requests. Different categories of API operations may have different limits, including search and GraphQL operations.

The data collection system will therefore need to:

- Monitor API rate-limit information.
- Avoid unnecessary requests.
- Use pagination correctly.
- Cache previously collected data.
- Use authenticated requests where appropriate.
- Implement retry and backoff behaviour.
- Avoid excessive concurrent requests.
- Store collected information locally.

GitHub recommends authenticated requests, avoiding unnecessary polling, and handling rate-limit responses appropriately.

### 5.12 Potential Collection Strategy

The initial strategy will be to identify a controlled set of AI technologies and then identify relevant public repositories associated with each technology.

The system may then periodically collect repository metadata and activity indicators.

A possible process is:

**Technology List → Repository Discovery → Repository Filtering → Metadata Collection → Activity Collection → Technology Aggregation → Time-Series Indicators**

The exact collection frequency will be determined after the initial data-access tests.

### 5.13 NLP Opportunities

GitHub repository descriptions, topics, and README content may provide additional textual information for NLP.

Potential applications include:

- Technology identification
- Topic extraction
- Technology relationship detection
- AI capability identification
- Repository classification
- Emerging technology detection

However, repository text will only be processed where access and usage conditions permit.

### 5.14 Limitations

GitHub data has several limitations:

- Repository activity does not directly represent technical capability.
- Star counts are an imperfect measure of adoption or interest.
- Some repositories may be inactive but still have large historical star counts.
- Repository naming and descriptions may be ambiguous.
- A technology may be implemented across many unrelated repositories.
- Current repository metrics do not necessarily provide complete historical time series.
- API rate limits restrict large-scale data collection.
- Search results may not provide complete coverage of every relevant repository.
- GitHub represents the open-source ecosystem and therefore does not represent proprietary AI development.
- Some repositories may contain duplicated, forked, experimental, or low-quality implementations.

### 5.15 Proposed Role in the System

GitHub will initially be classified as a:

**Primary Open-Source Ecosystem Signal**

Its main purpose will be to provide evidence about:

- Open-source adoption
- Technology ecosystem growth
- Development activity
- AI framework growth
- Technology relationships
- Open-source community interest

GitHub will complement Stack Overflow's developer signal and any approved community data obtained from Reddit.

### 5.16 Initial Assessment

**Status: Strong Candidate — Primary Source**

GitHub provides a valuable and relatively structured source of information for analysing the open-source evolution of AI technologies.

Its strongest contribution to the project is its ability to provide an ecosystem-development signal that is different from community discussion and developer-question activity.

However, historical time-series limitations mean that the project will need to carefully design how GitHub data is collected and aggregated.

GitHub will therefore be considered a strong candidate for inclusion in the core data architecture.

## 6. AI Model and Technology Release Data

### 6.1 Overview

AI model and technology release information will be investigated as a core data source for analysing the direct evolution of artificial intelligence models and technologies.

Unlike community and open-source ecosystem data, release information provides evidence of how AI systems themselves change over time. This may include new model versions, changes in capabilities, context windows, supported modalities, tool-use functionality, pricing, model availability, and other technical developments.

The project will investigate official documentation, model repositories, release information, and other reliable public sources to construct a structured historical representation of AI model and technology development.

### 6.2 Relevance to the Project

Model and technology release data is essential because the project is intended to analyse the evolution of AI itself rather than only changes in public interest.

For example, an AI model may evolve from:

Text generation
        ↓
Improved coding
        ↓
Longer context
        ↓
Multimodal input
        ↓
Reasoning capabilities
        ↓
Tool use
        ↓
Agentic capabilities

Tracking these changes over time allows the system to analyse the development trajectory of AI models and capabilities.

### 6.3 Potential Model Information

The project may collect structured information such as:

- Model name
- Model family
- Model version
- Organisation or developer
- Release date
- Retirement date where available
- Model type
- Supported modalities
- Context window
- Maximum output information where available
- Tool/function calling support
- Structured output support
- Vision capabilities
- Audio capabilities
- Video capabilities
- Reasoning capabilities
- Agent or computer-use capabilities
- Open-source or proprietary status
- Availability
- Pricing where reliable information is available
- Other documented capabilities

Not every model will provide all fields. Missing information will therefore be handled during data preprocessing.

### 6.4 Model Version Evolution

Where possible, models will be grouped into model families to analyse how their capabilities develop across versions.

For example:

Model Family
    ↓
Version 1
    ↓
Version 2
    ↓
Version 3
    ↓
Version 4

This allows the project to investigate whether model families demonstrate measurable improvements or changes in particular capability areas over time.

### 6.5 Capability Evolution

The project will attempt to represent AI capabilities as structured indicators.

Potential capability categories include:

- Text generation
- Coding
- Reasoning
- Mathematics
- Vision
- Audio
- Video
- Long-context processing
- Retrieval
- Tool calling
- Function calling
- Agentic behaviour
- Computer interaction
- Multimodal interaction

Capabilities may initially be represented using categorical indicators such as:

**0 = Not documented**

**1 = Supported**

Where sufficient historical information exists, more detailed measures may be introduced.

### 6.6 Context Window Evolution

Context window size may be considered as one measurable indicator of model evolution.

For models where reliable information is available, context-window values can be stored historically.

For example:

| Model Version | Release Date | Context Window |
|---|---|---:|
| Version A | — | — |
| Version B | — | — |
| Version C | — | — |

Changes in context capacity may provide one measurable indicator of model development.

However, context window size will not be treated as a direct measure of overall model intelligence.

### 6.7 Multimodal Evolution

The project may track the introduction and development of different modalities.

Potential modalities include:

- Text
- Image
- Audio
- Video
- Structured data
- Computer interaction

This can help identify broader capability shifts within the AI ecosystem.

For example:

Text-only
    ↓
Text + Image
    ↓
Text + Image + Audio
    ↓
Multimodal interaction
    ↓
Computer interaction

### 6.8 Tool and Agent Capability Evolution

The project will investigate the development of tool-use and agent-related capabilities.

Potential indicators include:

- Function calling
- Tool calling
- External API interaction
- Web browsing
- Code execution
- Computer use
- Agent frameworks
- Multi-step task execution

These indicators may be particularly important because agentic AI is expected to be an important area of AI development.

### 6.9 Model Release Events

Major model releases can be represented as events within the AI evolution timeline.

A release event may contain:

- Date
- Model
- Organisation
- New capabilities
- Previous model
- Major changes
- Relevant technologies
- Associated ecosystem activity

These events may later be compared with changes observed in Stack Overflow, GitHub, Reddit, and other sources.

### 6.10 Release-to-Ecosystem Analysis

One of the project's potentially valuable research areas will be investigating whether major model releases are followed by measurable changes in the wider AI ecosystem.

For example:

Model Release
      ↓
Increase in developer questions
      ↓
Increase in GitHub projects
      ↓
Increase in community discussions
      ↓
Emergence of related technologies

This could allow the system to investigate relationships between model development and ecosystem activity.

### 6.11 Potential Features

The following features may be derived from model and release data:

- Number of releases
- Release frequency
- Capability additions
- Capability growth
- Context-window growth
- Number of supported modalities
- Tool-use capability
- Agent capability
- Model family age
- Time between model versions
- Open-source availability
- Pricing changes where reliable data is available
- Number of major development events
- Technology associations

These features may contribute to the AI Evolution Index and machine learning models.

### 6.12 Potential Data Sources

The project will prioritise official and reliable sources wherever possible.

Potential sources include:

- Official AI provider documentation
- Official model documentation
- Official model release announcements
- Official API documentation
- Hugging Face model pages and APIs
- Public model cards
- Public benchmark repositories
- Other reputable structured AI datasets

The project will avoid relying on unofficial summaries when equivalent information is available from a primary source.

### 6.13 Provider Independence

The system will use a standard internal representation so that information from different AI providers can be compared.

For example:

Provider A
Provider B
Provider C

may all provide different terminology and different levels of technical detail.

The system will therefore normalise these differences into common categories such as:

- Model
- Version
- Release date
- Capability
- Modality
- Context
- Tool support
- Agent capability

This will allow cross-model and cross-provider analysis.

### 6.14 Data Quality Considerations

Model information may change after initial publication. Documentation may also differ between providers.

Therefore:

- Source URLs will be recorded where possible.
- Retrieval dates will be stored.
- Model versions will be preserved.
- Historical values will not be overwritten without tracking the change.
- Conflicting information will be investigated.
- Missing values will be explicitly represented.
- Primary sources will be preferred.

### 6.15 Limitations

Model and release data has several limitations:

- Different AI providers disclose different levels of technical information.
- Some capabilities may be difficult to quantify.
- Proprietary model information may not be publicly available.
- Model naming conventions differ between providers.
- Capability descriptions may be marketing-oriented.
- Historical documentation may become unavailable or change over time.
- Release dates do not necessarily indicate the exact date when a model became widely available.
- A model release does not automatically indicate successful adoption.
- Some AI capabilities are qualitative and difficult to represent numerically.
- Comparing models across providers may introduce methodological bias.

### 6.16 Proposed Role in the System

AI model and technology release data will initially be classified as a:

**Primary AI Evolution Signal**

Its primary purpose will be to represent:

- Model development
- Capability evolution
- Technology introduction
- Major release events
- Multimodal development
- Tool and agent capability development
- Changes in model architecture or documented characteristics where available

This source category will provide the foundation for analysing the direct technological evolution of AI.

### 6.17 Initial Assessment

**Status: Essential — Core Source Category**

Model and technology release information is considered essential to the project because it directly represents the development of AI technologies and models.

However, the project will not depend on one provider or one website. A standardised data model will be developed so that information from multiple reliable sources can be integrated into a common AI evolution dataset.

## 7. Benchmark and Evaluation Data

### 7.1 Overview

Benchmark and evaluation data will be investigated as a supporting data source for measuring changes in AI model capabilities over time.

AI benchmarks provide structured evaluations of models across specific tasks or capability areas. When historical results are available, benchmark data can provide quantitative evidence of changes in model performance and can complement model release information and ecosystem activity.

The project will not attempt to create a universal ranking of AI models. Instead, benchmark results will be treated as one of several measurable signals contributing to the analysis of AI capability evolution.

### 7.2 Relevance to the Project

Benchmark data can provide quantitative evidence that complements other sources.

For example:

**Model release data:**

> A model introduces improved reasoning capabilities.

**Benchmark data:**

> The model demonstrates improved performance on selected reasoning evaluations.

**Developer ecosystem data:**

> Developer activity related to the model increases.

Together, these signals provide a broader representation of AI evolution than any individual source.

### 7.3 Potential Benchmark Categories

The project may investigate benchmarks covering areas such as:

- General knowledge
- Reasoning
- Mathematics
- Coding
- Reading comprehension
- Instruction following
- Multilingual capabilities
- Vision
- Multimodal understanding
- Tool use
- Agentic tasks

The final benchmark categories will depend on the availability of reliable historical data.

### 7.4 Potential Data Fields

Where available, benchmark records may contain:

- Model name
- Model family
- Model version
- Benchmark name
- Benchmark category
- Evaluation date
- Score
- Evaluation methodology
- Dataset version
- Number of evaluation examples
- Source or reference
- Additional evaluation metadata

The system will preserve the evaluation date and benchmark identity because scores from different benchmark versions may not be directly comparable.

### 7.5 Historical Capability Analysis

Historical benchmark results may be used to construct time-series indicators for selected capabilities.

For example:

| Model | Date | Capability | Benchmark | Score |
|---|---|---|---|---:|
| Model A | — | Coding | Benchmark X | — |
| Model B | — | Coding | Benchmark X | — |
| Model C | — | Coding | Benchmark X | — |

This may allow the project to investigate how measurable capability performance changes across model generations.

### 7.6 Benchmark Normalisation

Benchmark results cannot automatically be compared directly because different benchmarks may use different:

- Datasets
- Scoring systems
- Evaluation methodologies
- Test sets
- Versions
- Sampling methods
- Evaluation conditions

Therefore, benchmark data will require careful normalisation.

Where appropriate, the project may:

- Compare models within the same benchmark.
- Preserve benchmark versions.
- Standardise score direction where necessary.
- Separate different evaluation methodologies.
- Avoid combining incompatible scores.
- Record the original score and source information.

The project will avoid creating misleading comparisons between fundamentally different evaluation systems.

### 7.7 Capability-Level Aggregation

Where sufficient compatible benchmark data exists, benchmark results may be aggregated at the capability level.

For example:

**Coding Capability**

- Benchmark A
- Benchmark B
- Benchmark C

could provide several measurements of coding performance.

However, an aggregate capability score will only be created when the underlying measurements are sufficiently comparable.

The project will prioritise transparency over creating a single score from incompatible benchmarks.

### 7.8 Benchmark Evolution Versus Model Evolution

The project will distinguish between:

**Model evolution**

Changes in model architecture, versions, capabilities, modalities, tools, and other documented characteristics.

and:

**Measured capability evolution**

Changes in observed performance on selected evaluation tasks.

This distinction is important because a model may introduce a new capability without having sufficient benchmark evidence to quantify that capability.

### 7.9 Relationship With Other Data Sources

Benchmark data will be analysed together with other signals.

A potential analytical relationship is:

**Model Release**
↓
**New Capability**
↓
**Benchmark Performance**
↓
**Developer Activity**
↓
**Open-Source Activity**
↓
**Community Activity**
↓
**Technology Adoption**

The project may investigate whether these signals show meaningful relationships over time.

### 7.10 Potential Features

Potential benchmark-derived features include:

- Benchmark score
- Score change between model versions
- Relative improvement
- Capability-specific score
- Number of evaluated capabilities
- Benchmark coverage
- Performance growth rate
- Performance stability
- Time between capability improvements

These features may be used as supporting indicators for AI capability evolution.

### 7.11 Limitations

Benchmark data has several important limitations:

- Not all models are evaluated on the same benchmarks.
- Benchmark methodologies can change over time.
- Some benchmark results are self-reported.
- Benchmark scores may be affected by evaluation conditions.
- Benchmark contamination can affect reported performance.
- A benchmark score measures performance on a particular evaluation task rather than general intelligence.
- New capabilities may not have established benchmarks.
- Different benchmarks may measure overlapping or different capabilities.
- Historical benchmark data may be incomplete.
- A higher benchmark score does not necessarily indicate greater real-world usefulness.
- Benchmark performance does not directly measure adoption or ecosystem growth.

### 7.12 Proposed Role in the System

Benchmark data will initially be classified as a:

**Supporting Capability Evolution Signal**

Its purpose will be to provide quantitative evidence of model performance changes where reliable and comparable historical evaluations are available.

Benchmark data will not be used as the sole basis for:

- AI Evolution Index calculations
- Technology lifecycle classification
- Future leader prediction
- Claims about overall AI superiority

Instead, it will be combined with other measurable signals.

### 7.13 Initial Assessment

**Status: Suitable — Supporting Source**

Benchmark data can provide valuable quantitative evidence for analysing AI capability evolution.

However, differences in evaluation methodologies and incomplete historical coverage mean that benchmark data must be used selectively.

The project will prioritise comparable, well-documented evaluation results and maintain the original benchmark context rather than combining incompatible scores into an unexplained ranking.

## 8. Hugging Face

### 8.1 Overview

Hugging Face is being investigated as a potential data source for analysing the open-model ecosystem and the development of publicly available AI models.

The Hugging Face Hub contains models, datasets, Spaces, and related metadata from organisations, researchers, and developers. This makes the platform potentially valuable for analysing the growth and evolution of open-source and openly available AI models.

Hugging Face provides programmatic access to Hub information through its APIs and Python client libraries.

### 8.2 Relevance to the Project

Hugging Face provides a different signal from Stack Overflow and GitHub.

Stack Overflow primarily represents developer questions and technical discussions, while GitHub represents open-source repository development. Hugging Face can provide more direct information about the availability, activity, and ecosystem growth of AI models.

Potential signals include:

- Model availability
- Model popularity
- Model downloads
- Model likes
- Model tags
- Model libraries
- Model tasks
- Model organisations
- Model updates
- Related datasets
- AI model ecosystem growth

This makes Hugging Face potentially useful for analysing the evolution of open AI models.

### 8.3 Potential Data

Potential model-level information may include:

- Model ID
- Model name
- Organisation
- Model creation information where available
- Last modification information
- Downloads
- Likes
- Tags
- Pipeline or task information
- Library information
- Model architecture information where available
- Model type
- Dataset associations
- License information
- Model card information
- Repository URL

The exact fields available will depend on the Hub API and the selected access method.

### 8.4 Model Identification

The project may use Hugging Face model metadata to identify models associated with selected AI technologies and capabilities.

Potential classification categories include:

- Large language models
- Vision models
- Multimodal models
- Speech models
- Embedding models
- Image generation models
- Video models
- Reinforcement learning models
- Agent-related models
- Other emerging model categories

The project will avoid assuming that every model uploaded to Hugging Face represents a significant AI technology. Filtering and classification will therefore be required.

### 8.5 Potential Features

Potential features derived from Hugging Face may include:

- Number of models associated with a technology
- Model creation rate
- Model update rate
- Download volume
- Download growth
- Number of likes
- Model popularity
- Number of organisations publishing models
- Number of model variants
- Model task distribution
- Model architecture distribution
- Technology and model co-occurrence
- Open-model ecosystem growth

These indicators may contribute to the AI Evolution Index.

### 8.6 Model Ecosystem Growth

Hugging Face may allow the project to investigate how quickly an AI technology develops an open-model ecosystem.

For example:

Technology A
    ↓
First public model
    ↓
More model variants
    ↓
More organisations
    ↓
Increasing downloads
    ↓
Increasing community activity

This may provide a useful indicator of technology growth.

### 8.7 Download Activity

Model download statistics may provide an adoption signal.

However, download counts will not be treated as direct measurements of:

- Model quality
- Model intelligence
- Commercial adoption
- Active users
- Production deployment

Downloads can be influenced by automated systems, repeated downloads, experiments, mirrors, and other factors.

Therefore, download activity will be combined with other signals rather than being used independently.

### 8.8 Model Popularity

Likes and other engagement indicators may provide additional information about community interest in open models.

However, these measures will be treated as relative ecosystem signals rather than objective measures of model quality.

### 8.9 Model Cards and Textual Analysis

Where model-card information is available and appropriate for use, natural language processing may be used to identify:

- Capabilities
- Intended tasks
- Supported languages
- Model technologies
- Training information
- Limitations
- Associated datasets
- Related technologies

This may provide additional structured information for the AI evolution dataset.

### 8.10 Relationship With GitHub

Some Hugging Face models are associated with GitHub repositories and open-source projects.

Where reliable relationships can be established, the project may investigate connections between:

Hugging Face Model
        ↓
GitHub Repository
        ↓
Developer Activity
        ↓
Open-Source Ecosystem Growth

This could provide a richer representation of open-model evolution.

### 8.11 Relationship With Other Data Sources

Hugging Face can complement other project signals:

| Source | Main Signal |
|---|---|
| Stack Overflow | Developer activity |
| Reddit | Community discussion |
| GitHub | Open-source development |
| Hugging Face | Open-model ecosystem |
| Model releases | Direct AI development |
| Benchmarks | Capability performance |

Combining these signals may provide a more comprehensive representation of AI evolution.

### 8.12 Historical Data Considerations

The project will investigate how much historical information can be reliably reconstructed from Hugging Face.

Current model metadata may not provide a complete historical time series for every metric.

For example, a current download count does not necessarily provide the complete daily download history required for long-term trend analysis.

Therefore, the project will distinguish between:

1. Historical metadata directly available.
2. Historical information that can be obtained through available datasets or APIs.
3. Metrics that can only be tracked prospectively after the project begins collecting them.

The project will not assume complete historical coverage for every metric.

### 8.13 API and Access Considerations

Hugging Face provides programmatic access through its Hub APIs and Python libraries.

The project will investigate the appropriate access method and available rate limits before implementing data collection.

The system will:

- Avoid unnecessary requests.
- Cache collected information.
- Respect applicable rate limits.
- Store collected data locally.
- Record collection dates.
- Preserve source information.
- Keep API credentials secure where authentication is required.

### 8.14 Limitations

Hugging Face data has several limitations:

- Not all AI models are hosted on Hugging Face.
- Model popularity does not necessarily represent overall AI adoption.
- Download counts are not equivalent to unique users.
- Some models may be uploaded for experimentation rather than production use.
- Model metadata can be incomplete.
- Model naming can be inconsistent.
- Model versions may not always be clearly represented.
- Historical activity may be incomplete.
- Open-model activity represents only part of the wider AI ecosystem.
- Some models may be derivatives or duplicates of existing models.

### 8.15 Proposed Role in the System

Hugging Face will initially be classified as a:

**Supporting Open-Model Ecosystem Signal**

Its primary purpose will be to provide information about:

- Open-model availability
- Model ecosystem growth
- Open-model popularity
- Model development
- Model categories
- Model technology relationships

It will complement GitHub rather than replace it.

### 8.16 Initial Assessment

**Status: Suitable — Supporting Source**

Hugging Face provides valuable information about the open-model ecosystem and can strengthen the project by providing model-level ecosystem signals.

However, because not all historical metrics are necessarily available, Hugging Face should be used as a supporting source rather than the sole basis for historical trend prediction.

## 9. Public Search and Interest Trends

### 9.1 Overview

Public search-interest data will be investigated as an additional signal for measuring general interest in AI technologies and models.

Google Trends is a potential source because it provides anonymised, aggregated, categorised, and normalised information about Google search interest. The platform allows search terms and topics to be compared over time and across geographical regions.

### 9.2 Relevance to the Project

Search-interest data provides a different perspective from developer and open-source ecosystem data.

The project currently considers the following signals:

- Stack Overflow → Developer activity
- GitHub → Open-source development
- Reddit → Community discussion
- Hugging Face → Open-model ecosystem
- Model releases → Direct AI development
- Benchmarks → Measured capability
- Google Trends → General search interest

Search interest may help determine whether changes observed within technical communities are also reflected in broader public interest.

### 9.3 Potential Data

Potential Google Trends indicators include:

- Search interest over time
- Search interest by geographical region
- Related topics
- Related queries
- Rising search terms
- Search interest comparisons
- Trending search activity

Google Trends data is represented using normalized values rather than raw numbers of searches.

### 9.4 Potential Features

Potential features may include:

- Search interest score
- Search-interest growth rate
- Search-interest acceleration
- Search-interest volatility
- Relative interest between technologies
- Related search frequency
- Regional interest
- Emerging search topics

These indicators may be used as supplementary features in trend and evolution analysis.

### 9.5 Historical Analysis

Search interest can potentially be analysed as a time series.

For example:

| Period | Technology | Search Interest |
|---|---|---:|
| 2023-01 | Technology A | — |
| 2023-06 | Technology A | — |
| 2024-01 | Technology A | — |
| 2025-01 | Technology A | — |
| 2026-08 | Technology A | — |

The exact historical coverage and granularity will depend on the selected Google Trends data-access method.

### 9.6 Data Normalisation

Google Trends does not provide raw search counts. Instead, search interest is represented using normalized values.

Therefore, Trends values will be treated as relative measures of search interest rather than absolute numbers of searches.

Comparisons will be performed carefully because Trends values are dependent on the selected terms, time period, geography, category, and comparison context.

### 9.7 Export and Data Access

Google Trends allows users to export chart data as CSV files for further analysis.

Google also provides a public Google Trends dataset through BigQuery containing selected Top and Rising search queries.

The project will investigate the most appropriate method for obtaining the required historical AI-related search-interest data.

### 9.8 Potential Role in Emerging Trend Detection

Search-interest changes may provide an additional early signal for emerging technologies.

For example:

Technology A

Developer activity → increasing
GitHub activity → increasing
Search interest → rapidly increasing

This combination may provide stronger evidence of an emerging trend than any individual signal.

However, search interest alone will not be sufficient to classify a technology as emerging.

### 9.9 Relationship With Other Data Sources

The project may investigate relationships between search interest and other ecosystem indicators.

For example:

Search Interest
      ↓
Developer Interest
      ↓
Open-Source Activity
      ↓
Community Activity
      ↓
Technology Adoption

Alternatively, changes in developer activity may occur before broader search interest increases.

The project may investigate these relationships using correlation, lag analysis, and time-series techniques.

### 9.10 Limitations

Google Trends data has several limitations:

- Search interest does not represent actual technology adoption.
- Search data is based on a sample rather than complete search activity.
- Trends values are normalized rather than raw search counts.
- Search interest may be influenced by news events or temporary publicity.
- Similar technologies may have different names and search terms.
- Search terms can have ambiguous meanings.
- Search interest may represent curiosity rather than actual usage.
- Search behaviour varies between geographical regions.
- Historical values may depend on the selected comparison and query configuration.
- The public Trends dataset does not provide unlimited historical data for arbitrary queries.

### 9.11 Proposed Role in the System

Google Trends will initially be classified as an:

**Optional Public Interest Signal**

Its purpose will be to provide additional evidence about general interest in AI technologies and models.

It will not be treated as a direct measure of:

- Technical capability
- Developer adoption
- Commercial success
- Model quality
- Technology superiority

### 9.12 Initial Assessment

**Status: Useful — Optional Supporting Source**

Google Trends can provide a valuable external signal for studying AI technology interest and emerging trends.

However, because search interest does not directly represent technological development or adoption, it should remain a supporting feature rather than a core dependency.

The project will first prioritise data sources that provide stronger direct evidence of AI development and ecosystem activity.

## 10. Data Source Comparison

The investigated data sources provide different types of information about the AI ecosystem. Because no single source can represent AI evolution comprehensively, the project will evaluate the sources according to their relevance, data availability, reliability, historical value, machine learning usefulness, collection complexity, and long-term sustainability.

The following criteria will be used:

- **Relevance:** How directly the source contributes to analysing AI evolution.
- **Historical Coverage:** Availability of useful historical information.
- **Data Quality:** Structure, consistency, and reliability of the available data.
- **Accessibility:** Practical ability to obtain the data through permitted methods.
- **ML Usefulness:** Potential value of the data for feature engineering and machine learning.
- **Collection Complexity:** Difficulty of collecting, processing, and maintaining the data.
- **Sustainability:** Likelihood that the selected access method can continue to support the project.

### 10.1 Preliminary Source Evaluation

Scores are initially assigned on a scale from 1 to 5, where 5 represents the strongest suitability.

| Data Source | Relevance | Historical Coverage | Data Quality | Accessibility | ML Usefulness | Collection Complexity | Sustainability |
|---|---:|---:|---:|---:|---:|---:|---:|
| AI Model / Release Data | 5 | 5 | 4 | 4 | 5 | 3 | 4 |
| Stack Overflow | 5 | 5 | 5 | 4 | 5 | 3 | 4 |
| GitHub | 5 | 4 | 5 | 4 | 5 | 3 | 4 |
| Benchmark Data | 5 | 4 | 4 | 4 | 5 | 4 | 4 |
| Hugging Face | 4 | 3 | 4 | 4 | 4 | 3 | 4 |
| Reddit | 4 | 3 | 3 | 2 | 4 | 4 | 2 |
| Google Trends | 3 | 4 | 4 | 3 | 3 | 3 | 3 |

These scores are preliminary research assessments and may be revised after practical API testing and sample data collection.

## 11. Final Data Source Selection

Based on the initial investigation, the project will use a multi-source data strategy. The system will not rely on a single data source because different sources represent different aspects of AI technology evolution.

The sources are divided into four categories:

### 11.1 Core Sources

The following sources will form the foundation of the initial system:

#### AI Model and Technology Release Data

**Role:** Direct AI technology evolution

This source category will provide information about model versions, releases, capabilities, modalities, tool support, and other documented technological developments.

#### Stack Overflow

**Role:** Developer ecosystem activity

Stack Overflow will provide information about developer questions, technical discussions, tags, answers, engagement, and changes in developer interest surrounding AI technologies.

#### GitHub

**Role:** Open-source ecosystem development

GitHub will provide information about open-source repositories, development activity, stars, forks, releases, and technology ecosystem growth.

### 11.2 Supporting Sources

The following sources will be used where sufficient data is available and where they provide additional analytical value.

#### Benchmark and Evaluation Data

**Role:** Measured AI capability evolution

Benchmark data will provide quantitative evidence of model performance changes within specific evaluation areas.

#### Hugging Face

**Role:** Open-model ecosystem

Hugging Face may provide model-level information, model popularity, downloads, metadata, and open-model ecosystem activity.

### 11.3 Conditional Sources

#### Reddit

**Role:** Community ecosystem activity

Reddit will be considered if appropriate research access can be obtained and sufficient historical data is available.

The core architecture will not depend on Reddit.

### 11.4 Optional Sources

#### Google Trends

**Role:** General public interest

Google Trends may be incorporated if testing demonstrates that search-interest data provides useful additional information for emerging trend detection or future prediction.

It will not be required for the initial functioning of the system.

## 12. Initial Data Collection Strategy

The project will use a multi-source data collection architecture in which each source is collected and processed independently before being integrated into a common analytical structure.

The initial strategy is:

**AI Model/Release Data**
→ Model and technology evolution

**Stack Overflow**
→ Developer ecosystem activity

**GitHub**
→ Open-source ecosystem activity

**Benchmark Data**
→ Capability performance

**Hugging Face**
→ Open-model ecosystem

**Reddit**
→ Community activity, if available

**Google Trends**
→ Public interest, if required

The collected data will initially be stored in source-specific raw datasets. This will preserve the original structure of each source and allow source-specific preprocessing.

The data will then be cleaned, normalised, and transformed into common analytical entities such as:

- AI Model
- AI Technology
- AI Capability
- Organisation
- Date
- Activity
- Ecosystem Signal
- Benchmark
- Release Event

This common representation will allow information from different sources to be compared and aggregated.

The project will maintain source information and collection dates so that analytical results can be traced back to their original data sources.

The system will also be designed so that individual data sources can be added, removed, or replaced without requiring major changes to the machine learning and visualisation components.

## 13. M2 Findings

The data-source investigation indicates that AI technology evolution cannot be reliably represented using a single data source.

Different sources provide different perspectives:

- AI model and release data provides direct evidence of technological development.
- Stack Overflow provides developer-focused activity.
- GitHub provides open-source ecosystem activity.
- Benchmark data provides quantitative capability measurements.
- Hugging Face provides open-model ecosystem information.
- Reddit may provide broader community activity where appropriate access is available.
- Google Trends may provide a supplementary public-interest signal.

The investigation therefore supports a multi-source approach in which different data sources are treated as independent ecosystem signals rather than interchangeable measures.

The initial core architecture will prioritise AI model/release data, Stack Overflow, and GitHub. Benchmark and Hugging Face data will provide supporting signals, while Reddit and Google Trends will remain conditional or optional until their practical value and accessibility are confirmed.

A key finding is that the project should not attempt to create a single AI "best model" ranking from these sources. Instead, the system should analyse multiple dimensions of AI evolution and investigate whether these signals collectively provide useful information about technology growth, decline, emerging trends, and future trajectories.

The data-source investigation also identified several important requirements for the next stage of the project:

1. A standardised data model is required to represent information from different sources.
2. Source-specific data collection pipelines should be developed independently.
3. Historical and current data must be distinguished.
4. Data collection dates and source references should be preserved.
5. API limits and access policies must be respected.
6. Missing and inconsistent data must be handled during preprocessing.
7. The system must avoid dependence on a single external data source.
8. The final AI Evolution Index methodology should be developed only after exploratory analysis of the collected data.
9. Machine learning targets must be defined based on measurable historical outcomes rather than assumed future events.
10. Predictions must be evaluated against historical or subsequently available observations wherever possible.

## 14. current architecture

                    AI EVOLUTION PLATFORM
                            │
       ┌────────────────────┼────────────────────┐
       │                    │                    │
       ▼                    ▼                    ▼
   AI MODELS             ECOSYSTEM            CAPABILITY
       │                     │                   │
 Releases / Versions    ┌────┼────┐          Benchmarks
 Capabilities           │    │    │
                        ▼    ▼    ▼
                       SO  GitHub Reddit*
                        │    │    │
                        └────┼────┘
                             │
                        Hugging Face*
                             │
                             ▼
                    NORMALISED DATA
                             │
                             ▼
                     EVOLUTION ENGINE
                             │
                  ┌──────────┼──────────┐
                  ▼          ▼          ▼
              Evolution   Lifecycle   Trends
                Index      Analysis   Detection
                  │          │          │
                  └──────────┼──────────┘
                             ▼
                      ML / Forecasting
                             │
                             ▼
                      WEB APPLICATION
