# Oz CLI Quick Reference Guide

## 🚀 Essential Commands for This Project

### Authentication
```bash
# Login to Oz
oz login

# Check authentication status
oz agent run --help
```

### Secrets Management
```bash
# Create secrets (do this FIRST)
oz secret create FIRECRAWL_API_KEY --value "your-api-key"
oz secret create SLACK_BOT_TOKEN --value "xoxb-your-token"
oz secret create SLACK_CHANNEL_ID --value "C01234567"
oz secret create GITHUB_TOKEN --value "ghp_your-token"
oz secret create GITHUB_REPO --value "owner/repo"

# List all secrets
oz secret list

# Delete a secret
oz secret delete SECRET_NAME

# Update a secret
oz secret update SECRET_NAME --value "new-value"
```

### Environment Management
```bash
# Create environment
oz environment create \
  --name tech-news-env \
  --repo https://github.com/owner/tech-news-aggregator \
  --branch main \
  --dockerfile Dockerfile

# List environments
oz environment list

# Inspect environment
oz environment inspect tech-news-env

# Update environment
oz environment update tech-news-env \
  --repo https://github.com/owner/tech-news-aggregator

# Delete environment
oz environment delete tech-news-env
```

### Running Agents

#### Single Agent Run
```bash
# Run scraper agent
oz agent run \
  --environment tech-news-env \
  --skill research-news \
  --prompt "Scrape tech news from configured sources"

# Run with specific model
oz agent run \
  --environment tech-news-env \
  --skill process-nlp \
  --model claude-3-5-sonnet-20241022 \
  --prompt "Analyze scraped articles"
```

#### Chaining Multiple Skills (if supported)
```bash
# Run complete pipeline
oz agent run \
  --environment tech-news-env \
  --skill research-news \
  --then process-nlp \
  --then deploy-update
```

### Schedule Management
```bash
# Create a schedule
oz schedule create \
  --name tech-news-daily \
  --cron "0 8 * * *" \
  --environment tech-news-env \
  --skill research-news \
  --prompt "Execute daily tech news aggregation"

# List all schedules
oz schedule list

# Inspect a schedule
oz schedule inspect tech-news-daily

# Update schedule timing
oz schedule update tech-news-daily --cron "0 6,18 * * *"

# Pause a schedule
oz schedule pause tech-news-daily

# Resume a schedule
oz schedule resume tech-news-daily

# Delete a schedule
oz schedule delete tech-news-daily
```

### Run Management
```bash
# List recent runs
oz run list --limit 20

# List running tasks
oz run list --status running

# List failed runs
oz run list --status failed

# Inspect a specific run
oz run inspect <run-id>

# Attach to a running task (monitor/steer)
oz run attach <run-id>

# Cancel a running task
oz run cancel <run-id>
```

### MCP Server Management
```bash
# List available MCP servers
oz mcp list

# Create GitHub MCP server
oz mcp create github-server \
  --type github \
  --config '{"repo": "owner/tech-news-aggregator"}'

# Inspect MCP server
oz mcp inspect github-server

# Delete MCP server
oz mcp delete github-server
```

### Model Management
```bash
# List available models
oz model list

# Show default model
oz model default
```

## 📋 Common Cron Expressions

```
# Daily at 8 AM UTC
0 8 * * *

# Twice daily (6 AM and 6 PM UTC)
0 6,18 * * *

# Every weekday at 9 AM UTC
0 9 * * 1-5

# Every Monday at 8 AM UTC
0 8 * * 1

# Every hour
0 * * * *

# Every 6 hours
0 */6 * * *
```

## 🔍 Debugging Commands

```bash
# Check Oz version
oz --version

# Enable debug logging
oz --debug agent run --environment tech-news-env --skill research-news

# Get detailed run information
oz run inspect <run-id> --output-format json

# View run transcript
oz run inspect <run-id> | grep -A 50 "transcript"
```

## 💡 Pro Tips

