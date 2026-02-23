# Tech News Aggregator - Oz Cloud Agent Environment
# Base image with Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Download SpaCy language model
RUN python -m spacy download en_core_web_sm

# Create necessary directories
RUN mkdir -p /workspace/data/raw \
    /workspace/data/analyzed \
    /workspace/scraper \
    /workspace/analyzer \
    /workspace/notifier \
    /workspace/shared \
    /workspace/.agent/skills

# Copy project files
COPY . .

# Set Python path
ENV PYTHONPATH=/workspace:$PYTHONPATH

# Health check (optional)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import spacy; import sklearn; import slack_sdk; print('OK')" || exit 1

# Default command (will be overridden by Oz agent runtime)
CMD ["python", "--version"]
