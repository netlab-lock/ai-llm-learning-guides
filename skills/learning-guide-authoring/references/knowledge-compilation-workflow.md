# Knowledge Compilation Workflow (Non-Paper-Survey)

When the user asks to "systematically learn" or "organize knowledge about" a technical topic (not a paper survey), use this workflow instead of the paper survey pipeline.

## When This Applies (vs Paper Survey)

| Signal | Paper Survey (use `research-survey`) | Knowledge Compilation (this workflow) |
|--------|-------------|----------------------|
| User says | "find papers on X" | "learn about X", "systematically organize X" |
| Output | Per-paper entries with arxiv links | Concept explanations with diagrams |
| Structure | Direction → Papers | Topic → Concepts → Code examples |
| Focus | Research frontier | Fundamentals + practical guide |
| Papers needed? | Yes, primary content | Optional, secondary |

Both share: dark-theme HTML, Chinese UI, D:\学习\ storage, topic subdirectories.

## Directory Structure

```
<topic>/
├── index.html                    # Main entry: learning roadmap, overview table, quick start
├── 00-概述与背景/README.html      # What, why, history
├── 01-核心概念/README.html        # Fundamental concepts
├── 02-.../README.html             # One per major topic area
├── ...
└── N-学习资源/README.html         # Papers, blogs, videos, courses, GitHub repos
```

## HTML Template Conventions

Use the same CSS variables and dark theme as learning guides:
- `--bg: #0d1117; --surface: #161b22; --border: #30363d`
- Accent: `--accent: #58a6ff`, Green: `--green: #3fb950`, Orange: `--orange: #d29922`
- Font: `-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`

### Key Components Per Module HTML

1. **Breadcrumb**: `<a href="../index.html">首页</a> / XX - 模块名</a>`
2. **ASCII diagrams**: Use `<pre>` with `white-space: pre` for architecture diagrams, data flow, comparisons
3. **Info/Warn/Tip boxes**: `.box.info` (blue left border), `.box.warn` (orange), `.box.tip` (green)
4. **Comparison tables**: Standard `<table>` with hover effect
5. **Code blocks**: `<pre><code>` with syntax-highlighted commands
6. **Navigation**: `.nav-bottom` with prev/next module links

### Index.html Should Include

- Hero section with stats (module count, framework count, study duration)
- "Why learn this" motivation cards
- ASCII architecture/overview diagram
- Learning roadmap (phased, with time estimates)
- Module card grid (clickable cards linking to each module)
- Quick reference table (frameworks, tools, or key entities)
- Quick start code example (5-min experience)

## Research Phase

Before writing, research the topic. **Two strategies depending on context availability:**

**Strategy A: When you have a key reference document (PDF, tech report)**
- Extract text from the document using `pymupdf` via `terminal` (not `execute_code` — isolated sandbox)
- Supplement with your own domain knowledge
- This is often sufficient for comprehensive guides — no web search needed

**Strategy B: When you need web research**
- Use `delegate_task` with 3 parallel sub-tasks:
  1. Latest overview/comparison of major tools/frameworks in the domain
  2. Core techniques and their technical details
  3. Beginner tutorials, guides, and learning resources
- Budget ~3 min per sub-task. Use `web` toolset.
- **Pitfall**: With mimo-v2.5-pro provider, sub-agents may return minimal results ("I'll search...") without actual content. If sub-agents return <200 chars of useful content, fall back to Strategy A or do direct web searches yourself.

## Content Quality Standards

- Each module should have: 2-3 ASCII diagrams, 1-2 comparison tables, 1-2 code examples
- Explain "why" before "what" — motivation first
- Use concrete numbers (e.g., "60-80% memory wasted") not vague statements
- Code examples should be copy-pasteable (real commands, real model names)
- End each module with a "小结" (summary) box with 5 bullet points
- Link modules sequentially (prev/next navigation)

## Sub-File Splitting (Important)

When a module covers 5+ distinct sub-topics (e.g., 7 types of parallelism, 10 frameworks), **split into multiple focused sub-files** instead of one monolithic HTML. User explicitly requested this for better readability.

**Structure for split modules:**
```
06-并行策略/
├── 00-并行策略总览.html      ← Navigation index with card grid
├── 01-数据并行DP.html        ← One file per sub-topic
├── 02-张量并行TP.html
├── ...
└── README.html               ← Redirect to 00-总览.html
```

**Rules:**
- Each sub-file: 6-12KB, focused on ONE concept
- `00-总览.html`: card-grid navigation + overview table + relationship diagram
- Old `README.html`: redirect to `00-总览.html` via `<meta http-equiv="refresh">`
- Update `index.html` links to point to `00-总览.html` not `README.html`
- Each sub-file has prev/next navigation linking to adjacent sub-files

## Vivid Diagrams for Beginners

Use **metaphor-based ASCII art** with emojis to make complex concepts accessible:

