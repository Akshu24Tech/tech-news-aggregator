# Deploy Update - Integration & Notification Agent Skill

## Purpose
Commit analyzed data to GitHub, trigger workflows, and deliver tech news insights via Slack notifications.

## Context
You are Agent C in a multi-agent tech news aggregation pipeline. Your role is to take structured insights from the NLP Analyst, commit them to a repository, and send formatted notifications to Slack channels.

## Tools and APIs Available
- **PyGithub / GitHub API**: For repository operations (commit, push, PR creation)
- **Slack SDK**: For sending rich notifications via Slack API
- **GitHub MCP**: For advanced repository interactions
- **File operations**: Read analysis results
- **Environment variables**: Access to secrets for authentication

## Input Specification
- **Analysis Results**: Read from `data/analyzed/` directory
- **Manifest**: Read `data/analyzed/manifest.json` for structured insights
- **Environment Variables** (injected via Oz Secrets):
  - `GITHUB_TOKEN`: Personal access token with repo write access
  - `SLACK_BOT_TOKEN`: Slack bot token (xoxb-...)
  - `SLACK_CHANNEL_ID`: Target Slack channel ID
  - `GITHUB_REPO`: Repository name (format: `owner/repo`)

## Workflow Steps

### 1. Initialize Clients
```python
import os
import json
from datetime import datetime
from github import Github
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Verify environment variables
required_vars = ['GITHUB_TOKEN', 'SLACK_BOT_TOKEN', 'SLACK_CHANNEL_ID', 'GITHUB_REPO']
for var in required_vars:
    assert os.getenv(var), f"{var} not found in environment"

# Initialize GitHub client
gh = Github(os.getenv('GITHUB_TOKEN'))
repo = gh.get_repo(os.getenv('GITHUB_REPO'))

# Initialize Slack client
slack_client = WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
channel_id = os.getenv('SLACK_CHANNEL_ID')

print("Clients initialized successfully")
```

### 2. Load Analysis Results
```python
# Read analysis manifest
with open('data/analyzed/manifest.json', 'r', encoding='utf-8') as f:
    analysis_manifest = json.load(f)

# Read full results
with open('data/analyzed/analysis_results.json', 'r', encoding='utf-8') as f:
    analysis_results = json.load(f)

print(f"Loaded analysis for {analysis_manifest['total_articles']} articles")
```

### 3. Commit to GitHub

Push analysis results to the repository:

```python
from notifier.github_actions import GitHubCommitter

committer = GitHubCommitter(repo)

# Prepare files to commit
files_to_commit = {
    'data/analyzed/manifest.json': json.dumps(analysis_manifest, indent=2),
    'data/analyzed/analysis_results.json': json.dumps(analysis_results, indent=2)
}

# Create commit message
commit_message = f"""Tech News Update - {datetime.utcnow().strftime('%Y-%m-%d')}

Analysis Summary:
- Total Articles Analyzed: {analysis_manifest['total_articles']}
- Successful: {analysis_manifest['successful_analyses']}
- Top Trending Topics: {', '.join([t[0] for t in analysis_manifest['trending_topics']['top_keywords'][:3]])}

Co-Authored-By: Warp <agent@warp.dev>
"""

try:
    # Commit and push
    commit_sha = committer.commit_files(
        files=files_to_commit,
        message=commit_message,
        branch='main'
    )
    
    print(f"✓ Committed to GitHub: {commit_sha[:7]}")
    commit_url = f"https://github.com/{os.getenv('GITHUB_REPO')}/commit/{commit_sha}"
    
except Exception as e:
    print(f"✗ Failed to commit to GitHub: {str(e)}")
    commit_url = None
```

### 4. Format Slack Notification

Create rich Slack message using Block Kit:

