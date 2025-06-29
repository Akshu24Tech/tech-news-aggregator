# Scalable Web Scraping API

Containerized web scraping solution with Python, FastAPI, and Playwright.

## Architecture

- **Scraper Worker**: Python + Playwright for browser automation
- **FastAPI Server**: REST API for triggering scrapes and returning results
- **PostgreSQL**: Persistent data storage
- **Redis**: Caching and job queue management
- **Docker Compose**: Local development setup

## Quick Start

1. Clone and setup:
   ```bash
   git clone <your-repo-url>
   cd scalable-web-scraping-api
   cp .env.example .env  # Edit with your config
   ```

2. Run with Docker:
   ```bash
   docker-compose up -d
   ```

## Project Structure

```
api/           # FastAPI server
scraper/       # Playwright worker
database/      # PostgreSQL setup
docker-compose.yml
```

## API Usage

```bash
# Start scraping
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "selector": ".item"}'

# Check status
curl "http://localhost:8000/status/job-123"

# Get results
curl "http://localhost:8000/results/job-123"
```

## Deployment (Linode VPS)

1. Install Docker:
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo apt install docker-compose-plugin
   ```

2. Deploy:
   ```bash
   git clone <repo-url>
   cd scalable-web-scraping-api
   cp .env.example .env  # Edit for production
   docker compose up -d
   ```
