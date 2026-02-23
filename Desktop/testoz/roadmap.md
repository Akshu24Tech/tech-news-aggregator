# Tech News Aggregator - Project Roadmap

## Phase 1: Foundation Setup (Week 1)

### Goals
- Set up project structure and development environment
- Configure Oz Platform access
- Create base Docker environment

### Tasks

#### 1.1 Project Initialization
- [ ] Create GitHub repository
- [ ] Set up directory structure per spec
- [ ] Initialize Python virtual environment
- [ ] Create `requirements.txt` with all dependencies
- [ ] Add `.gitignore` for Python/Docker

#### 1.2 Oz Platform Setup
- [ ] Authenticate with Oz CLI (`oz login`)
- [ ] Create Oz environment: `oz environment create --name tech-news-env`
- [ ] Configure required secrets:
  - `FIRECRAWL_API_KEY`
  - `SLACK_BOT_TOKEN`
  - `GITHUB_TOKEN`
- [ ] Set up GitHub MCP server for repository operations

#### 1.3 Docker Environment
- [ ] Create `Dockerfile` with Python 3.11 base
- [ ] Install system dependencies (build tools, etc.)
- [ ] Install Python packages from requirements
- [ ] Download SpaCy model: `python -m spacy download en_core_web_sm`
- [ ] Test Docker build locally: `docker build -t tech-news-env .`
- [ ] Push environment to Oz: `oz environment update tech-news-env`

#### 1.4 Data Models
- [ ] Define `Article` data model in `shared/models.py`
- [ ] Define `AnalysisResult` data model
- [ ] Define `NotificationPayload` data model
- [ ] Create utility functions in `shared/utils.py`

**Deliverables**: Working Docker environment, basic project structure, Oz access configured

---

## Phase 2: Agent A - Scraper Implementation (Week 2)

### Goals
- Implement web scraping functionality
- Integrate Firecrawl API
- Create first Oz skill definition

### Tasks

#### 2.1 Scraper Module
- [ ] Create `scraper/sources.json` with initial tech blog URLs:
  - TechCrunch, Hacker News, The Verge, Ars Technica, etc.
- [ ] Implement `scraper/firecrawl_client.py`:
  - Initialize Firecrawl API client
  - Create `scrape_url()` method with retry logic
  - Add markdown cleaning and validation
- [ ] Implement rate limiting and error handling
- [ ] Create unit tests for scraper module

#### 2.2 Oz Skill: research-news.md
- [ ] Create `.agent/skills/research-news.md` with:
  - Clear instructions for scraping workflow
  - Input/output specifications
  - Error handling guidelines
  - Tool usage examples (MCP, file operations)
- [ ] Test skill locally: `oz agent run --skill research-news --prompt "Test scrape"`

#### 2.3 Testing & Validation
- [ ] Test scraping from each source in `sources.json`
- [ ] Validate markdown output quality
- [ ] Verify data storage in correct format
- [ ] Create sample output files for downstream testing

**Deliverables**: Working scraper agent, research-news skill, sample scraped data

---

## Phase 3: Agent B - NLP Analyst Implementation (Week 3)

### Goals
- Implement NLP analysis pipeline
- Generate summaries and extract insights
- Create process-nlp skill

### Tasks

#### 3.1 NLP Processor Module
- [ ] Implement `analyzer/nlp_processor.py`:
  - Text preprocessing (tokenization, cleaning)
  - TF-IDF keyword extraction using scikit-learn
  - Named entity recognition using SpaCy
  - Topic clustering
- [ ] Implement `analyzer/summarizer.py`:
  - Extractive summarization (top-N sentences)
  - Abstractive summarization using HuggingFace (optional, if resources allow)
  - Summary quality scoring

#### 3.2 Analysis Pipeline
- [ ] Create pipeline that:
  - Reads scraped markdown files
  - Processes each article through NLP modules
  - Generates structured JSON output
  - Ranks articles by relevance and novelty
- [ ] Add trend detection across multiple articles
- [ ] Create visualization-ready data structures

#### 3.3 Oz Skill: process-nlp.md
- [ ] Create `.agent/skills/process-nlp.md` with:
  - NLP workflow instructions
  - Model loading and inference steps
  - Output format specifications
  - Performance optimization tips
- [ ] Test skill with Phase 2 sample data

#### 3.4 Testing & Optimization
- [ ] Test with various article types and lengths
- [ ] Benchmark processing speed
- [ ] Optimize memory usage for cloud execution
- [ ] Create sample analysis outputs

**Deliverables**: Working NLP analyst agent, process-nlp skill, analyzed sample data

---

## Phase 4: Agent C - Integrator Implementation (Week 4)

### Goals
- Implement GitHub and Slack integrations
- Create notification system
- Complete the agent pipeline

### Tasks

#### 4.1 GitHub Integration
- [ ] Implement `notifier/github_actions.py`:
  - Repository cloning/updating
  - File commit and push operations
  - PR creation (optional)
  - Workflow trigger via GitHub API
- [ ] Test with test repository

#### 4.2 Slack Integration
- [ ] Create Slack app and bot
- [ ] Implement `notifier/slack_client.py`:
  - Rich message formatting (Block Kit)
  - Channel posting
  - Thread replies for details
  - Error notifications
