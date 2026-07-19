# arXiv API for Paper Fetching

Pattern for automatically fetching academic papers from arXiv using their REST API.

## API Endpoint

```
http://export.arxiv.org/api/query
```

## Basic Query

```python
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

def search_arxiv(query, max_results=50):
    params = {
        "search_query": f'all:"{query}"',
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = f"http://export.arxiv.org/api/query?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "MyApp/1.0"})
    with urllib.request.urlopen(req, timeout=30) as response:
        xml_data = response.read().decode("utf-8")
    return parse_response(xml_data)
```

## XML Parsing

```python
def parse_response(xml_data):
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    
    papers = []
    for entry in root.findall("atom:entry", ns):
        paper = {}
        paper["arxiv_id"] = entry.find("atom:id", ns).text.split("/abs/")[-1]
        paper["title"] = " ".join(entry.find("atom:title", ns).text.strip().split())
        paper["abstract"] = " ".join(entry.find("atom:summary", ns).text.strip().split())
        paper["authors"] = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns)]
        paper["published"] = entry.find("atom:published", ns).text[:10]
        paper["categories"] = [c.get("term") for c in entry.findall("atom:category", ns)]
        
        for link in entry.findall("atom:link", ns):
            if link.get("title") == "pdf":
                paper["pdf_url"] = link.get("href")
        
        papers.append(paper)
    return papers
```

## Rate Limiting

- arXiv requires 3-second delay between requests
- Use `time.sleep(3)` between queries
- Max 50 results per query (use `start` parameter for pagination)

## Search Query Syntax

```
# All fields
all:"federated learning"

# Title only
ti:"flash attention"

# Abstract only
abs:"speculative decoding"

# Author
au:"Karpathy"

# Category
cat:cs.LG

# Combine with AND/OR/ANDNOT
all:"LLM" AND all:"inference" ANDNOT all:"training"
```

## Relevant Categories for LLM Inference

- `cs.LG` — Machine Learning
- `cs.CL` — Computation and Language
- `cs.DC` — Distributed Computing
- `cs.AR` — Hardware Architecture
- `cs.PF` — Performance

## Deduplication Pattern

```python
existing_papers = load_papers()  # dict keyed by arxiv_id
for paper in new_papers:
    if paper["arxiv_id"] not in existing_papers:
        existing_papers[paper["arxiv_id"]] = paper
save_papers(existing_papers)
```

## Date Filtering

```python
from datetime import datetime, timedelta

def filter_recent(papers, days_back=7):
    cutoff = datetime.now() - timedelta(days=days_back)
    return [p for p in papers if datetime.strptime(p["published"], "%Y-%m-%d") >= cutoff]
```

## Pitfalls

1. **Rate limit** — Must wait 3 seconds between requests or get blocked
2. **XML namespace** — arXiv uses Atom namespace, must include in findall calls
3. **Abstract formatting** — Abstracts have newlines and extra whitespace, use `" ".join(text.split())`
4. **ID format** — arXiv IDs can be `2401.12345` or `2401.12345v1`, handle both
5. **No API key needed** — arXiv API is free and open

## Example Project

See `D:\学习\llm-inference-papers\scripts\fetch_papers.py` for a complete implementation with:
- Multiple search queries
- Deduplication
- Date filtering
- Category-based organization
- JSON storage