```python
from notifier.slack_client import SlackFormatter

formatter = SlackFormatter()

# Get top articles for notification
top_articles = analysis_manifest['top_articles'][:5]
trending_topics = analysis_manifest['trending_topics']

# Build Slack blocks
blocks = [
    {
        "type": "header",
        "text": {
            "type": "plain_text",
            "text": f"📰 Tech News Digest - {datetime.utcnow().strftime('%B %d, %Y')}",
            "emoji": True
        }
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{analysis_manifest['successful_analyses']} articles* analyzed from top tech sources"
        }
    },
    {
        "type": "divider"
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*🔥 Trending Topics*"
        }
    }
]

# Add trending topics
trending_text = ""
for keyword, count in trending_topics['top_keywords'][:5]:
    trending_text += f"• *{keyword}* ({count} mentions)\n"

blocks.append({
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": trending_text
    }
})

blocks.append({"type": "divider"})
blocks.append({
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "*📌 Top Articles*"
    }
})

# Add top articles
for i, article in enumerate(top_articles, 1):
    article_block = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{i}. {article['source_name']}*\n{article['summary'][:150]}...\n" +
                    f"_Keywords: {', '.join(article['keywords'][:5])}_"
        },
        "accessory": {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": "Read More"
            },
            "url": article['source_url']
        }
    }
    blocks.append(article_block)

# Add footer with GitHub link
if commit_url:
    blocks.append({"type": "divider"})
    blocks.append({
        "type": "context",
        "elements": [
            {
                "type": "mrkdwn",
                "text": f"💾 <{commit_url}|View full analysis on GitHub> | Generated by Oz Cloud Agents"
            }
        ]
    })
```

### 5. Send Slack Notification

```python
try:
    response = slack_client.chat_postMessage(
        channel=channel_id,
        blocks=blocks,
        text=f"Tech News Digest - {datetime.utcnow().strftime('%B %d, %Y')}"  # Fallback text
    )
    
    message_ts = response['ts']
    print(f"✓ Slack notification sent successfully")
    print(f"  Message timestamp: {message_ts}")
    
    # Optional: Post detailed trending analysis in thread
    if trending_topics['emerging_trends']:
        thread_text = "*🚀 Emerging Trends (appearing in 3+ sources):*\n\n"
        for trend in trending_topics['emerging_trends'][:5]:
            thread_text += f"• *{trend['keyword']}* - seen in {trend['source_count']} sources\n"
            thread_text += f"  Sources: {', '.join(trend['sources'])}\n\n"
        
        slack_client.chat_postMessage(
            channel=channel_id,
            thread_ts=message_ts,
            text=thread_text
        )
        print(f"✓ Posted emerging trends in thread")
    
except SlackApiError as e:
    print(f"✗ Failed to send Slack notification: {e.response['error']}")
    print(f"  Details: {e}")
```

### 6. Optional: Trigger GitHub Actions Workflow

If you have a GitHub Actions workflow to run:

```python
# Trigger workflow dispatch
try:
    workflow = repo.get_workflow('update-dashboard.yml')
    workflow.create_dispatch(
        ref='main',
        inputs={
            'run_id': analysis_manifest['run_id'],
            'article_count': str(analysis_manifest['successful_analyses'])
        }
    )
    print(f"✓ Triggered GitHub Actions workflow")
except Exception as e:
    print(f"⚠️ Could not trigger workflow: {str(e)}")
```

### 7. Generate Summary Report

```python
summary = {
    'run_id': analysis_manifest['run_id'],
    'agent': 'integrator',
    'completed_at': datetime.utcnow().isoformat(),
    'github_commit': commit_sha if commit_url else None,
    'slack_message_ts': message_ts if 'message_ts' in locals() else None,
    'articles_delivered': len(top_articles),
    'trending_topics_count': len(trending_topics['top_keywords']),
    'status': 'success'
}

# Save summary
summary_path = 'data/analyzed/delivery_summary.json'
with open(summary_path, 'w') as f:
    json.dump(summary, f, indent=2)

print(f"\n{'='*60}")
print(f"Deployment Complete")
print(f"{'='*60}")
print(f"GitHub Commit: {commit_sha[:7] if commit_url else 'Failed'}")
print(f"Slack Notification: {'Sent' if 'message_ts' in locals() else 'Failed'}")
print(f"Articles Delivered: {len(top_articles)}")
print(f"Trending Topics: {len(trending_topics['top_keywords'])}")
print(f"{'='*60}")
```

## Output Specification

### delivery_summary.json
```json
{
  "run_id": "2024-01-15T08:00:00",
  "agent": "integrator",
  "completed_at": "2024-01-15T08:05:23",
  "github_commit": "abc1234",
  "slack_message_ts": "1705305923.123456",
  "articles_delivered": 5,
  "trending_topics_count": 10,
  "status": "success"
}
```

## Slack Message Examples

