# Research News - Web Scraping Agent Skill

## Purpose
Extract clean, structured content from tech news sources and prepare it for NLP analysis.

## Context
You are Agent A in a multi-agent tech news aggregation pipeline. Your role is to scrape content from configured news sources, convert it to clean markdown, and store it for downstream processing by the NLP Analyst agent.

## Tools and APIs Available
- **Firecrawl API**: Use for converting web pages to clean markdown
- **File operations**: Read/write capabilities for storing scraped content
- **GitHub MCP**: Access to repository for reading source configurations
- **Shell commands**: For directory operations and file management

## Input Specification
- **Source Configuration**: Read from `scraper/sources.json` which contains:
  ```json
  {
    "sources": [
      {
        "name": "TechCrunch",
        "url": "https://techcrunch.com",
        "category": "general_tech",
        "scrape_depth": "homepage"
      }
    ]
  }
  ```
- **Environment Variables** (injected via Oz Secrets):
  - `FIRECRAWL_API_KEY`: API key for Firecrawl service
  - `OUTPUT_DIR`: Directory to store scraped content (default: `data/raw`)

## Workflow Steps

### 1. Initialize Environment
```python
import os
import json
from datetime import datetime

# Verify required environment variables
assert os.getenv('FIRECRAWL_API_KEY'), "FIRECRAWL_API_KEY not found"

# Set up output directory
output_dir = os.getenv('OUTPUT_DIR', 'data/raw')
os.makedirs(output_dir, exist_ok=True)

# Create timestamp for this run
run_timestamp = datetime.utcnow().isoformat()
```

### 2. Load Source Configuration
```python
# Read sources configuration
with open('scraper/sources.json', 'r') as f:
    config = json.load(f)
    sources = config['sources']

print(f"Loaded {len(sources)} sources to scrape")
```

### 3. Scrape Each Source
For each source in the configuration:

```python
from scraper.firecrawl_client import FirecrawlClient

client = FirecrawlClient(api_key=os.getenv('FIRECRAWL_API_KEY'))

results = []
for source in sources:
    try:
        print(f"Scraping {source['name']}...")
        
        # Use Firecrawl to extract clean markdown
        markdown_content = client.scrape_url(
            url=source['url'],
            formats=['markdown'],
            timeout=30
        )
        
        # Extract metadata
        metadata = {
            'source_name': source['name'],
            'source_url': source['url'],
            'category': source['category'],
            'scraped_at': run_timestamp,
            'word_count': len(markdown_content.split()),
            'status': 'success'
        }
        
        # Save to file
        filename = f"{source['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"---\n")
            f.write(f"source: {source['name']}\n")
            f.write(f"url: {source['url']}\n")
            f.write(f"scraped_at: {run_timestamp}\n")
            f.write(f"---\n\n")
            f.write(markdown_content)
        
        metadata['file_path'] = filepath
        results.append(metadata)
        
        print(f"✓ Saved {source['name']} ({metadata['word_count']} words)")
        
    except Exception as e:
        print(f"✗ Failed to scrape {source['name']}: {str(e)}")
        results.append({
            'source_name': source['name'],
            'status': 'failed',
            'error': str(e)
        })
```

### 4. Generate Manifest
Create a manifest file that downstream agents can read:

```python
manifest = {
    'run_id': run_timestamp,
    'agent': 'scraper',
    'total_sources': len(sources),
    'successful_scrapes': len([r for r in results if r['status'] == 'success']),
    'failed_scrapes': len([r for r in results if r['status'] == 'failed']),
    'output_directory': output_dir,
    'results': results
}

manifest_path = os.path.join(output_dir, 'manifest.json')
with open(manifest_path, 'w') as f:
    json.dump(manifest, f, indent=2)

print(f"\nManifest saved to: {manifest_path}")
```

### 5. Report Summary
```python
success_rate = (manifest['successful_scrapes'] / manifest['total_sources']) * 100
print(f"\n{'='*60}")
print(f"Scraping Complete")
print(f"{'='*60}")
print(f"Total Sources: {manifest['total_sources']}")
print(f"Successful: {manifest['successful_scrapes']}")
print(f"Failed: {manifest['failed_scrapes']}")
print(f"Success Rate: {success_rate:.1f}%")
print(f"Output Directory: {output_dir}")
print(f"{'='*60}")
```

## Output Specification
- **Scraped Content Files**: One markdown file per source in `data/raw/`
  - Format: `{source_name}_{date}.md`
  - Contains: YAML frontmatter + clean markdown content
- **Manifest File**: `data/raw/manifest.json`
  - Contains: Run metadata, success/failure stats, file paths

## Error Handling

### Rate Limiting
If Firecrawl API returns rate limit errors:
```python
import time

max_retries = 3
retry_delay = 5  # seconds

for attempt in range(max_retries):
    try:
        result = client.scrape_url(url)
        break
    except RateLimitError as e:
        if attempt < max_retries - 1:
            print(f"Rate limited, waiting {retry_delay}s...")
            time.sleep(retry_delay)
            retry_delay *= 2  # exponential backoff
        else:
            raise
```

### Network Failures
```python
try:
    result = client.scrape_url(url, timeout=30)
except requests.exceptions.Timeout:
    print(f"Timeout scraping {url}, skipping...")
except requests.exceptions.ConnectionError:
    print(f"Connection error for {url}, skipping...")
```

### Invalid Content
```python
# Validate markdown content
if len(markdown_content.strip()) < 100:
    print(f"Warning: Content too short for {source['name']}, may be invalid")

# Check for common error patterns
if "404" in markdown_content or "Access Denied" in markdown_content:
    raise ValueError("Page returned error content")
```

## Quality Checks
Before completing, verify:
- [ ] At least 50% of sources scraped successfully
- [ ] Each output file is valid UTF-8 and >100 bytes
- [ ] Manifest file is valid JSON
- [ ] No API keys or secrets in output files

## Next Agent Trigger
Upon successful completion, signal the NLP Analyst agent (Agent B) to begin processing:
```python
# Create signal file for orchestration
signal_path = 'data/.scraper_complete'
with open(signal_path, 'w') as f:
    f.write(run_timestamp)
```

## Monitoring and Observability
This agent should report:
- Number of sources attempted
- Number of sources successfully scraped
- Total word count across all articles
- Any errors or warnings encountered
- Execution time

These metrics help track pipeline health and identify issues with specific sources.
