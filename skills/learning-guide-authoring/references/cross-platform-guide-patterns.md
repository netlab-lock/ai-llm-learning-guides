# Cross-Platform Comparison Guide Patterns

## When to Use
When the user wants to learn the same technical domain across competing platforms (e.g., NVIDIA vs Huawei, PyTorch vs JAX, AWS vs GCP).

## Parallel Guide Structure
Each platform gets its own complete guide directory with cross-links:

```
D:\学习\
├── PlatformA集合通信\
│   ├── 00-资料索引.html      ← Dedicated resource index (100+ URLs)
│   ├── 01-架构总览.html
│   ├── 02-核心技术.html
│   ├── ...
│   └── 06-对比与面试.html    ← Cross-platform comparison + interview
├── PlatformB集合通信\
│   ├── 00-资料索引.html
│   ├── 01-架构总览.html
│   ├── ...
│   └── 06-面试专题.html      ← Cross-platform comparison
```

## Key Design Decisions

### 1. Separate Directories, Not Merged
Each platform gets its own complete guide. Reasons:
- Each platform has enough depth for 6+ chapters
- Merging creates unwieldy 1000+ line files
- Users may only need one platform initially
- Cross-references connect them when needed

### 2. Cross-Link Navigation
Every file's nav bar links to the other platform's guide:
```html
<li style="margin-top:12px;border-top:1px solid var(--border);padding-top:12px">
  📖 <a href="/path/to/other/guide/01-架构总览.html">Other Platform系列指南</a>
</li>
```

### 3. Comparison Chapter in Each Guide
Each guide's final chapter (06-对比与面试) covers:
- Side-by-side spec tables
- Architecture philosophy comparison (not just numbers)
- "Which to use when" decision framework
- Interview questions covering BOTH platforms

### 4. Resource Index Chapter (00-资料索引.html)
For specialized domains with 80+ source URLs, create a dedicated index page:
- Categories: Official Docs, GitHub Repos, Technical Blogs, Whitepapers, Academic Papers, GTC/Talks
- Each entry: name, URL, one-line description
- Statistics: total URL count per category
- Comparison table: what sources each platform has

### 5. Same CSS Theme
Both platforms use identical dark theme CSS for visual consistency.

## Research Workflow
1. Search and create Platform A guide first (establishes CSS/template)
2. Search and create Platform B guide using same structure
3. Create comparison chapters last (need both platforms' data)
4. Cross-validate claims across platforms
5. Create resource index pages for both

## Source Collection Density
For specialized/proprietary domains, aim for **80+ verified URLs** per platform:
- Official docs: 10-15 URLs (test each for HTTP 200)
- GitHub/Gitee repos: 5-10 URLs
- Developer blogs: 15-20 URLs (NVIDIA Developer Blog, CSDN, Zhihu)
- Whitepapers: 3-5 URLs (architecture, protocol specs)
- Academic papers: 20-30 URLs (arXiv IDs)
- Technical sites: 5-10 URLs (TechPowerUp, ServeTheHome, etc.)
- Conference talks: 2-3 URLs (GTC, Hot Chips)

## Subagent Research Pattern
Use 3 parallel delegate_task subagents for URL collection:
1. Official docs + repos (test URLs directly)
2. Technical blogs + analysis articles (search via ddgs)
3. Academic papers (search arXiv)

Each subagent returns URLs with descriptions. Main agent deduplicates and verifies.

## Pitfalls
- **Don't merge platforms** — each has enough depth for standalone guides
- **Don't skip the resource index** — specialized domains need curated URL collections
- **Cross-validate** — don't trust one platform's claims about the other; verify independently
- **Subagent timeout** — always check for partial output before retrying (subagent may have created 3-8 files before timeout)
- **Old files after renaming** — when rewriting a chapter with a better name, delete the old file (e.g., 01-NVLink与NVSwitch架构.html → 01-GPU架构与互联技术.html)