### 1. Testing Before Scheduling
Always test your skills manually before creating a schedule:
```bash
oz agent run --environment tech-news-env --skill research-news --prompt "Test run"
```

### 2. Viewing Logs in Real-Time
Attach to a running agent to see live output:
```bash
oz run list --status running  # Get run-id
oz run attach <run-id>
```

### 3. Quick Environment Rebuild
If you update your Dockerfile or dependencies:
```bash
oz environment update tech-news-env --rebuild
```

### 4. Check Credit Usage
Monitor your Oz credit balance:
```bash
# This may vary based on CLI version
oz account info
```

### 5. Environment Variables in Skills
Access secrets in your skill code:
```python
import os
api_key = os.getenv('FIRECRAWL_API_KEY')
```

## 🔧 Workflow Patterns

### Pattern 1: Sequential Agent Execution
```bash
# Agent A
oz agent run --environment tech-news-env --skill research-news

# Wait for completion, then Agent B
oz agent run --environment tech-news-env --skill process-nlp

# Wait for completion, then Agent C
oz agent run --environment tech-news-env --skill deploy-update
```

### Pattern 2: Scheduled Sequential
Create three separate schedules with staggered times:
```bash
# Scraper at 8:00 AM
oz schedule create --name scraper --cron "0 8 * * *" --skill research-news

# Analyst at 8:15 AM
oz schedule create --name analyst --cron "15 8 * * *" --skill process-nlp

# Integrator at 8:30 AM
oz schedule create --name integrator --cron "30 8 * * *" --skill deploy-update
```

### Pattern 3: On-Demand Full Pipeline
Run all three agents in sequence manually:
```bash
oz agent run --environment tech-news-env \
  --skill research-news \
  --prompt "Run complete pipeline" && \
oz agent run --environment tech-news-env \
  --skill process-nlp \
  --prompt "Analyze results" && \
oz agent run --environment tech-news-env \
  --skill deploy-update \
  --prompt "Deploy and notify"
```

## 🚨 Troubleshooting Commands

```bash
# If agent fails, check environment
oz environment inspect tech-news-env

# If secrets aren't working
oz secret list

# If schedule isn't running
oz schedule inspect tech-news-daily

# View recent failures
oz run list --status failed --limit 10

# Get detailed error logs
oz run inspect <failed-run-id>
```

## 📚 Additional Resources

- **Oz Platform Docs**: https://docs.warp.dev/agent-platform/cloud-agents
- **Oz CLI Reference**: https://docs.warp.dev/reference/cli
- **Warp Community**: https://go.warp.dev/join-preview

## 🎯 Project-Specific Workflows

### Initial Setup
```bash
# 1. Create secrets
oz secret create FIRECRAWL_API_KEY --value "..."
oz secret create SLACK_BOT_TOKEN --value "..."
oz secret create SLACK_CHANNEL_ID --value "..."
oz secret create GITHUB_TOKEN --value "..."
oz secret create GITHUB_REPO --value "..."

# 2. Create environment
oz environment create --name tech-news-env --repo <repo-url> --dockerfile Dockerfile

# 3. Test each agent
oz agent run --environment tech-news-env --skill research-news --prompt "Test"
oz agent run --environment tech-news-env --skill process-nlp --prompt "Test"
oz agent run --environment tech-news-env --skill deploy-update --prompt "Test"

# 4. Create schedule
oz schedule create --name tech-news-daily --cron "0 8 * * *" --environment tech-news-env --skill research-news
```

### Daily Operations
```bash
# Check last run status
oz run list --limit 1

# Monitor active run
oz run list --status running
oz run attach <run-id>

# View yesterday's results
oz run list --limit 5
```

### Maintenance
```bash
# Update environment after code changes
git push
oz environment update tech-news-env

# Modify schedule
oz schedule update tech-news-daily --cron "0 6 * * *"

# Check credit usage trends
oz run list --limit 30
```
