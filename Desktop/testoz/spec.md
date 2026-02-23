# Tech News Aggregator - Oz Cloud Agents System

## Overview
An automated tech news aggregation and analysis system powered by Oz Cloud Agents. The system scrapes tech blogs, analyzes content using NLP, and delivers insights via Slack notifications on a scheduled basis.

## Architecture Design

### Directory Structure
```
testoz/
├── spec.md
├── roadmap.md
├── .agent/
│   └── skills/
│       ├── research-news.md
│       ├── process-nlp.md
│       └── deploy-update.md
├── scraper/
│   ├── __init__.py
│   ├── firecrawl_client.py
│   └── sources.json
├── analyzer/
│   ├── __init__.py
│   ├── nlp_processor.py
│   └── summarizer.py
├── notifier/
│   ├── __init__.py
│   ├── slack_client.py
│   └── github_actions.py
├── shared/
│   ├── __init__.py
│   ├── models.py
│   └── utils.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Specialized Agent Roles

### Agent A: Scraper Agent
**Purpose**: Extract clean, structured content from tech news sources  
**Technology Stack**: Python, Firecrawl API, BeautifulSoup4  
**Skill Reference**: `.agent/skills/research-news.md`

**Responsibilities**:
- Fetch content from configured tech blog sources
- Convert HTML to clean markdown using Firecrawl
- Filter out ads, navigation, and irrelevant content
- Store raw markdown in structured format
- Handle rate limiting and retries

**Input**: List of target URLs from `sources.json`  
**Output**: Clean markdown files with metadata (title, author, date, source)

### Agent B: NLP Analyst Agent
**Purpose**: Process raw text into actionable insights  
**Technology Stack**: Python, HuggingFace Transformers, SpaCy, scikit-learn  
**Skill Reference**: `.agent/skills/process-nlp.md`

**Responsibilities**:
- Tokenize and preprocess markdown content
- Extract key terms using TF-IDF scoring
- Generate summaries using extractive/abstractive methods
- Identify trending topics and technologies
- Score articles by relevance and novelty
- Create structured JSON output with insights

**Input**: Clean markdown files from Scraper Agent  
**Output**: JSON with summaries, key terms, scores, and categories

### Agent C: Integrator Agent
**Purpose**: Deploy updates and send notifications  
**Technology Stack**: Python, GitHub Actions SDK, Slack API  
**Skill Reference**: `.agent/skills/deploy-update.md`

**Responsibilities**:
- Commit analyzed data to GitHub repository
- Trigger GitHub Actions workflows if needed
- Format insights for Slack delivery
- Send rich Slack notifications with summaries
- Handle error notifications and retry logic

**Input**: Analyzed JSON data from NLP Analyst  
**Output**: GitHub commits, Slack notifications, workflow triggers

## Technical Specifications

### Environment Configuration

**Docker Base Image**: `python:3.11-slim`

**Required Dependencies**:
```
# Core
python>=3.11
numpy>=1.24.0
pandas>=2.0.0

# Web Scraping
firecrawl-py>=0.0.5
beautifulsoup4>=4.12.0
requests>=2.31.0

# NLP
spacy>=3.7.0
transformers>=4.35.0
torch>=2.1.0
scikit-learn>=1.3.0
nltk>=3.8.0

# Integration
slack-sdk>=3.23.0
PyGithub>=2.1.1
python-dotenv>=1.0.0
```

**SpaCy Model**: `en_core_web_sm` (small English model, ~12MB)

### Oz Cloud Agent Setup

#### Environments
Create an Oz environment named `tech-news-env`:
```bash
oz environment create \
  --name tech-news-env \
  --repo https://github.com/<your-org>/tech-news-aggregator \
  --branch main \
  --dockerfile Dockerfile
```

#### Secrets Management
Store sensitive credentials in Oz Secrets:
```bash
oz secret create FIRECRAWL_API_KEY --value "your-api-key"
oz secret create SLACK_BOT_TOKEN --value "xoxb-your-token"
oz secret create GITHUB_TOKEN --value "ghp_your-token"
```

#### MCP Server Configuration
Configure GitHub MCP server for repository operations:
```bash
oz mcp create github-server \
  --type github \
  --config '{"repo": "<your-org>/tech-news-aggregator"}'
```

### Workflow Orchestration

**Execution Flow**:
1. **Scraper Agent** runs first → outputs to `/data/raw/`
2. **NLP Analyst Agent** processes raw data → outputs to `/data/analyzed/`
3. **Integrator Agent** commits and notifies → completes workflow

**Agent Communication**:
- Agents share data via mounted volumes or cloud storage
- Each agent outputs JSON manifest with file locations
- Subsequent agents read manifests to locate input data

## Oz Trigger Configuration

### Cron Schedule Setup

**Via CLI**:
```bash
oz schedule create \
  --name tech-news-daily \
  --cron "0 8 * * *" \
  --environment tech-news-env \
  --skill research-news \
  --prompt "Scrape and analyze tech news from configured sources"
```

**Cron Schedule**: `0 8 * * *` (Daily at 8:00 AM UTC)

**Via Oz Web App**:
1. Navigate to oz.warp.dev
2. Go to Schedules → Create Schedule
3. Configure:
   - Name: `tech-news-daily`
   - Trigger: Cron expression `0 8 * * *`
   - Environment: `tech-news-env`
   - Skill Chain: `research-news` → `process-nlp` → `deploy-update`
   - Prompt: "Execute daily tech news aggregation workflow"

### Multi-Agent Coordination

**Option 1: Sequential Skills**
Execute skills in sequence where each skill triggers the next:
```bash
oz agent run \
  --environment tech-news-env \
  --skill research-news \
  --then process-nlp \
  --then deploy-update
```

**Option 2: Master Orchestrator**
Create a master skill that coordinates all three agents:
```bash
oz agent run \
  --environment tech-news-env \
  --skill orchestrate-news-pipeline \
  --prompt "Run complete news aggregation workflow"
```

## Monitoring and Observability

### Agent Session Sharing
Team members can attach to running tasks:
```bash
oz run list --status running
oz run attach <run-id>
```

### Task History
View past runs and their outcomes:
```bash
oz run list --limit 30
oz run inspect <run-id>
```

### Slack Notifications
Configure notifications for:
- ✅ Successful workflow completion with summary
- ⚠️ Partial failures (e.g., some sources failed)
- ❌ Critical errors requiring intervention

## Success Metrics

- **Coverage**: Number of sources successfully scraped
- **Quality**: Average relevance score of analyzed articles
- **Timeliness**: Workflow completion time
- **Reliability**: Success rate over 30 days
- **Insights**: Number of trending topics identified

## Security Considerations

1. **API Keys**: Store all credentials in Oz Secrets (never in code)
2. **Rate Limiting**: Implement exponential backoff for external APIs
3. **Data Privacy**: Ensure scraped content respects robots.txt and Terms of Service
4. **Access Control**: Limit who can trigger/modify scheduled agents via Oz permissions

## Next Steps

Refer to `roadmap.md` for implementation phases and timeline.
