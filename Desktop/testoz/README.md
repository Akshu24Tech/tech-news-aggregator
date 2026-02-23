# Tech News Aggregator - Oz Cloud Agents

An automated tech news aggregation and analysis system powered by **Oz Cloud Agents**. The system scrapes tech blogs, analyzes content using NLP, and delivers insights via Slack notifications on a scheduled basis.

## 🏗️ Architecture

This project uses a **multi-agent architecture** with three specialized agents:

1. **Agent A (Scraper)**: Extracts clean content from tech news sources using Firecrawl
2. **Agent B (NLP Analyst)**: Processes content with SpaCy and HuggingFace for insights
3. **Agent C (Integrator)**: Commits data to GitHub and sends Slack notifications

All agents run as **Oz Cloud Agents** on the Oz Platform with scheduled triggers.

## 📁 Project Structure

```
testoz/
├── spec.md                    # Detailed technical specification
├── roadmap.md                 # Implementation roadmap (6-7 weeks)
├── README.md                  # This file
├── Dockerfile                 # Docker environment configuration
├── requirements.txt           # Python dependencies
│
├── .agent/skills/            # Oz agent skill definitions
│   ├── research-news.md      # Scraper agent instructions
│   ├── process-nlp.md        # NLP analyst instructions
│   └── deploy-update.md      # Integrator agent instructions
│
├── scraper/                  # Web scraping module
│   ├── __init__.py
│   ├── firecrawl_client.py
│   └── sources.json          # List of news sources
│
├── analyzer/                 # NLP analysis module
│   ├── __init__.py
│   ├── nlp_processor.py
│   └── summarizer.py
│
├── notifier/                 # Integration module
│   ├── __init__.py
│   ├── slack_client.py
│   └── github_actions.py
│
└── shared/                   # Shared utilities
    ├── __init__.py
    ├── models.py
    └── utils.py
```

## 🚀 Quick Start

### Prerequisites

- **Warp terminal** with Oz CLI installed
- **Oz account** with login completed (`oz login`)
- **API keys**:
  - Firecrawl API key
  - Slack bot token
  - GitHub personal access token
- **Minimum 20 credits** in your Oz account

### 1. Clone/Setup Repository

```bash
# If using an existing repo
git clone <your-repo-url>
cd tech-news-aggregator

# Or initialize a new one
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Configure Oz Secrets

Store your API credentials securely:

```bash
oz secret create FIRECRAWL_API_KEY --value "your-firecrawl-api-key"
oz secret create SLACK_BOT_TOKEN --value "xoxb-your-slack-token"
oz secret create SLACK_CHANNEL_ID --value "C01234567"
oz secret create GITHUB_TOKEN --value "ghp_your-github-token"
oz secret create GITHUB_REPO --value "your-org/tech-news-aggregator"
```

### 3. Create Oz Environment

```bash
oz environment create \
  --name tech-news-env \
  --repo https://github.com/<your-org>/tech-news-aggregator \
  --branch main \
  --dockerfile Dockerfile
```

This will:
- Build the Docker image with all NLP dependencies
- Download the SpaCy language model
- Set up the runtime environment for agents

### 4. Test Individual Agents

Test each agent locally before scheduling:

```bash
# Test scraper agent
oz agent run \
  --environment tech-news-env \
  --skill research-news \
  --prompt "Scrape tech news from configured sources"

# Test NLP analyst agent (after scraper completes)
oz agent run \
  --environment tech-news-env \
  --skill process-nlp \
  --prompt "Analyze scraped articles"

# Test integrator agent (after NLP analysis)
oz agent run \
  --environment tech-news-env \
  --skill deploy-update \
  --prompt "Commit and notify"
```

### 5. Schedule Automated Runs

Set up a cron schedule for daily execution:

```bash
oz schedule create \
  --name tech-news-daily \
  --cron "0 8 * * *" \
  --environment tech-news-env \
  --skill research-news \
  --prompt "Execute daily tech news aggregation workflow"
```

This runs every day at 8:00 AM UTC.

## 📊 Monitoring

### View Running Tasks

```bash
# List all runs
oz run list --limit 10

