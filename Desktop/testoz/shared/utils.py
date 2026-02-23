"""Utility functions for the tech news aggregator."""

import json
from pathlib import Path
from typing import Any


def load_json(file_path: str) -> Any:
    """
    Load JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Parsed JSON data
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(data: Any, file_path: str, indent: int = 2):
    """
    Save data to JSON file.
    
    Args:
        data: Data to save
        file_path: Output file path
        indent: JSON indentation
    """
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def validate_environment():
    """Validate required environment variables are set."""
    import os
    
    required_vars = [
        'FIRECRAWL_API_KEY',
        'SLACK_BOT_TOKEN',
        'SLACK_CHANNEL_ID',
        'GITHUB_TOKEN',
        'GITHUB_REPO'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    
    if missing:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
