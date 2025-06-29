# Scalable Web Scraping API

A containerized web scraping solution built with Python, FastAPI, and Playwright, designed for scalable and reliable data extraction.

## 🏗️ Architecture Overview

This project consists of four main components working together to provide a robust web scraping solution:

### 1. Scraper Worker (Python + Playwright)
- **Purpose**: Handles the actual web scraping operations
- **Technology**: Python with Playwright for browser automation
- **Execution**: Runs on a schedule or processes queue-based tasks
- **Deployment**: Containerized as a separate service for scalability
- **Features**:
  - Headless browser automation
  - JavaScript rendering support
  - Concurrent scraping capabilities
  - Error handling and retry mechanisms

### 2. FastAPI Server
- **Purpose**: Provides REST API interface for the scraping service
- **Technology**: FastAPI (Python)
- **Functionality**:
  - Trigger scraping jobs
  - Return cached results
  - Manage scraping schedules
  - Monitor job status
- **Endpoints**:
  - `POST /scrape` - Initiate new scraping job
  - `GET /results/{job_id}` - Retrieve scraping results
  - `GET /status/{job_id}` - Check job status
  - `GET /cache/{url}` - Get cached data

### 3. Database Layer
- **PostgreSQL**: Persistent storage for scraped data, job history, and configurations
- **Redis**: Fast caching layer and job queue management
- **Data Flow**:
  - Fresh scraping results stored in PostgreSQL
  - Frequently accessed data cached in Redis
  - Job queues managed through Redis

### 4. Container Orchestration
- **Docker Compose**: Local development environment setup
- **Benefits**:
  - Consistent development environment
  - Easy service management
  - Simplified dependency handling

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.9+ (for local development)
- Git

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd scalable-web-scraping-api
   ```

2. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start the services**
   ```bash
   docker-compose up -d
   ```

4. **Verify the setup**
   ```bash
   curl http://localhost:8000/health
   ```

## 📁 Project Structure

```
scalable-web-scraping-api/
├── api/                    # FastAPI application
│   ├── main.py            # API entry point
│   ├── routes/            # API route definitions
│   ├── models/            # Data models
│   └── dependencies/      # Shared dependencies
├── scraper/               # Scraper worker
│   ├── worker.py          # Main worker script
│   ├── scrapers/          # Site-specific scrapers
│   └── utils/             # Utility functions
├── database/              # Database schemas and migrations
│   ├── migrations/        # PostgreSQL migrations
│   └── init.sql          # Initial database setup
├── docker-compose.yml     # Local development setup
├── Dockerfile.api         # FastAPI container
├── Dockerfile.scraper     # Scraper worker container
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Database Configuration
POSTGRES_DB=scraper_db
POSTGRES_USER=scraper_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# Redis Configuration
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=false

# Scraper Configuration
SCRAPER_CONCURRENT_JOBS=5
SCRAPER_TIMEOUT=30
BROWSER_HEADLESS=true
```

## 🐳 Docker Compose Services

The `docker-compose.yml` includes:

- **api**: FastAPI server (port 8000)
- **scraper**: Playwright worker
- **postgres**: PostgreSQL database (port 5432)
- **redis**: Redis cache and queue (port 6379)
- **nginx** (optional): Reverse proxy for production

## 🌐 API Usage Examples

### Start a Scraping Job
```bash
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "selector": ".product-item",
    "schedule": "0 */6 * * *"
  }'
```

### Get Job Status
```bash
curl "http://localhost:8000/status/job-123"
```

### Retrieve Results
```bash
curl "http://localhost:8000/results/job-123"
```

## 🚀 Deployment

### Linode VPS Deployment

1. **Server Setup**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   
   # Install Docker Compose
   sudo apt install docker-compose-plugin
   ```

2. **Deploy Application**
   ```bash
   # Clone repository
   git clone <your-repo-url>
   cd scalable-web-scraping-api
   
   # Configure environment
   cp .env.example .env
   # Edit .env for production
   
   # Deploy
   docker compose -f docker-compose.prod.yml up -d
   ```

3. **Configure Reverse Proxy** (recommended)
   - Set up Nginx or Traefik
   - Configure SSL certificates
   - Set up domain routing

## 🔍 Monitoring and Logging

- **Health Checks**: Built-in endpoints for service monitoring
- **Logging**: Structured JSON logging for all services
- **Metrics**: Optional Prometheus integration
- **Alerting**: Configurable alerts for job failures

## 🛠️ Development

### Running Tests
```bash
# Unit tests
python -m pytest tests/

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Adding New Scrapers
1. Create scraper class in `scraper/scrapers/`
2. Register scraper in worker configuration
3. Add API endpoint for specific scraper
4. Update documentation

## 📈 Scaling Considerations

- **Horizontal Scaling**: Deploy multiple scraper workers
- **Queue Management**: Use Redis for job distribution
- **Database Optimization**: Implement read replicas for high load
- **Caching Strategy**: Leverage Redis for frequently accessed data
- **Rate Limiting**: Implement per-domain rate limiting

## 🔒 Security

- Environment variable management
- API authentication (JWT recommended)
- Database connection security
- Container security best practices
- Rate limiting and DDoS protection

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create GitHub issues for bugs and feature requests
- **Documentation**: Check the `/docs` endpoint when API is running
- **Community**: Join our Discord/Slack for discussions

---

**Note**: This is a development-ready template. Adjust configurations and add specific implementation details based on your exact requirements.
