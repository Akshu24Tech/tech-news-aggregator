# Process NLP - Content Analysis Agent Skill

## Purpose
Transform raw scraped content into structured insights using NLP techniques including summarization, keyword extraction, and topic identification.

## Context
You are Agent B in a multi-agent tech news aggregation pipeline. Your role is to process clean markdown from the Scraper agent, analyze it using NLP, and produce structured insights for the Integrator agent to deliver.

## Tools and APIs Available
- **SpaCy**: For NER, POS tagging, and linguistic analysis
- **HuggingFace Transformers**: For advanced summarization (optional)
- **scikit-learn**: For TF-IDF and text vectorization
- **NLTK**: For additional text processing
- **File operations**: Read scraped content, write analysis results

## Input Specification
- **Scraped Content**: Read from `data/raw/` directory
- **Manifest**: Read `data/raw/manifest.json` to locate input files
- **Configuration**: Optional `analyzer/config.json` for tuning parameters

## Workflow Steps

### 1. Initialize NLP Models
```python
import spacy
import json
import os
from datetime import datetime
from analyzer.nlp_processor import NLPProcessor
from analyzer.summarizer import Summarizer

# Load SpaCy model
print("Loading SpaCy model...")
nlp = spacy.load("en_core_web_sm")

# Initialize processors
processor = NLPProcessor(nlp)
summarizer = Summarizer(model_name="facebook/bart-large-cnn")

print("Models loaded successfully")
```

### 2. Load Scraper Output
```python
# Read manifest from previous agent
with open('data/raw/manifest.json', 'r') as f:
    scraper_manifest = json.load(f)

successful_scrapes = [
    r for r in scraper_manifest['results'] 
    if r['status'] == 'success'
]

print(f"Processing {len(successful_scrapes)} articles...")
```

### 3. Process Each Article

For each scraped article:

```python
from sklearn.feature_extraction.text import TfidfVectorizer

analysis_results = []

for scrape_result in successful_scrapes:
    filepath = scrape_result['file_path']
    
    try:
        # Read article content
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split frontmatter and body
        parts = content.split('---\n')
        if len(parts) >= 3:
            article_text = parts[2].strip()
        else:
            article_text = content
        
        print(f"Analyzing {scrape_result['source_name']}...")
        
        # === NLP PROCESSING ===
        
        # 1. Extract keywords using TF-IDF
        keywords = processor.extract_keywords(
            article_text, 
            top_n=10
        )
        
        # 2. Named Entity Recognition
        entities = processor.extract_entities(article_text)
        
        # 3. Generate summary
        summary = summarizer.summarize(
            article_text,
            max_length=150,
            min_length=50
        )
        
        # 4. Identify topics/categories
        topics = processor.classify_topics(article_text)
        
        # 5. Calculate relevance score
        relevance_score = processor.calculate_relevance(
            article_text,
            keywords=keywords,
            entities=entities
        )
        
        # 6. Sentiment analysis (optional)
        sentiment = processor.analyze_sentiment(article_text)
        
        # Compile analysis result
        analysis = {
            'source_name': scrape_result['source_name'],
            'source_url': scrape_result['source_url'],
            'analyzed_at': datetime.utcnow().isoformat(),
            'summary': summary,
            'keywords': keywords,
            'entities': {
                'organizations': entities.get('ORG', []),
                'technologies': entities.get('PRODUCT', []),
                'people': entities.get('PERSON', []),
                'locations': entities.get('GPE', [])
            },
            'topics': topics,
            'relevance_score': relevance_score,
            'sentiment': sentiment,
            'word_count': len(article_text.split()),
            'reading_time_minutes': len(article_text.split()) // 200
        }
        
        analysis_results.append(analysis)
        
        print(f"✓ Analyzed {scrape_result['source_name']}")
        print(f"  Keywords: {', '.join(keywords[:5])}")
        print(f"  Relevance: {relevance_score:.2f}")
        
    except Exception as e:
        print(f"✗ Failed to analyze {scrape_result['source_name']}: {str(e)}")
        analysis_results.append({
            'source_name': scrape_result['source_name'],
            'status': 'failed',
            'error': str(e)
        })
```

### 4. Identify Trending Topics

Analyze across all articles to find common themes:

```python
from collections import Counter

# Aggregate keywords across all articles
all_keywords = []
all_entities = []

for result in analysis_results:
    if 'keywords' in result:
        all_keywords.extend(result['keywords'])
    if 'entities' in result:
        for entity_list in result['entities'].values():
            all_entities.extend(entity_list)

# Find trending topics
keyword_freq = Counter(all_keywords)
entity_freq = Counter(all_entities)

trending_topics = {
    'top_keywords': keyword_freq.most_common(10),
    'top_entities': entity_freq.most_common(10),
    'emerging_trends': []
}

# Identify emerging trends (keywords appearing in multiple sources)
keyword_sources = {}
for result in analysis_results:
    if 'keywords' in result:
        for kw in result['keywords']:
            keyword_sources.setdefault(kw, set()).add(result['source_name'])

for keyword, sources in keyword_sources.items():
    if len(sources) >= 3:  # Appears in 3+ sources
        trending_topics['emerging_trends'].append({
            'keyword': keyword,
            'source_count': len(sources),
            'sources': list(sources)
        })

print(f"\nIdentified {len(trending_topics['emerging_trends'])} emerging trends")
```

