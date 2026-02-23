"""Firecrawl API client for web scraping."""

import os
from typing import Optional


class FirecrawlClient:
    """Client for interacting with Firecrawl API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Firecrawl client.
        
        Args:
            api_key: Firecrawl API key. If None, reads from FIRECRAWL_API_KEY env var.
        """
        self.api_key = api_key or os.getenv('FIRECRAWL_API_KEY')
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY not provided")
    
    def scrape_url(self, url: str, formats: list = None, timeout: int = 30) -> str:
        """
        Scrape a URL and return clean markdown content.
        
        Args:
            url: URL to scrape
            formats: Output formats (default: ['markdown'])
            timeout: Request timeout in seconds
            
        Returns:
            Clean markdown content from the URL
        """
        # TODO: Implement Firecrawl API call
        raise NotImplementedError("Firecrawl integration not yet implemented")
