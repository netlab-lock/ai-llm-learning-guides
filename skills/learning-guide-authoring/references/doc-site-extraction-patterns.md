# Doc-Site Extraction Patterns for Chinese Tech Sites

Tested patterns for extracting content from Chinese tech documentation sites, blogs, and community platforms. Last validated: 2026-06.

## Site Classification

| Site | Rendering | Extraction Method | Success Rate |
|------|-----------|-------------------|--------------|
| MkDocs/GitBook sites | Server-rendered | `curl` → regex on `<article>` | ~95% |
| CSDN blogs | Server-rendered | `curl` → regex on `id="content_views"` | ~90% |
| Huawei Cloud BBS | Server-rendered | `curl` → regex on `<article>` | ~70% |
| 华为昇腾文档 (hiascend.com) | Heavy JS SPA | **Browser only** — curl returns empty | ~40% (sidebar loads, content may not) |
| 知乎 (zhihu.com) | JS SPA + login wall | **Difficult** — curl returns empty, browser needs login | ~10% |
| GitHub repos | Server-rendered | `curl` or `browser` | ~95% |
| Gitee repos | Server-rendered | `curl` or `browser` | ~95% |
| arXiv papers | Server-rendered | `curl` → HTML or PDF | ~95% |
| DeepLink whitepaper (MkDocs) | Server-rendered | `curl` → regex on `<article>` | ~98% |

## Extraction Commands

### MkDocs/GitBook Sites (best quality)

```bash
curl -sL --max-time 30 "URL" -H "User-Agent: Mozilla/5.0" | python3 -c "
import sys, re
html = sys.stdin.read()
content = re.findall(r'<article[^>]*>(.*?)</article>', html, re.DOTALL)
if content:
    text = re.sub(r'<[^>]+>', ' ', content[0])
    text = re.sub(r'\s+', ' ', text).strip()
    print(text[:12000])
else:
    print('No content found')
"
```

### CSDN Blogs

```bash
curl -sL --max-time 30 "URL" -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36" | python3 -c "
import sys, re
html = sys.stdin.read()
title = re.findall(r'<title>(.*?)</title>', html)
print(f'Title: {title[0] if title else \"N/A\"}')
# Try content_views first (newer CSDN)
content = re.findall(r'id=\"content_views\"[^>]*>(.*?)</div>', html, re.DOTALL)
if not content:
    content = re.findall(r'article_content[^>]*>(.*?)</article', html, re.DOTALL)
if content:
    text = re.sub(r'<[^>]+>', ' ', content[0])
    text = re.sub(r'\s+', ' ', text).strip()
    print(text[:8000])
else:
    print('Could not extract article body')
"
```

### 知乎 (Zhihu) — Usually Fails

知乎 articles require JavaScript rendering AND login. Best approach:
1. Search for the article title on DuckDuckGo — sometimes content is cached/referenced elsewhere
2. Look for cross-posted content on CSDN or WeChat (微信公众号)
3. Use `browser_use` agent if available (needs login session)
4. As fallback, just note the URL in the guide with a description from the search snippet

### Huawei Ascend Docs (hiascend.com)

```bash
# The site is a heavy SPA — curl returns empty HTML shell
# Browser can load sidebar navigation but main content may not render
# Best approach: use the docs for navigation/structure, get actual content from:
#   1. The Gitee source repo: https://gitee.com/ascend/cann-hccl
#   2. Community blog posts that quote the docs
#   3. Huawei Cloud BBS developer blogs
```

### DeepLink Whitepaper (MkDocs)

```bash
# This is the gold standard — MkDocs server-renders everything
curl -sL --max-time 30 "https://deeplink-org.github.io/superpod-whitepaper/01-architecture/02-huawei/" -H "User-Agent: Mozilla/5.0"
# Content is in <article> tags, tables render beautifully
# Images are relative paths — note them for later reference
```

### arXiv Papers

```bash
# Abstract + metadata
curl -sL "https://arxiv.org/abs/PAPER_ID" | grep -oP '<title>[^<]*</title>'

# Full paper (PDF) — use web_extract or pymupdf
web_extract(urls=["https://arxiv.org/pdf/PAPER_ID"])
```

## Multi-Source Search Pattern

For specialized domains, use parallel search with diverse query strategies:

```
delegate_task(tasks=[
    {"goal": "Search for OFFICIAL docs. Run: ddgs text -q 'topic official documentation' -m 5. Also try: ddgs text -q 'topic 开发文档' -m 5. Return ALL URLs with descriptions.", "toolsets": ["terminal"]},
    {"goal": "Search for COMMUNITY content. Run: ddgs text -q 'topic CSDN' -m 5. Also: ddgs text -q 'topic 技术博客' -m 5. Also: ddgs text -q 'topic zhihu' -m 5. Return ALL URLs.", "toolsets": ["terminal"]},
    {"goal": "Search for CODE REPOS and PAPERS. Run: ddgs text -q 'topic github' -m 5. Also: ddgs text -q 'topic arxiv paper' -m 5. Return ALL URLs.", "toolsets": ["terminal"]},
])
```

**Key pitfalls:**
- Chinese queries via ddgs frequently return empty — always have English fallback queries
- `site:` operator causes fast rate limiting — use plain queries + URL domain filtering
- Add 3s delay between searches to avoid rate limits
- Some subagents may get blocked terminal requests — that's OK, the other subagents compensate

## Content Prioritization

From 80+ discovered URLs, prioritize extraction in this order:

1. **Whitepapers / technical reports** — comprehensive, architecture-level (e.g., DeepLink SuperPod whitepaper)
2. **Official documentation** — authoritative but often JS-rendered, may need creative extraction
3. **In-depth CSDN blogs** — practical, code-level, easy to extract via curl
4. **Source code repos** — ground truth for APIs and algorithms
5. **Zhihu articles** — good insights but hard to extract; use search snippets as fallback
6. **arXiv papers** — academic depth, use for specific technical claims
7. **News/press releases** — use for timeline/context only, not technical depth

## Synthesizing Into Learning Guide

After extraction, you'll have 5-10 substantial content pieces. Synthesize:

1. **Chapter outline first** — what are 4-6 major sub-topics? What's the logical sequence?
2. **One chapter per sub-topic** — 200-400 lines HTML each
3. **Chapter 1 always includes**: motivation, architecture overview, comparison table, resource index (all source URLs)
4. **ASCII diagrams** from extracted content — restructure for clarity
5. **Comparison tables** — the user's most valued content format
6. **Last chapter**: interview Q&A if applicable

## Validated With

- Huawei Ascend HCCL collective communication (2026-06): 83+ URLs → 6 chapters, 128KB
- Sources: DeepLink whitepaper, CSDN blogs, HCCL Gitee repo, arXiv papers, Huawei official docs