- [ ] Design notification templates:
  - Daily summary format
  - Trending topics highlight
  - Article recommendations
  - Error alerts

#### 4.3 Oz Skill: deploy-update.md
- [ ] Create `.agent/skills/deploy-update.md` with:
  - Git operations workflow
  - Slack notification instructions
  - Error handling and rollback procedures
  - Webhook trigger setup
- [ ] Test skill end-to-end

#### 4.4 Pipeline Integration
- [ ] Create orchestration script that runs all three agents
- [ ] Implement data handoff between agents
- [ ] Add comprehensive error handling
- [ ] Test complete pipeline locally

**Deliverables**: Working integrator agent, deploy-update skill, complete pipeline

---

## Phase 5: Oz Cloud Deployment (Week 5)

### Goals
- Deploy all agents to Oz Platform
- Configure scheduled execution
- Set up monitoring and alerts

### Tasks

#### 5.1 Cloud Environment Setup
- [ ] Push Docker environment to Oz
- [ ] Verify all dependencies work in cloud environment
- [ ] Test each agent individually in cloud
- [ ] Verify secret injection works correctly

#### 5.2 Schedule Configuration
- [ ] Create cron schedule via CLI:
  ```bash
  oz schedule create \
    --name tech-news-daily \
    --cron "0 8 * * *" \
    --environment tech-news-env \
    --skill research-news
  ```
- [ ] Configure multi-agent coordination
- [ ] Set up schedule via Oz Web App for team visibility

#### 5.3 Monitoring Setup
- [ ] Configure Slack notifications for run status
- [ ] Set up task history retention
- [ ] Enable agent session sharing for team
- [ ] Create dashboard for tracking metrics:
  - Success rate
  - Processing time
  - Article count
  - Error frequency

#### 5.4 Documentation
- [ ] Update README with deployment instructions
- [ ] Document how to add new news sources
- [ ] Create troubleshooting guide
- [ ] Document monitoring and alerting setup

**Deliverables**: Fully deployed cloud agents, automated schedule, monitoring dashboard

---

## Phase 6: Testing & Refinement (Week 6)

### Goals
- Validate system reliability
- Optimize performance
- Fine-tune NLP models

### Tasks

#### 6.1 System Testing
- [ ] Run scheduled workflow for 7 consecutive days
- [ ] Monitor for failures and edge cases
- [ ] Validate data quality and accuracy
- [ ] Test with various source failures

#### 6.2 Performance Optimization
- [ ] Profile slow operations
- [ ] Optimize Docker image size
- [ ] Reduce cold start time
- [ ] Implement caching where appropriate

#### 6.3 Model Fine-tuning
- [ ] Analyze NLP output quality
- [ ] Adjust TF-IDF parameters
- [ ] Tune summarization length
- [ ] Improve trend detection accuracy

#### 6.4 User Feedback
- [ ] Gather feedback from Slack users
- [ ] Adjust notification format based on preferences
- [ ] Add requested features (filters, topics, etc.)

**Deliverables**: Production-ready system, optimized performance, refined outputs

---

## Future Enhancements (Post-Launch)

### Short-term (1-3 months)
- [ ] Add more news sources (Reddit, HN API, RSS feeds)
- [ ] Implement personalized topic filtering
- [ ] Add weekly digest in addition to daily updates
- [ ] Create web dashboard for browsing articles
- [ ] Add sentiment analysis to articles

### Medium-term (3-6 months)
- [ ] Multi-language support
- [ ] Custom categorization based on team interests
- [ ] Integration with Linear for task creation from articles
- [ ] Historical trend analysis and reporting
- [ ] A/B testing for summary quality

### Long-term (6+ months)
- [ ] Machine learning model for article relevance
- [ ] Predictive trending topic identification
- [ ] Integration with team knowledge bases
- [ ] Automated research reports
- [ ] Competitive intelligence features

---

## Success Criteria

### Technical Metrics
- ✅ 95%+ scheduled run success rate
- ✅ <5 minute average workflow execution time
- ✅ 90%+ source scraping success rate
- ✅ Zero credential leaks or security incidents

### Business Metrics
- ✅ Daily delivery of 10-20 high-quality summaries
- ✅ Team engagement with Slack notifications (50%+ open rate)
- ✅ Identification of 3-5 trending topics per week
- ✅ Positive team feedback on content quality

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Firecrawl API rate limits | High | Implement request throttling, use caching |
| Source website changes | Medium | Regular monitoring, fallback scraping methods |
| NLP processing timeout | Medium | Set timeouts, process in batches, optimize models |
| Slack notification spam | Low | Configurable frequency, digest mode, thread replies |
| Oz credit exhaustion | High | Monitor credit usage, set alerts, optimize runs |

---

## Timeline Summary

- **Week 1**: Foundation & Oz setup
- **Week 2**: Scraper agent implementation
- **Week 3**: NLP analyst implementation
- **Week 4**: Integrator implementation
- **Week 5**: Cloud deployment & scheduling
- **Week 6**: Testing & refinement
- **Week 7+**: Production monitoring & enhancements

**Total Duration**: 6-7 weeks to production-ready system
