"""Data models for the tech news aggregator."""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class Article:
    """Represents a scraped article."""
    
    source_name: str
    source_url: str
    content: str
    scraped_at: datetime
    category: str
    word_count: int
    metadata: Optional[Dict] = None


@dataclass
class AnalysisResult:
    """Represents NLP analysis results."""
    
    article: Article
    summary: str
    keywords: List[str]
    entities: Dict[str, List[str]]
    topics: List[str]
    relevance_score: float
    sentiment: Dict[str, float]
    analyzed_at: datetime


@dataclass
class NotificationPayload:
    """Represents data for Slack notification."""
    
    run_id: str
    total_articles: int
    top_articles: List[AnalysisResult]
    trending_topics: Dict[str, List]
    github_commit_url: Optional[str] = None