### 5. Rank and Filter Articles

Sort articles by relevance and filter for quality:

```python
# Sort by relevance score
analysis_results.sort(
    key=lambda x: x.get('relevance_score', 0),
    reverse=True
)

# Filter to top articles
top_articles = [
    result for result in analysis_results
    if result.get('relevance_score', 0) >= 0.5 and 'status' not in result
]

print(f"Selected {len(top_articles)} high-quality articles")
```

### 6. Generate Analysis Manifest

Create output manifest for the Integrator agent:

```python
output_dir = 'data/analyzed'
os.makedirs(output_dir, exist_ok=True)

manifest = {
    'run_id': scraper_manifest['run_id'],
    'agent': 'nlp_analyst',
    'analyzed_at': datetime.utcnow().isoformat(),
    'total_articles': len(analysis_results),
    'successful_analyses': len([r for r in analysis_results if 'status' not in r]),
    'failed_analyses': len([r for r in analysis_results if r.get('status') == 'failed']),
    'top_articles': top_articles[:20],  # Top 20 articles
    'trending_topics': trending_topics,
    'output_directory': output_dir
}

# Save detailed results
results_path = os.path.join(output_dir, 'analysis_results.json')
with open(results_path, 'w', encoding='utf-8') as f:
    json.dump(analysis_results, f, indent=2, ensure_ascii=False)

# Save manifest
manifest_path = os.path.join(output_dir, 'manifest.json')
with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"\nAnalysis saved to: {results_path}")
print(f"Manifest saved to: {manifest_path}")
```

### 7. Report Summary

```python
print(f"\n{'='*60}")
print(f"NLP Analysis Complete")
print(f"{'='*60}")
print(f"Total Articles: {manifest['total_articles']}")
print(f"Successfully Analyzed: {manifest['successful_analyses']}")
print(f"Failed: {manifest['failed_analyses']}")
print(f"\nTop Trending Topics:")
for keyword, count in trending_topics['top_keywords'][:5]:
    print(f"  - {keyword}: {count} mentions")
print(f"\nTop Articles by Relevance:")
for i, article in enumerate(top_articles[:3], 1):
    print(f"  {i}. {article['source_name']} (score: {article['relevance_score']:.2f})")
print(f"{'='*60}")
```

## Output Specification

### analysis_results.json
Complete analysis for all articles:
```json
[
  {
    "source_name": "TechCrunch",
    "source_url": "https://...",
    "summary": "AI startup announces...",
    "keywords": ["AI", "startup", "funding"],
    "entities": {
      "organizations": ["OpenAI", "Microsoft"],
      "technologies": ["GPT-4", "Azure"],
      "people": ["Sam Altman"],
      "locations": ["San Francisco"]
    },
    "topics": ["artificial_intelligence", "venture_capital"],
    "relevance_score": 0.85,
    "sentiment": {"label": "positive", "score": 0.75}
  }
]
```

### manifest.json
Summary for downstream agent:
- Run metadata
- Statistics (success/failure counts)
- Top 20 articles by relevance
- Trending topics and entities

## Performance Optimization

### Memory Management
```python
# Process in batches to avoid memory issues
batch_size = 10
for i in range(0, len(successful_scrapes), batch_size):
    batch = successful_scrapes[i:i+batch_size]
    process_batch(batch)
    # Free memory
    import gc
    gc.collect()
```

### Model Caching
```python
# Cache SpaCy Doc objects for reuse
doc_cache = {}

def get_doc(text):
    if text not in doc_cache:
        doc_cache[text] = nlp(text)
    return doc_cache[text]
```

## Error Handling

### Handle Long Articles
```python
max_tokens = 10000
if len(article_text.split()) > max_tokens:
    # Truncate or split into chunks
    article_text = ' '.join(article_text.split()[:max_tokens])
```

### Model Loading Failures
```python
try:
    summarizer = Summarizer(model_name="facebook/bart-large-cnn")
except Exception as e:
    print(f"Warning: Could not load transformer model, using extractive summarization")
    summarizer = None  # Fallback to extractive
```

## Quality Checks
- [ ] All articles processed without critical errors
- [ ] Summaries are coherent and <200 words
- [ ] At least 5 keywords per article
- [ ] Relevance scores between 0.0 and 1.0
- [ ] Trending topics identified correctly

## Next Agent Trigger
Signal the Integrator agent:
```python
signal_path = 'data/.nlp_complete'
with open(signal_path, 'w') as f:
    f.write(datetime.utcnow().isoformat())
```

## Monitoring Metrics
- Processing time per article
- Average relevance score
- Number of trending topics found
- Model inference latency
- Memory usage peak