```
🏭 Pipeline Parallelism — 工厂流水线

  👷 工人1         👷 工人2         👷 工人3         👷 工人4
  (GPU 0)          (GPU 1)          (GPU 2)          (GPU 3)
  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
  │ Layer    │     │ Layer    │     │ Layer    │     │ Layer    │
  │ 0 ~ 19   │ ──→ │ 20 ~ 39  │ ──→ │ 40 ~ 59  │ ──→ │ 60 ~ 79  │
  └──────────┘     └──────────┘     └──────────┘     └──────────┘
```

**Good metaphors from this session:**
- DP = 开多个相同的工厂 (multiple identical factories)
- TP = 把蛋糕切成几份 (cutting a cake into pieces)
- PP = 工厂流水线 (assembly line)
- PagedAttention = 快递分拣中心 (delivery sorting center)
- MoE = 专家会诊 (expert consultation)

**Technique:** Start with the metaphor, then show the technical diagram, then the formal formula.

## Strategy C: Doc-Site Crawl for Specialized Domains (NEW 2026-06)

When the user wants to learn a **specialized/niche domain** where public web resources are scarce (e.g., Huawei Ascend internals, proprietary chip architecture, vendor-specific protocols), the knowledge lives in specific doc sites, repos, whitepapers, and community blogs — not in general search results.

### When This Applies

| Signal | Strategy A (Reference doc) | Strategy B (Web research) | Strategy C (Doc-site crawl) |
|--------|---------------------------|--------------------------|----------------------------|
| User says | "学习这个PDF" | "系统学习X" | "学习X专有技术" |
| Content source | One key document | General web | Specific doc sites/repos |
| Discovery needed? | No | Moderate | High — need to find 80+ URLs |
| Extraction complexity | Low | Low | High — JS-rendered sites, login walls |

### Workflow (5 Phases)

**Phase 1: Multi-Source Discovery (parallel search)**
- Use `delegate_task` with 3 parallel subagents, each searching different angles:
  1. Official documentation URLs (site:huawei.com, site:hiascend.com, etc.)
  2. Community blogs (CSDN, Zhihu, Huawei Cloud BBS)
  3. GitHub/Gitee repos + academic papers (arXiv)
- **Always search in BOTH Chinese AND English** — Chinese queries via ddgs often return empty; English fallback is essential
- Collect ALL URLs with one-line descriptions — aim for 50-100+ URLs
- Budget: ~4 min per subagent

**Phase 2: Selective Extraction (browser + curl)**
- NOT all URLs are worth extracting — prioritize:
  1. Official documentation (authoritative, structured)
  2. Whitepapers / technical reports (comprehensive, architecture-level)
  3. In-depth blog posts (practical, code-level)
  4. Source code repos (ground truth)
- Use `curl` for simple HTML sites (CSDN, blogs) — faster, no JS issues
- Use `browser_navigate` + `browser_snapshot` for JS-rendered sites (official docs, MkDocs sites)
- **Pitfall**: Many Chinese tech doc sites use heavy JS rendering — `curl` returns empty body, browser gets sidebar only. Workaround: try multiple approaches, don't give up on first failure.

**Phase 3: Knowledge Synthesis**
- From 80+ URLs, you'll extract ~5-10 substantial content pieces
- Synthesize into a **chapter outline** before writing:
  - What are the 4-6 major sub-topics?
  - What's the logical learning sequence?
  - Where do sources agree/disagree?
- Each chapter = one focused HTML file (200-400 lines)
- Total: 5-7 chapters forming a complete learning path

**Phase 4: HTML Generation**
- Follow standard learning-guide-authoring conventions (dark theme, Chinese UI)
- Each chapter should have: ASCII diagrams, comparison tables, code examples
- Include a **资料索引** section in chapter 1 listing all source URLs
- Use prev/next navigation linking all chapters

**Phase 5: Verification**
- Verify all URLs in the guide are accessible
- Check ASCII diagrams render correctly in browser
- Ensure cross-chapter navigation works

### Site-Specific Extraction Patterns

See `references/doc-site-extraction-patterns.md` for tested patterns for Chinese tech sites (Huawei, CSDN, Zhihu, etc.).

## Pitfalls

- Don't mix paper survey content (per-paper entries) into knowledge compilation
- ASCII diagrams need monospace font and `white-space: pre` — test rendering
- **Split large modules** (5+ sub-topics) into focused sub-files with card-grid index
- Chinese model names (Qwen, DeepSeek) are more relatable than English-only examples
- Include both GPU and CPU paths in practical guides (not everyone has GPUs)
- When writing HTML with f-strings, escape curly braces in JSON examples (use `{{` and `}}`)
- Card-grid navigation pages need `text-decoration:none;color:inherit` on `<a>` tags to look right
- **execute_code sandbox is isolated** — Python packages installed in terminal are NOT available there. Use `terminal` for PDF extraction / data processing, `write_file` for HTML creation
- **write_file tool is preferred** over execute_code for creating HTML files — more reliable, no sandbox environment issues
