# Web Research Patterns for Learning Guides

## ddgs (DuckDuckGo Search) Reliability Issues

### Problem
ddgs CLI frequently fails with Chinese-language queries:
- `DDGSException('No results found.')` — common for Chinese strings
- `TimeoutException` — intermittent, affects all query languages
- Results are inconsistent — same query may fail then succeed minutes later

### Workarounds (in priority order)

1. **Use English queries** for the same topic
   - Bad: `ddgs text -k "DeepSeek V4 架构 CSA HCA"`
   - Good: `ddgs text -k "DeepSeek V4 architecture CSA HCA technical report"`
   - English queries return 5-10x more results consistently

2. **Try multiple query formulations**
   - Use `-m 10` to get more results
   - Vary keywords: "technical report" vs "paper" vs "architecture"
   - Add year: "2026" helps filter stale results

3. **Batch with timeout tolerance**
   - Run 3-5 queries in parallel via delegate_task
   - If a batch fails, wait 30 seconds and retry
   - Don't rely on a single query for critical information

4. **Fetch specific articles directly**
   - After initial search identifies key URLs, use `terminal("curl -sL URL")` or `web_extract`
   - Official sources: `site:huggingface.co`, `site:arxiv.org`, `site:github.com`
   - Chinese tech blogs: zhihu.com, csdn.net, juejin.cn often have detailed analysis

5. **Cross-validate across sources**
   - Model parameters may differ between sources (official vs blog vs Wikipedia)
   - Prefer official technical reports > arxiv papers > blog posts
   - Note discrepancies in the guide with footnotes

## Search Strategy for Model Updates

When researching the latest models from Chinese vendors:

1. **First pass**: English queries for each vendor + "2026 latest model"
2. **Second pass**: Specific technical terms (architecture names, optimizer names)
3. **Third pass**: Chinese queries for domestic coverage (may fail, retry)

## Data Validation Checklist

Before including model specs in the guide:
- [ ] Cross-check parameters across 2+ sources
- [ ] Verify release date from official announcement
- [ ] Confirm open-source license from HuggingFace/GitHub
- [ ] Check if "latest" claim is still current
- [ ] Note if data comes from leaks/rumors vs official sources