# Check running tasks
oz run list --status running

# Inspect a specific run
oz run inspect <run-id>
```

### Attach to Live Sessions

```bash
# Attach to monitor or steer a running agent
oz run attach <run-id>
```

### Check Task History

Visit the Oz web app at **oz.warp.dev** to:
- View run history and transcripts
- Monitor success rates
- Review agent outputs
- Manage schedules

## 🔧 Configuration

### Adding News Sources

Edit `scraper/sources.json`:

```json
{
  "sources": [
    {
      "name": "TechCrunch",
      "url": "https://techcrunch.com",
      "category": "general_tech",
      "scrape_depth": "homepage"
    },
    {
      "name": "Hacker News",
      "url": "https://news.ycombinator.com",
      "category": "developer",
      "scrape_depth": "homepage"
    }
  ]
}
```

### Adjusting Schedule

Modify the cron expression:

```bash
# Update schedule
oz schedule update tech-news-daily --cron "0 6,18 * * *"  # 6am and 6pm
```

### Customizing NLP Parameters

Edit `analyzer/config.json` (create if doesn't exist):

```json
{
  "max_keywords": 15,
  "summary_length": 200,
  "relevance_threshold": 0.5,
  "min_article_length": 100
}
```

## 🔐 Security Best Practices

- ✅ **All secrets stored in Oz Secrets** (never in code)
- ✅ **API keys injected at runtime** via environment variables
- ✅ **No credentials in git history** (use `.gitignore`)
- ✅ **Co-authorship attribution** on all commits
- ✅ **Rate limiting and retry logic** on all external APIs

## 📈 Success Metrics

Track these metrics to evaluate performance:

- **Coverage**: Number of sources successfully scraped
- **Quality**: Average relevance score of analyzed articles
- **Timeliness**: Workflow completion time
- **Reliability**: Success rate over 30 days
- **Insights**: Number of trending topics identified

Target metrics:
- ✅ 95%+ success rate
- ✅ <5 minute execution time
- ✅ 10-20 high-quality summaries daily

## 🛠️ Development

### Local Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download SpaCy model
python -m spacy download en_core_web_sm

# Run tests
pytest
```

### Building Docker Image Locally

```bash
docker build -t tech-news-env .
docker run -it tech-news-env python --version
```

### Testing Skills Locally

```bash
# Test without Oz (for development)
python -c "
from scraper.firecrawl_client import FirecrawlClient
client = FirecrawlClient(api_key='your-key')
result = client.scrape_url('https://techcrunch.com')
print(result[:200])
"
```

## 🐛 Troubleshooting

### Agent fails with "FIRECRAWL_API_KEY not found"

**Solution**: Ensure secrets are created and environment is configured:
```bash
oz secret list
oz environment inspect tech-news-env
```

### NLP processing times out

**Solution**: Reduce batch size or optimize model loading in `process-nlp.md`

### Slack notifications not received

**Solution**: Verify bot token and channel ID:
```bash
# Test Slack connection
curl -X POST https://slack.com/api/auth.test \
  -H "Authorization: Bearer xoxb-your-token"
```

### Docker build fails

**Solution**: Check internet connectivity and Docker daemon status:
```bash
docker system info
docker system prune -a  # Clean up if needed
```

## 📚 Documentation

- **[spec.md](spec.md)**: Complete technical specification
- **[roadmap.md](roadmap.md)**: 6-7 week implementation plan
- **[Oz Platform Docs](https://docs.warp.dev/agent-platform/cloud-agents)**: Official Oz documentation
- **[Oz CLI Reference](https://docs.warp.dev/reference/cli)**: CLI command reference

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test locally with `oz agent run`
4. Submit a pull request
5. Include co-authorship attribution: `Co-Authored-By: Warp <agent@warp.dev>`

## 📝 License

MIT License - see LICENSE file for details

## 🙋 Support

- **Warp Community Slack**: [Join here](https://go.warp.dev/join-preview)
- **GitHub Issues**: Submit bugs or feature requests
- **Oz Documentation**: https://docs.warp.dev

---

**Built with Oz Cloud Agents** | Powered by Warp