### Daily Digest Format
```
📰 Tech News Digest - January 15, 2024

12 articles analyzed from top tech sources

━━━━━━━━━━━━━━━━━━━━━━

🔥 Trending Topics
• AI (8 mentions)
• Cybersecurity (5 mentions)
• Cloud Computing (4 mentions)
• Startup Funding (3 mentions)

━━━━━━━━━━━━━━━━━━━━━━

📌 Top Articles

1. TechCrunch
OpenAI announces GPT-5 with improved reasoning capabilities...
Keywords: AI, OpenAI, GPT-5, machine learning
[Read More]

2. The Verge
Microsoft Azure launches new security features...
Keywords: cloud, security, Microsoft, enterprise
[Read More]

━━━━━━━━━━━━━━━━━━━━━━
💾 View full analysis on GitHub | Generated by Oz Cloud Agents
```

## Error Handling

### GitHub Authentication Failures
```python
try:
    repo = gh.get_repo(os.getenv('GITHUB_REPO'))
    repo.get_branch('main')  # Test access
except Exception as e:
    print(f"✗ GitHub authentication failed: {str(e)}")
    print("  Check that GITHUB_TOKEN has repo write permissions")
    # Continue with Slack notification even if GitHub fails
```

### Slack API Rate Limits
```python
import time

max_retries = 3
for attempt in range(max_retries):
    try:
        response = slack_client.chat_postMessage(...)
        break
    except SlackApiError as e:
        if e.response['error'] == 'ratelimited':
            retry_after = int(e.response.headers.get('Retry-After', 60))
            print(f"Rate limited, waiting {retry_after}s...")
            time.sleep(retry_after)
        else:
            raise
```

### Malformed Blocks
```python
# Validate blocks before sending
def validate_slack_blocks(blocks):
    if not isinstance(blocks, list):
        raise ValueError("Blocks must be a list")
    for block in blocks:
        if 'type' not in block:
            raise ValueError("Each block must have a 'type' field")
    return True

try:
    validate_slack_blocks(blocks)
    response = slack_client.chat_postMessage(channel=channel_id, blocks=blocks)
except Exception as e:
    print(f"⚠️ Block validation failed, sending simple text message")
    slack_client.chat_postMessage(
        channel=channel_id,
        text=f"Tech News Update: {analysis_manifest['successful_analyses']} articles analyzed"
    )
```

## Rollback Procedures

### Failed GitHub Push
```python
if commit_failed:
    print("Rolling back: Deleting local changes")
    # Don't push bad data, but continue with notification
    pass
```

### Failed Slack Notification
```python
if slack_failed:
    # Fallback: Log to file for manual review
    with open('data/failed_notifications.log', 'a') as f:
        f.write(f"{datetime.utcnow()}: Failed to send Slack notification\n")
        f.write(f"Manifest: {analysis_manifest['run_id']}\n\n")
```

## Quality Checks
- [ ] GitHub commit includes Co-Authored-By line
- [ ] Slack message renders correctly (test in Slack API tester)
- [ ] All URLs in Slack message are valid and accessible
- [ ] No secrets or tokens exposed in commit or Slack message
- [ ] Trending topics are relevant and accurate

## Pipeline Completion
Mark the entire pipeline as complete:
```python
signal_path = 'data/.pipeline_complete'
with open(signal_path, 'w') as f:
    json.dump({
        'run_id': analysis_manifest['run_id'],
        'completed_at': datetime.utcnow().isoformat(),
        'status': 'success'
    }, f, indent=2)
```

## Monitoring Metrics
- GitHub commit success rate
- Slack notification delivery rate
- Average notification latency
- Message engagement (optional, via Slack analytics)
- Failed delivery count

## Advanced Features

### Personalized Notifications
```python
# Send different summaries to different channels
tech_leads_channel = os.getenv('TECH_LEADS_CHANNEL')
if tech_leads_channel:
    executive_summary = format_executive_summary(top_articles)
    slack_client.chat_postMessage(
        channel=tech_leads_channel,
        blocks=executive_summary
    )
```

### Create GitHub Issue for High-Priority News
```python
for article in top_articles:
    if article['relevance_score'] > 0.9:
        issue = repo.create_issue(
            title=f"High-Priority News: {article['source_name']}",
            body=f"{article['summary']}\n\nSource: {article['source_url']}",
            labels=['news', 'high-priority']
        )
        print(f"Created issue #{issue.number} for high-priority article")
```

### Integration with Linear (optional)
```python
# If you have Linear integration
from linear import LinearClient

linear = LinearClient(os.getenv('LINEAR_API_KEY'))
for trend in trending_topics['emerging_trends']:
    linear.create_issue(
        team_id='TEAM_ID',
        title=f"Research: {trend['keyword']}",
        description=f"Trending topic identified across {trend['source_count']} sources"
    )
```
