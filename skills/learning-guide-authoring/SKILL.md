---
name: learning-guide-authoring
description: Create structured HTML learning guides — dark-themed, Chinese, self-contained, with navigation, diagrams, code blocks, and hands-on exercises. For technical topic deep-dives (not paper surveys).
tags: [html, learning, guide, dark-theme, chinese, study-material, tutorial]
triggers:
  - "学习指南 / learning guide"
  - "系统学习 / systematic study"
  - "入门教程 / beginner tutorial"
  - "create a study guide for X"
  - "from-zero learning path"
  - "调研X厂商 / survey providers in domain X"
  - "国产LLM / Chinese LLM providers"
  - "模型发展历史 / model development history"
  - "各厂商对比 / compare all providers"
  - "修复index.html / fix index / audit index / 整理目录"
  - "面试准备 / interview preparation"
  - "面试题 / interview questions"
  - "查缺补漏 / audit guide / 补充内容 / enhance guide"
  - "补充知识点 / add knowledge points"
  - "整理目录 / 整理学习内容 / summarize guide"
  - "写书的深度 / 更详尽 / 更深入 / book-level depth"
  - "SVG图 / 架构图 / 升级图 / diagram upgrade"
  - "对比NVIDIA / NVIDIA vs 华为 / 跨平台对比 / cross-platform comparison / parallel guides"
  - "批量增强 / B级升级 / 补充教学元素 / batch enhance / upgrade B-level"
  - "检查现有指南 / 审计指南 / audit guide quality / 检查做得怎么样"
  - "调研最新进展 / update guide with latest / 2026更新 / 补充最新内容"
  - "推理框架 / inference framework / vLLM / SGLang / Dynamo"
# Audit workflow detail → references/audit-workflow.md (file search + ddgs web research + P0/P1/P2 report)
  - "深度学习指南 / deep dive guide / 技术深度学习"
  - "空壳文件 / empty shell / 薄弱文件 / thin file"
  - "跨章节交叉引用 / cross-reference / 知识孤岛"
  - "资料索引 / 资源索引 / URL汇总 / resource index / source collection"
  - "源码级分析 / source code analysis / 读源码"
---

## Pitfalls (see also: references/pitfalls-and-patterns.md)

- Subagent timeout: Use execute_code+write_file for batch file creation (5+ files)
- Stay on task: Complete primary goal before exploring tangential activities
- Large project: Audit → index pages → cross-references → fill gaps

---

# Learning Guide Authoring

Create comprehensive, self-contained HTML learning guides for technical topics. Dark theme, Chinese content, beginner-friendly with ASCII diagrams and hands-on exercises.

**CRITICAL**: Read `references/depth-requirements.md` before starting any guide. The user expects paper-level depth (论文级深度) — every topic needs architecture diagrams, exact benchmark numbers, comparison tables, pricing, limitations, and learning notes. Do NOT produce shallow overviews.

### Linked References (read before starting)
- `references/breadth-depth-audit-methodology.md` — Two-dimensional audit: breadth (keyword coverage) + depth (marker counting for 为什么/工作方式/公式/代码/etc). Use when reviewing/enriching existing guides.
- `references/svg-python-generation-patterns.md` — Reusable SVG helpers (box/arrow/txt), color table, batch upgrade, f-string pitfall. Also see `svg-generation-patterns.md` for string-concat templates and HTML tag audit pitfall.
- `references/svg-diagram-integration.md` — SVG diagram design system for upgrading ASCII to professional SVG
- `references/depth-audit-methodology.md` — How to audit and enrich modules to "book-level depth"
- `references/multi-vendor-deep-dive-workflow.md` — Validated workflow for creating 60+ files across 5+ vendors: directory structure, index-first, subagent chapters, cross-references, timeout handling. Includes subagent partial output discovery pattern (check what was created before retrying).
- `references/multi-module-architecture.md` — Multi-file guide structure (高内聚低耦合)
- `references/8-dimension-teaching-framework.md` — 8 dimensions for each knowledge point
- `references/p3-guide-css-template.md` — Standard CSS template for dark-themed guides
- `references/proprietary-domain-research.md` — Three-layer explanation methodology (analogy→technical→math) and specialized domain source hierarchy (Gitee, JS-rendered docs, developer blogs). Read when creating guides for proprietary/hardware topics.

**CRITICAL**: Read `references/large-guide-workflow.md` before creating guides >50KB. Covers iterative depth expansion, large HTML file manipulation, and search strategies for fast-moving topics.

## When to Use

User wants a structured, multi-module learning resource for a technical topic. NOT for paper surveys (use `research-survey` instead). This is for "learning guide" or "study guide" creation — deep technical content with structured modules, not paper summaries.

Also use when user asks to "分块建HTML" (split into modular HTML), demands "高内聚低耦合" (high cohesion, low coupling), or wants a multi-file knowledge base with cross-references.

**MODULAR STRUCTURE:** For broad domains, split into multiple self-contained HTML files (high cohesion, low coupling). See `references/modular-structure.md` for the full pattern, pitfalls, and audit workflow. User explicitly prefers this over monolithic single-file guides.

For non-technical domains (finance, law, health, career), see `references/non-technical-domain-patterns.md` for adapted content structures (product tables, risk ratings, lifecycle frameworks instead of code/formulas/benchmarks).

**Also use for multi-provider domain surveys** — when the user asks to "调研所有X厂商" (survey all providers in a domain), compile model development histories, or create comparison reports across companies. These are knowledge compilation tasks, not paper surveys. See `references/multi-provider-survey-pattern.md` for the template covering: provider list, timeline, key technologies, comparison tables. For LLM provider surveys specifically, see `references/llm-provider-chapter-template.md` for the standard 11-chapter structure covering architecture→training→alignment→deployment→evaluation→ecosystem. For paper-based deep dives, download PDFs from arxiv/HuggingFace and extract text with pymupdf — see `parallel-subagent-research` skill for the full workflow.

## User Preferences (critical)

- **Format**: Dark-themed HTML with embedded CSS (NOT Markdown)
- **Language**: Chinese section headers and explanations throughout
- **Location**: `D:\\学习\\<topic-name>\\` (Windows path, `D:\\` is a learning drive)
- **Style**: Beginner-friendly with analogies, ASCII architecture diagrams, comparison tables
- **通俗易懂 (MUST)**: Every technical concept MUST have THREE layers of explanation:
  1. **通俗类比 (Analogy)** — A everyday life comparison that builds intuition. E.g., "工厂" for AI Core, "快递柜" for Jetty, "食堂排队" for weak ordering, "快递费=起步价+重量费" for α-β model
  2. **技术原理 (Technical)** — ASCII diagrams, tables, step-by-step mechanism explanation
  3. **数学/本质 (Mathematical)** — Formal proofs, complexity analysis, design rationale
  The user explicitly said "不要浮于表面" — the analogy layer is NOT optional decoration, it's the entry point for understanding. Without it, even technically correct content fails.
- **Structure**: Progressive learning path (basics → intermediate → advanced → practice)
- **Depth**: Bottom-up, not top-down. Always cover foundational knowledge before frontier topics. User explicitly rejects "高屋建瓴" (lofty/high-level-only) guides. A guide that only lists hot topics without explaining prerequisites is incomplete.
- **Data freshness**: For rapidly-evolving fields (LLM, AI, ML), ALWAYS verify information with fresh web searches. Do NOT rely on training data alone — the user will notice and reject outdated info. Search before writing, cite sources in the guide.
- **Scope control**: When the user specifies a focus (e.g., "侧重硬件架构和通信算法，实战部署可以不重点讲解"), adjust the module plan accordingly — reduce or remove modules in the de-emphasized area, expand the focused areas. Don't present the full plan and ask "is this OK?" — just adjust and start creating.

## Output Structure

Flat layout (simple guides, 10-15 modules):
```
D:\学习\<topic-name>\
├── index.html              ← Main page (overview, roadmap, resource links)
├── 01-模块名.html           ← Module 1
├── 02-模块名.html           ← Module 2
├── ...
└── NN-模块名.html           ← Module N
```

Sub-directory layout (detailed guides, 30+ files):
```
D:\学习\<topic-name>\
├── index.html
├── 01-模块名/
│   ├── 00-总览.html          ← Module overview + knowledge map
│   ├── 01-子主题A.html       ← Deep dive
│   ├── 02-子主题B.html
│   └── README.html           ← Original (can be kept or removed)
├── 02-模块名/
│   ├── 00-总览.html
│   └── ...
```

Use sub-directory layout when modules need 3+ sub-topics or when total files exceed 20.

Typical guide: 10-15 modules, each 12-30KB, total 200-400KB.

## Authoring Workflow

### Step 0: Hands-On Project Trial Guide Pattern (项目试玩指南)
When the user wants to "try out" a GitHub project (e.g., Browser Use, Graphify), follow this sequence:
1. **You install and run it first** — don't just give instructions, actually run the install commands and demo
2. **Hit errors and fix them in front of the user** — this teaches real-world troubleshooting (e.g., MiMo doesn't support image input → use_vision=False)
3. **Write the guide AFTER the trial** — embed the actual errors you hit and solutions you found, not theoretical issues
4. **Include "your environment" section** — with exact paths, versions, and run commands specific to the user's machine
5. **Include runnable demo scripts** — put them on Desktop or a known location, with exact run commands

**Guide structure for project trial guides** (single-page, not multi-module):
- 项目信息 (links, stars, description)
- 环境要求 (Python version, browser, API key)
- 安装步骤 (numbered steps with exact commands)
- 第一个脚本 (fully commented, ready to copy-paste)
- 核心概念 (what Agent/LLM/vision mean in this context)
- 常用任务示例 (5 practical examples)
- 进阶配置 (different LLM providers)
- 常见问题 FAQ (based on errors YOU actually hit)
- 你的环境信息 (installed versions, paths, run commands)

**Critical**: User explicitly corrected "请务必写好项目指南，因为到现在都是你在操作项目，我本人还属于完全不会操作" — when trying out projects, the user wants to LEARN, not just watch. Write guides they can follow independently.

### Step 0a: Specialized Domain Research (专有领域资料采集)
When the topic is a **proprietary/specialized domain** (e.g., Huawei Ascend, specific hardware platforms, niche protocols) where public web resources are scarce:

**Source priority (in order)**:
1. **Official documentation sites** — e.g., `hiascend.com`, `docs.nvidia.com`. Note: many Chinese tech docs sites are **JS-rendered** and won't return content via `curl`. Use `browser_navigate` + `browser_snapshot` instead.
2. **Source code repos** — Search Gitee (gitee.com) for Chinese companies, GitHub for others. Look for `docs/` directories and README.md files in repos. E.g., `gitee.com/ascend/cann-hccl/blob/master/docs/Ring.md`
3. **Academic papers** — arXiv for official papers (e.g., `arXiv:2506.12708` for CloudMatrix384). Use `curl` to fetch abstracts.
4. **Community blogs** — CSDN (blog.csdn.net), Zhihu (zhuanlan.zhihu.com), Huawei Cloud BBS (bbs.huaweicloud.cn). CSDN articles are usually accessible via `curl`; Zhihu requires browser.
5. **Industry analysis** — Substack, Medium, specialized analysis sites (e.g., China Research Collective, SemiAnalysis)
6. **Developer personal blogs** — Often the deepest technical content. E.g., Bojie Li's blog (01.me) had the best UB protocol analysis.

**Search strategy**: Run 3 parallel delegate_task searches with different language/query angles:
- Chinese queries for domestic platforms/docs
- English queries for international papers/analysis
- Technical term queries for source code/repos

**JS-rendered site workaround**: When `curl` returns empty/minimal content for a doc site:
1. Try `browser_navigate` + `browser_snapshot` (may work for some JS sites)
2. Search for cached/mirrored versions: `ddgs text -q 'site:cached: URL'`
3. Search for the specific page title to find cross-posted content on accessible platforms
4. Look for the source repo (many doc sites have a GitHub/Gitee source)

**Pitfall**: Don't rely on a single source. Proprietary domains often have information scattered across official docs (architecture overview), source code (implementation details), papers (benchmark data), and blogs (design rationale). Synthesize from all sources.

### Step 0b: Verify Knowledge Freshness (for rapidly-evolving fields)
When the topic is in a fast-moving field (LLM, AI, ML, etc.), search for the latest developments BEFORE writing. Use **parallel subagents** for efficiency:

```python
delegate_task(tasks=[
  {"goal": "Search for latest [topic] techniques 2024-2025 via ddgs CLI", "toolsets": ["terminal"]},
  {"goal": "Search for latest [topic] developments 2024-2025 via ddgs CLI", "toolsets": ["terminal"]},
  {"goal": "Search for trending [topic] research 2024-2025 via ddgs CLI", "toolsets": ["terminal"]}
])
```
Each subagent runs `ddgs text -q '...' -m 3`. 3 parallel subagents complete in ~80-100s.
Cross-check any training-data claims against search results. If search reveals newer information, use the search results. Cite sources (arXiv IDs, URLs) in the guide.

**ddgs Chinese query pitfall**: DuckDuckGo search often returns no results for Chinese-language queries. Workaround: use English queries with Chinese technical terms (e.g., "GLM-5 zhipu 2026 latest model" instead of "智谱 GLM-5 最新模型"). Fallback: search for the English name of the model/company.

**MiMo API key discovery**: The MiMo API key is stored in `~/.hermes/auth.json` under `credentials[].label == "XIAOMI_API_KEY"` with the key in `access_token` field. It is NOT in environment variables. The base URL is configured in `~/.hermes/config.yaml` under `model.base_url`. To extract programmatically:
```python
import json
with open('/home/atios/.hermes/auth.json') as f:
    data = json.load(f)
for item in data.get('credentials', []):
    if item.get('label') == 'XIAOMI_API_KEY':
        api_key = item.get('access_token', '')
```

### Step 0b: Concept-First Explanation Pattern (概念先行模式)
### Step 0b: Concept-First Explanation Pattern (概念先行模式)
When the user says "我对这个技术点的背景完全不了解" or asks "这一般用在什么场景" before any HTML is created:
1. **Explain conversationally first** — use ASCII diagrams, analogies, and progressive disclosure in the chat
2. **Wait for the user to ask follow-up questions** — they will often ask about related techniques, comparisons, or scenarios
3. **Disambiguate similar-sounding concepts proactively** — e.g., Chunked Prefill vs Context Parallelism, GQA vs MLA. Users WILL confuse them
4. **Present the full landscape** — when the user asks "还有其他技术吗?", show the complete taxonomy (not just the one topic they asked about). This helps them choose what to include in the guide
5. **Only create HTML after the user signals readiness** (e.g., "把这些都写进指南", "继续")

This pattern is especially important for LLM inference topics where terminology overlaps (Prefill/Decode, Chunked/Parallel, Cache/Buffer).

**Pitfall: Do NOT force conversational teaching when user wants the guide directly.** Some users (especially those requesting "系统性学习") want the structured HTML guide itself — not a CLI dialogue. If the user says "写成指南" or "不要再cli里面试图教会我", skip the conversational phase entirely and go straight to HTML creation. The concept-first pattern is for users who want interactive Q&A; it is NOT appropriate when the user explicitly asks for a self-study document.

### Step 1 (alternate): Conversation-First Draft Pattern
When the topic is fast-moving and the user wants search-verified content, use this workflow:
1. **Search first**: Run multiple `ddgs` searches to gather fresh data
2. **Draft in conversation**: Present the full content outline as plain text in the conversation — NOT as HTML files yet
3. **Let user review**: User may correct structure, add/remove topics, or request more search verification
4. **Then convert to HTML**: Only after the user approves the content, create the HTML files

This avoids creating 12 HTML files with wrong/outdated content and having to redo them. The user's correction "不要高屋建瓴" came AFTER the initial draft — if HTML had been created first, all files would need rewriting.

### Step 1 (alternate): Conversational Deep-Dive Pattern
When the user says "我对这个技术点完全不了解" or "从零讲起", they want to **understand the topic conversationally first** before any HTML is created. This is a multi-turn teaching flow:

1. **Explain the problem**: Start with "why does this technology exist?" — the pain point it solves. Use analogies (餐厅大桌 vs 回转寿司 for batching).
2. **Explain the solution**: How does the technology solve it? Use ASCII diagrams inline in the conversation.
3. **Let user ask follow-ups**: The user will naturally ask "what scenarios?" / "are there alternatives?" / "how does it compare to X?" — answer each in detail.
4. **Repeat for related topics**: User often chains questions (batching → chunked prefill → CP → FlashAttention). Each gets the same treatment.
5. **Create HTML only when user says "先写进html吧"**: Don't rush to create files. The conversational understanding IS the deliverable until the user explicitly asks for HTML.

Key signals from this session:
- User asked "它一般用在什么场景呢" → wants use-case context, not just theory
- User asked "就它一个常见技术点吗" → wants to understand the landscape, not just one technique
- User asked "CP是不是也能解决上述问题" → wants to understand relationships between techniques
- User asked "介绍一下名字由来，以及背后的原理" → wants deep technical + historical context

**Rule**: When the user is learning a topic from zero, spend 3-5 turns on conversational explanation before creating any HTML. The HTML should embed the depth of the conversation, not be a shallow placeholder.

**EXCEPTION — Override signal: "写成指南" / "写成html"**: If the user explicitly says they want a guide created (e.g., "写成指南", "写成html", "不要在cli里面试图教会我", "直接写指南"), skip the conversational teaching entirely and start creating HTML immediately. Some users find CLI-based teaching frustrating — they want the structured guide, not a chat. Read the room: if the user pushes back on conversational explanation, that IS the signal to create. Do NOT try to squeeze in more explanation first.

### Step 0c: Prerequisite Knowledge Assessment (领域前置知识评估)
When creating a paper-based or domain-specific guide, **assess whether the user has the prerequisite knowledge** to understand the source material. Signals that prerequisites are needed:
- User says "我在这个领域是小白" / "完全不懂XX"
- The paper uses domain-specific jargon (e.g., MOSFET, TSV, hybrid bonding) without explanation
- The topic spans multiple technical layers (device physics → circuit design → system architecture)

**When prerequisites are needed**: Create a `00-基础知识入门.html` module FIRST (before the main content modules). This module should:
1. Cover every domain-specific term/concept that appears in the main guide but isn't explained there
2. Use heavy analogies and visual diagrams — the user explicitly said they're a beginner
3. Map each prerequisite concept to where it's used in the main guide ("这个概念在第3章逻辑折叠中会用到")
4. Include a "概念速查表" (concept lookup table) at the end

**Don't wait for the user to ask for it** — if the topic is clearly domain-specific (hardware, semiconductor, networking, etc.) and the user hasn't demonstrated expertise, include the prerequisite module in the initial plan. The user asking "补充基础知识" after the guide is done means you missed the signal earlier.

### Step 1 (alternate): Reference Directory Deep-Dive Pattern
When user says "给每个知识点都新建一个目录" or "参照 XX 的结构", they want EACH knowledge point to be its own directory with the same depth as the reference. This is the most labor-intensive pattern — 50+ files total.

**Target structure per knowledge point directory**:
```
01-TopicName/
├── 01-SubTopicA.html    (核心概念 + 数学 + ASCII图)
├── 02-SubTopicB.html    (技术演进 + 对比表)
├── 03-SubTopicC.html    (代码示例 + 实现细节)
├── 04-SubTopicD.html    (前沿进展 + 搜索验证)
└── 05-总结与练习.html    (回顾表 + 练习题 + 误区)
```
Each sub-file: 5-10KB, with nav links to prev/next and back to directory index.

### Step 2: Plan Module Structure
Decide 10-15 modules in a logical progression:
- Phase 1 (基础入门): 2-3 foundational modules
- Phase 2 (核心概念): 4-5 core concept modules
- Phase 3 (进阶原理): 3-4 advanced modules
- Phase 4 (实战应用): 1-2 hands-on modules

### Step 2: Create index.html First
The index page serves as the table of contents and learning roadmap. Include:
- Hero section with title and badges
- "Learning goals" cards (what you'll achieve)
- Module cards with phase tags, descriptions, and tags
- Recommended resources (official docs, videos, books, practice platforms)
- Certification paths (if applicable)
- Learning tips
- Progress tracker

### Step 3: Create Module Files in Batches
**IMPORTANT**: Do NOT use `delegate_task` for HTML generation — mimo-v2.5-pro API timeouts (600s) make sub-agents unreliable. Even single-file generation tasks timeout on mimo.

**Recommended approach for 10+ files**: Write Python scripts to `/tmp/gen_batchN.py` and execute via `terminal("python3 /tmp/gen_batchN.py")`. Each script handles 2-3 modules:
1. Extract CSS from an existing file via `open(existing_file).read().split("<style>")[1].split("</style>")[0]`
2. Define a `hp(title, prev, nxt, nav, body)` template function
3. Define a `w(path, content)` helper that writes and prints file size
4. Call `w()` for each module with full HTML body content
5. Run via terminal — each batch takes ~1-2 seconds

This is 5-10× faster than individual `write_file` calls and avoids the announce-then-stall anti-pattern (pitfall #29).

**Alternative**: Use `write_file` tool directly for each module. Fine for 5-15 files, but slow for 20+.

**Recommended approach — Python script via terminal:**
1. Write a Python script to `/tmp/gen_XX.py` that defines CSS + template function + model content
2. Run via `terminal("python3 /tmp/gen_XX.py")`
3. Each script should handle 2-3 modules (script size ~20-25KB)
4. Extract CSS from an existing file in the guide for consistency
5. The template function `hp(title, prev, nxt, nav, body)` wraps content with nav/footer

**Alternative — direct write_file:** Use the `write_file` tool directly for each module. Each module takes ~1 second to write. Fine for 5-15 files, but slow for 20+. Use the Python script approach for large batches.

The `execute_code` sandbox has a **separate Python environment** from the terminal — packages installed via `pip3 install --break-system-packages` in terminal are NOT available in execute_code. If you need Python libraries (pymupdf, etc.), use `terminal` commands, not `execute_code`.

## Content Depth Standard (8-Dimension Framework + Three-Layer Method)

Every knowledge-point module MUST follow this 8-dimension framework as the DEFAULT depth standard. Do NOT create shallow content that requires later deepening — the user will reject it.

**CRITICAL — Three-Layer Explanation (三层解释法)**: Every technical concept MUST be explained at three layers. See `references/proprietary-domain-research.md` for the full methodology with 14 worked examples.
1. **通俗类比** — Everyday analogy that builds intuition (e.g., "工厂" for AI Core, "快递柜" for Jetty)
2. **技术原理** — ASCII diagrams, tables, step-by-step mechanism
3. **数学/本质** — Formal proof, complexity analysis, design rationale

Use `<div class="callout-tip"><strong>通俗理解：</strong>...</div>` for the analogy layer. This is NOT decoration — it's the entry point for understanding.

1. **背景与动机** — Why does this technology exist? Quantify the problem it solves (real numbers, not vague claims).
2. **名字由来** — Etymology of the term. English word breakdown, historical origin.
3. **核心原理** — How it works fundamentally. ASCII diagrams, analogies, step-by-step explanation.
4. **技术细节** — Real parameters, formulas, specs tables, protocol details. This is the deepest section.
5. **使用场景** — Where it's used in practice. Map to specific products/systems/configurations.
6. **相似技术对比** — Comparison tables with alternatives. Pros/cons.
7. **关联技术** — How it relates to other topics in the guide. Dependencies and interactions.
8. **实际效果** — Real performance numbers. Quantified impact on training/inference speed.

**Target file size**: 15-20KB per module for technical content. Anything under 12KB is too shallow.

**Focus area control**: When the user specifies a focus (e.g., "侧重硬件架构和通信算法，实战部署不重点讲解"), redistribute depth accordingly. Expand focus-area modules to 18-25KB, compress non-focus areas to 10-12KB with a brief overview + pointer to focus modules.

## Module HTML Template

Every module file MUST have:

1. **Navigation bar** (sticky top): `← Previous | Module Title | Next →`
2. **h1**: Module title with emoji
3. **h2 sections**: 5-10 major sections
4. **ASCII diagrams**: Architecture diagrams, flow charts, comparisons
5. **Tables**: For comparisons, command references, concept summaries
6. **Code blocks**: With syntax highlighting spans (`.keyword`, `.string`, `.comment`, `.cmd`)
7. **Tip/Warning/Exercise boxes**: Colored left-border boxes
8. **Summary table**: At the end, one-row-per-concept
9. **Next/Prev links**: At bottom
10. **Footer**: Link back to index.html

### CSS Standard Classes

Full CSS at `templates/dark-theme.css`. Inline summary:
h2 { color: #f0f6fc; border-left: 4px solid #58a6ff; }
code { background: #21262d; color: #79c0ff; }
pre { background: #161b22; border: 1px solid #30363d; }
.keyword { color: #ff7b72; }
.string { color: #a5d6ff; }
.comment { color: #8b949e; }
.cmd { color: #79c0ff; }

/* Info boxes */
.tip { background: #0d1d30; border-left: 4px solid #58a6ff; }
.warn { background: #2d1b00; border-left: 4px solid #d29922; }
.exercise { background: #0d2818; border-left: 4px solid #238636; }
.deep { background: #1a1024; border-left: 4px solid #a371f7; }  /* 深入/历史背景 */

/* ASCII diagrams */
.ascii { background: #161b22; border: 1px solid #30363d; font-family: monospace; }

/* Navigation */
.nav { background: #161b22; border-bottom: 1px solid #30363d; position: sticky; top: 0; }
.next-prev { display: flex; justify-content: space-between; border-top: 1px solid #21262d; }
```

Use `.deep` (purple) for historical background, deep-dive technical details, and "why it had to be this way" explanations. It complements `.tip` (blue, practical advice), `.warn` (yellow, pitfalls), and `.exercise` (green, practice problems).

## Enhancing Existing Shallow Files (Audit & Rewrite Pattern)

When the user reports that existing guide files are technically shallow:

### Step 1: Audit all files for depth
```bash
cd /mnt/d/学习/国产LLM系列
for dir in */; do
  vendor="${dir%/}"
  for f in "$vendor"/*.html; do
    fn=$(basename "$f")
    [[ "$fn" == "index.html" || "$fn" == 学习指南* ]] && continue
    lines=$(wc -l < "$f")
    tech=$(grep -ciE '(attention|softmax|layernorm|embedding|gradient|loss|token|parameter|激活|归一化|梯度|注意力)' "$f" 2>/dev/null || echo 0)
    if [ "$lines" -lt 150 ] && [ "$tech" -lt 10 ]; then
      echo "SHALLOW: $f (${lines}L, ${tech} tech-terms)"
    fi
  done
done
```

### Step 2: Check HTML structural integrity
```bash
# Tag balance check
for f in $(find . -name "*.html" ! -name "index.html" ! -name "学习指南*" | sort); do
  opens=$(grep -o '<div' "$f" | wc -l)
  closes=$(grep -o '</div>' "$f" | wc -l)
  [ "$opens" -ne "$closes" ] && echo "DIV MISMATCH: $f (open=$opens, close=$closes)"
  topens=$(grep -o '<table' "$f" | wc -l)
  tcloses=$(grep -o '</table>' "$f" | wc -l)
  [ "$topens" -ne "$tcloses" ] && echo "TABLE MISMATCH: $f (open=$topens, close=$tcloses)"
done
# Broken link check
for f in $(find . -name "*.html" | sort); do
  links=$(grep -oP 'href="[^"]*\.html"' "$f" | sed 's/href="//;s/"//' | grep -v '^http' | grep -v '^#')
  dir=$(dirname "$f")
  for link in $links; do
    [ ! -f "$dir/$link" ] && echo "BROKEN LINK: $f -> $link"
  done
done
```

### Step 3: Research real technical details
Use `ddgs` CLI to search for papers, GitHub repos, blog posts. Prefer arXiv papers (architecture, training details), GitHub READMEs (model configs), and technical blogs (DeepWiki, Medium).

### Step 4: Enhance files via execute_code + write_file
**This is the preferred pattern for batch file generation** — faster than individual `write_file` calls and more reliable than `delegate_task` subagents (which timeout at 600s on mimo).

```python
from hermes_tools import terminal, write_file

# Extract CSS from existing file (reuse for consistency)
r = terminal("sed -n '/<style>/,/<\\/style>/p' '/path/to/existing.html'")
CSS = r["output"].split("<style>")[1].split("</style>")[0]

def hp(title, prev_file, next_file, nav_title, body):
    pv = '<a href="'+prev_file+'">&larr; '+prev_file.replace('.html','')+'</a>' if prev_file else '<span></span>'
    nx = '<a href="'+next_file+'">'+next_file.replace('.html','')+' &rarr;</a>' if next_file else '<span></span>'
    return ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>'+title+' | Guide</title>\n<style>'+CSS+'</style>\n</head>\n<body>\n'
            '<div class="nav">'+pv+'<span>'+nav_title+'</span>'+nx+'</div>\n'
            '<div class="container">\n'+body+'\n</div>\n'
            '<div class="footer"><p><a href="index.html">返回总览</a> | '
            '<a href="../index.html">返回总目录</a></p></div>\n</body>\n</html>')

write_file("/path/to/file.html", hp("Title", "prev.html", "next.html", "Nav", """...body..."""))
```

**For partial section updates** (enhancing one section of a large file): use `terminal` to `cat` the file, find the section boundaries, splice in new content, and `write_file` the result. Pattern: `full[:start_idx] + new_section + full[end_idx:]`.

### Step 5: Verify after changes
```bash
for f in vendor/*.html; do
  fn=$(basename "$f")
  [[ "$fn" == "index.html" || "$fn" == 学习指南* ]] && continue
  lines=$(wc -l < "$f"); size=$(wc -c < "$f")
  echo "$f: ${lines}L, $((size/1024))KB"
done
```

**File depth expectations (aligned with 8-Dimension Framework)**
- Minimum: 200 lines / 11KB — absolute floor, should not have any module below this
- Good: 250-300 lines / 12-16KB — standard depth for all modules
- Excellent: 300-400 lines / 17-20KB — deep modules with full formulas and derivations
- Target for ALL modules: 12-16KB on the FIRST pass. Don't create 10KB placeholders expecting to deepen later — the user will reject them.
- **When user requests "深入" content**: apply the 8-dimension framework — each knowledge point should be 12-20KB with all 8 sections filled (not just headers with 1-2 sentences each).
- **Depth ratio target**: <180% between thickest and thinnest file. If thickest is 20KB, thinnest should be ≥11KB. Achieving <160% is ideal but not always possible when hardware specs naturally require more detail.

### Content Coverage Audit (内容覆盖度审计)
When the user asks to check for omissions ("有没有遗漏", "检查一下还有无遗漏"), run a systematic coverage audit:
```python
import os, re
BASE = "/path/to/guide"
files = sorted([f for f in os.listdir(BASE) if f.endswith('.html') and f != 'index.html'])
topics = [
    ("TopicName", r"keyword1|keyword2|keyword3"),
    # ... one entry per key topic
]
for name, pat in topics:
    total = 0
    found = []
    for f in files:
        c = len(re.findall(pat, open(os.path.join(BASE, f), encoding='utf-8').read(), re.I))
        if c > 0:
            total += c
            found.append(f[:2])
    status = "OK" if total >= 5 else "WARN" if total >= 2 else "GAP"
    print(f"  {status} {name}: {total} [{', '.join(found)}]")
```
- Topics with <2 matches are "gaps" — patch content into existing files or create new chapters
- After patching, re-run the audit to verify gaps are filled
- This is especially important for fast-moving fields where web research reveals topics not in training data

**Enrichment best practices (learned 2026-05-28)**:
When user asks to "丰富内容" / "补充" / "加入最新技术":
1. **Research first**: Use ddgs subagents to gather latest 2024-2025 findings (3 parallel searches, ~80s)
2. **Identify thinnest files**: Run `wc -c` audit, sort by size, target files <12KB
3. **Enrich via write_file**: Rewrite entire file with additional content, don't try to patch
4. **Priority additions**:
   - ASCII architecture diagrams (users want MORE diagrams, not fewer)
   - Latest 2024-2025 research findings with citations
   - Foundational knowledge explanations (don't assume reader knows basics)
   - Comparison tables with concrete numbers
   - Decision trees for practical choices
5. **Batch by topic**: Write 2-3 enriched files per script, not one at a time
6. **Verify after each batch**: Check file sizes to ensure enrichment actually increased content

### Depth Consistency Pitfall (NEW — learned 2026-05-25)
When creating a multi-module guide (10+ modules), the **first 2-3 modules tend to be significantly deeper** than later ones because the agent gets more efficient/tired. This creates an inconsistent reading experience. **After creating all modules, ALWAYS audit depth consistency**:

```bash
cd "/mnt/d/学习/<topic>/"
for f in *.html; do
  lines=$(wc -l < "$f"); size=$(wc -c < "$f")
  echo "$f: ${lines}行, $((size/1024))KB"
done
```

If the deepest module is 2x+ the size of the thinnest module, systematically deepen the thinnest ones. Target: all modules within 60-100% of the deepest module's size. The user will NOT accept "the critical modules are deep, the rest are thin" — they expect **uniform depth** across all modules.

**Recommended workflow (validated 2026-05-27):**
1. Generate all files in batches (2-3 files per Python script)
2. Run the depth audit above
3. Identify files below 60% of the deepest file's size
4. Write a separate "deepen" script that overwrites only the thinnest files with expanded content
5. Re-audit to verify consistency

This two-pass approach (generate → audit → deepen) is faster than trying to get perfect depth on the first pass, because you can focus deepening effort where it's needed.

### Prerequisite Knowledge Module for Paper-Based Guides

When creating a learning guide based on a specific technical paper (not a general topic survey), readers often lack domain-specific prerequisites that the paper assumes. The paper's authors assume professional background — your reader may be a complete beginner ("小白") in that domain.

**Rule**: Always create a `00-基础知识入门.html` module that covers ALL foundational concepts needed to understand the paper, placed BEFORE the paper-specific modules. This module should be the largest file in the guide (40-60KB) because it needs to cover the entire prerequisite knowledge chain.

**Structure for the prerequisite module** (example: semiconductor paper):
1. Industry overview (what is a chip, how is it made)
2. Core components (transistors, logic gates, process nodes)
3. Key manufacturing concepts (lithography, DUV vs EUV)
4. Physical phenomena the paper relies on (parasitic RC, wire delay, clock skew)
5. System-level concepts (memory hierarchy, packaging 2D/2.5D/3D, HBM)
6. The specific bottleneck the paper addresses (memory wall, fan-out dilemma, etc.)
7. Terminology glossary (every technical term the paper uses, in table format)
8. Self-test quiz (8-10 questions to verify readiness)

**Why a separate module, not embedded in later chapters**: The prerequisite module serves as a "dictionary" — readers refer back to it when they encounter unfamiliar terms in later chapters. Embedding foundations in each chapter creates fragmentation and breaks the learning flow.

### Large HTML File Generation Pattern (Split + Concat)

When a single HTML file exceeds ~20KB of content, use this reliable pattern:
1. Write content in 2-3 parts as temporary files (`_part1.html`, `_part2.html`, `_part3.html`)
2. Use `terminal("cat part1 part2 part3 > final.html")` to concatenate
3. Clean up temp files: `terminal("rm _part*.html")`

This avoids any single write_file call exceeding limits and lets you verify each part independently before combining.

## Knowledge Base Gap Audit (审查现有知识库)

When the user asks "检查一下我的知识库" or wants to assess whether their learning materials are comprehensive, follow this workflow:

### Step 1: Inventory
```bash
# Count files per top-level directory
find /mnt/d/学习/ -name '*.html' | sed 's|/mnt/d/学习/||' | cut -d'/' -f1 | sort | uniq -c | sort -rn

# Count per second-level directory
find /mnt/d/学习/ -name '*.html' | sed 's|/mnt/d/学习/||' | cut -d'/' -f1-2 | sort | uniq -c | sort -rn

# Total size
du -sh /mnt/d/学习/
```

### Step 2: Sample Quality Check
Pick 3-5 representative files across different sections. For each:
- Check file size (`wc -c`) — under 10KB is shallow
- Count technical terms (`grep -ciE 'formula|architecture|algorithm|...'`)
- Count sections (`grep -c '<h[1-3]'`)
- Read section headers to assess coverage depth

### Step 3: Identify Structural Gaps
- **Empty shells**: directories with only `index.html` but no content files (common with incomplete expansion)
- **Missing prerequisites**: topics that assume knowledge not covered elsewhere
- **Imbalance**: "heavy on X, light on Y" patterns (e.g., "重推理轻训练")
- **Missing frontier topics**: check against current research landscape

### Step 4: Create a Gap Checklist
Write a structured markdown checklist at the learning directory root with:
- Current coverage assessment (table: section | file count | rating)
- Identified problems (empty shells, broken links)
- Knowledge gaps organized by priority (P0/P1/P2/P3)
- Each gap includes: topic name, suggested output path, specific sub-topics to cover, references
- Progress tracking table (checkbox per topic with status/date/file count)

### Step 5: Generate Prompts for Each Gap Direction
When the user asks to write prompts for all gap directions, create a prompt file with:
- A **common preamble** defining the output format, style, and quality standards
- **Per-topic customizations** that specify the exact sub-topics, key concepts, formulas, comparisons, and references for that direction
- Each prompt should be self-contained — a generating agent can pick up any single prompt and produce a complete guide without additional context

**Prompt structure for learning guide generation**:
1. Role + context ("你是一个AI/LLM技术教育专家...")
2. Output format spec (HTML, dark theme, Chinese, file path)
3. 8-dimension framework reminder
4. Module structure (10-15 modules, each 15-20KB)
5. Topic-specific sub-topics list (detailed, not vague)
6. Must-include concepts, formulas, and comparison tables
7. Reference sources (papers, docs, repos)
8. Quality requirements ("不要泛泛而谈", "从零开始", "原理要到位")

**Key user preference**: User explicitly said "担心批量生成会影响质量" — prefer one-by-one generation over batch. Each prompt should be used individually for maximum depth.

## Massive Multi-Topic Guide Creation (6+ topics, 30+ files)

When creating guides with 6+ topics (each with 6-7 files), use this 3-phase workflow:

### Phase 1: Create All Files via Python Scripts
- Write a Python script per topic at `/tmp/gen_<topic>.py`, then execute via `terminal("python3 /tmp/gen_<topic>.py")`
- Each script defines CSS once, creates a template function `hp()`, and calls `w()` for each module
- **Critical escaping pitfall**: Triple-quoted strings with backslashes in HTML (regex patterns, ASCII art with `\`) cause `SyntaxError`. Solution: use single-quoted strings with `+` concatenation, or avoid backslashes entirely in ASCII art
- **Heredoc pitfall**: `cat > file << 'EOF'` in terminal may fail silently. Use `write_file` to create scripts instead
- Expected output: 4-8KB per file (Python scripts trade depth for speed)

### Phase 2: Deepen Core Modules
- After all files exist, audit sizes with `wc -c`
- Core technical modules (typically 02-04) must reach 14-21KB — deepen with `write_file` replacing entire file
- Overview (01) and summary (05-06) can stay at 5-8KB
- Deepen by adding: detailed code examples, ASCII architecture diagrams, comparison tables, formula derivations, pitfall sections
- **Priority order**: deepen the first topic's core modules first as demonstration, then proceed to other topics

### Phase 3: Verify
- Check internal links and HTML tag balance
- Report per-topic file counts and sizes

### Sub-agent Decision
- For 30+ files, `delegate_task` sub-agents work in batches of 3-4 files per sub-agent
- Always verify files at expected paths after sub-agent completion (path drift is common)
- For <20 files, direct `write_file` is more reliable

## Organizing an Existing Guide Collection (Collection Landing Page)

When the user has accumulated multiple guides/projects in `D:\学习\` and the top-level `index.html` is outdated or unorganized, use this pattern to create a categorized landing page.

### Step 1: Inventory All Content
```bash
# List all directories
ls -d /mnt/d/学习/*/
# List loose files (orphan html, test scripts, utility files)
ls /mnt/d/学习/*.html /mnt/d/学习/*.py /mnt/d/学习/*.bat 2>/dev/null
# Check each directory's content for accurate descriptions
for d in /mnt/d/学习/*/; do echo "=== $(basename $d) ===" && ls "$d" | head -10; done
```

### Step 2: Categorize into 3-5 Groups
Common categories for a learning-focused directory:
- **🧠 AI/LLM 技术** — Model guides, inference frameworks, communication, papers
- **🛠️ 开发工具** — Tool tutorials (Browser Use, Graphify, etc.)
- **☸️ DevOps** — Infrastructure (K8s, Docker, etc.)
- **🌱 生活技能** — Non-technical (finance, career, etc.)

Don't create too many categories — 3-5 is ideal. Merge small groups into the nearest larger one.

### Step 3: Build Grouped Landing Page (Grouped Index Template)
The grouped index uses **section dividers** with headers, unlike the flat grid of a single-guide index. Key elements:

1. **Stats bar** at top — total projects, total pages, total categories (impressive numbers)
2. **Section per category** — each with: icon + title + count badge, then a grid of cards
3. **Color-coded hover** — each section gets a distinct hover color (blue, green, amber, pink) via `.section-ai .card:hover`, `.section-tools .card:hover`, etc.
4. **Tag labels** on cards — `基础→进阶`, `工程实战`, `硬件底层`, `可视化项目` etc.
5. **Card layout** — icon + title + description + meta tags, using `card-row` flex layout (icon left, content right) for compactness

Store the full template as `references/grouped-landing-page-template.html` for reuse — load it with `skill_view('learning-guide-authoring', 'references/grouped-landing-page-template.html')`.

### Step 4: Clean Up Orphan Files
- Orphan `.html` files at root level → move into the most relevant subdirectory
- Test scripts (`.py`) → move into the relevant tool's directory
- Utility scripts (`.bat`) → keep at root if they serve the whole collection (e.g., server startup)

```bash
# Move orphan files
mv /mnt/d/学习/orphan-guide.html /mnt/d/学习/relevant-dir/new-name.html
mv /mnt/d/学习/test_script.py /mnt/d/学习/tool-guide/test_script.py
```

### Step 5: Update LAN Server Index
The root `index.html` is what the LAN server serves as the homepage. After reorganization, verify it loads correctly and all links work.

## Serving Your Guide Over LAN

After creating a learning guide, serve it over LAN so other devices (phone, tablet) can access it. Full details in `references/lan-serving.md`.

### Quick Start

**Key principle**: Run the server on the same OS where the files live. Files on D:\ → run on Windows, not WSL (WSL2 NAT blocks inbound LAN connections).

```powershell
# Launch from WSL on Windows side:
powershell.exe -Command "Start-Process python -ArgumentList '-m http.server 8080 --bind 0.0.0.0' -WorkingDirectory 'D:\学习' -WindowStyle Hidden"
```

Open firewall (admin required):
```powershell
powershell.exe -Command "Start-Process cmd -ArgumentList '/c netsh advfirewall firewall add rule name=\"HTTP-LAN\" dir=in action=allow protocol=TCP localport=8080' -Verb RunAs -Wait"
```

Get LAN IP and access: `http://<LAN_IP>:8080`

For external access outside home network, see `references/lan-serving.md` (Tailscale, VPS, Cloudflare Tunnel, FRP options).

## Authoring Philosophy: 像写书一样制作指南

**CRITICAL**: Read `references/book-level-authoring-philosophy.md` before creating any new guide. 核心升级：

1. **叙事红线** — 章节之间不是并列而是递进。读完第N章自然产生第N+1章要回答的问题。按"问题链"排序，不是按"概念分类"排序。

2. **章节结构** — 每章必须包含：🎣开篇钩子(故事/问题/反直觉事实) → 🎯学习目标 → 📖正文(穿插类比+图解+作者注) → ⚡关键洞察 → ⚠️常见误区 → 🗺️知识定位 → 📝本章小结 → 🧠深度思考题(L1理解/L2分析/L3创造) → 🔗下章预告。

3. **三层阅读** — 用`<details class="deep-dive">`实现折叠的深挖层。速读(5min)看标题+小结；标准(20min)看全文；深挖(60min)展开所有折叠区+做练习。

4. **视觉升级** — 架构图用CSS Grid/Flexbox（不是纯ASCII），对比图带视觉编码（绿色=胜出，红色=劣势），流程图用CSS连接线。保留ASCII用于纯文本环境。

5. **作者视角** — 必须出现：经验之谈(`.experience`框)、观点判断(`.opinion`框)、踩坑记录(`.pitfall`框)、类比解释。禁止纯罗列式写作。

6. **知识地图** — index.html中必须有全局知识地图，节点=章节，边=依赖关系，颜色=难度级别(入门绿/中级蓝/高级橙/专家粉)，可点击跳转。

7. **练习题设计** — 三个层次：L1理解(用自己的话解释) → L2分析(如果X改为Y会怎样) → L3创造(设计一个方案)。每题有场景、有提示、有实用价值。

8. **写作语气** — 像经验丰富的同事在跟你解释。用"你"不用"读者"，允许口语化("说白了就是")，主动使用反问，承认不确定性，每个核心概念至少一个类比。

## Reference Library
- `references/book-level-authoring-philosophy.md` — 像写书一样制作指南：叙事红线、章节结构(钩子→正文→洞察→误区→练习)、三层阅读模式、CSS/SVG视觉升级、作者视角、知识地图、练习题设计、写作语气。**新指南必读**。
- `references/pitfalls-consolidated.md` — 35条踩坑记录，按7类整理(生成工具/Python脚本/深度质量/内容风格/工作流/文件路径/增强审计)。主SKILL.md只保留摘要。
- `references/migration-guide.md` — 迁移环境到新电脑：核心skill列表、config打包、CLI工具安装。5分钟可完成。
- `references/html-generation-patterns.md` — CSS extraction, batch HTML generation, string escaping pitfalls, depth audit workflow. Use when creating 10+ HTML files.
- `references/p3-batch-generation-workflow.md` — Workflow for generating multiple topic guides from a checklist file (research in batches of 3, one Python script per topic, depth consistency audit)
- `references/p3-multi-topic-batch-generation.md` — Validated workflow for 42-file, 6-topic generation: research → create → audit → enrich. Includes quality audit dimensions (diagrams + code blocks) and enrichment depth strategy.
- `references/knowledge-gap-to-prompts-workflow.md` — End-to-end workflow: audit existing knowledge base → identify gaps by priority → write self-contained prompts → generate guides sequentially per direction
- `references/collective-communication-landscape.md` — Knowledge map for 集合通信 (GPU interconnects, RDMA, collective primitives, NCCL, network topologies). Use when building distributed training/communication guides.
- `references/collective-communication-nccl-detail.md` — NCCL source code analysis: 7 algorithms, 3 protocols, Ring/Tree implementations, NVLink 5-gen history, SHARP, HCCL comparison. Use when creating collective communication guides.
- `references/cross-platform-guide-patterns.md` — Parallel guide creation for competing platforms (e.g., NVIDIA vs Huawei). Covers: separate directories with cross-links, resource index chapters (100+ URLs), comparison chapters, subagent research workflow. Read when user wants to compare two or more platforms systematically.
- `references/github-api-source-reading.md` — How to read open-source code via GitHub API for source-level technical analysis. Validated on NCCL repo. Use when docs are insufficient and source code is available.
- `references/interactive-visualization-patterns.md` — Patterns for creating self-contained interactive HTML applications with Canvas animations, tab interfaces, and control panels. Use when user wants a "demo", "visualization", or "interactive tool" (distinct from static learning guides).
- `references/arxiv-api-paper-fetching.md` — arXiv REST API for automatic paper fetching, XML parsing, rate limiting, deduplication. Use when building research paper tracking tools.
- `references/scaling-law-guide-2026.md` — Research bank for Scaling Law domain: key papers, formulas (Kaplan/Chinchilla), test-time compute, MoE scaling, data scaling. Use when creating AI/ML scaling or training-related guides.
- `references/inference-framework-guide-pattern.md` — Pattern for deep-dive guides on specific inference frameworks/tools (Dynamo, vLLM, SGLang, TRT-LLM). Flat 10-file structure, 3-subagent research, benchmark honesty, decision trees. Use when user asks to "分析/解读" a specific inference tool.

## Enrichment Pass Workflow (Post-Generation Enhancement)

After generating an initial set of guide files, the user may ask to "补强" (enrich/strengthen) the content with latest developments, more diagrams, and deeper explanations. Use this workflow:

### Step 1: Audit file sizes
```bash
for f in *.html; do
  fn=$(basename "$f"); [[ "$fn" == "index.html" ]] && continue
  sz=$(wc -c < "$f"); lines=$(wc -l < "$f")
  echo "  $fn: ${sz}B, ${lines}行"
done
```
Identify files below 10KB as priority targets for enrichment.

### Step 2: Parallel research for latest developments
Use `delegate_task` with 3 parallel subagents (one per topic area) running `ddgs` CLI. **This is the ONLY reliable use of delegate_task for guide work** — searching via ddgs, not generating HTML:
```python
delegate_task(tasks=[
    {"goal": "Search for latest developments in [topic1] 2024-2025 via ddgs CLI", "toolsets": ["terminal"]},
    {"goal": "Search for latest developments in [topic2] 2024-2025 via ddgs CLI", "toolsets": ["terminal"]},
    {"goal": "Search for latest developments in [topic3] 2024-2025 via ddgs CLI", "toolsets": ["terminal"]},
])
```
Each subagent runs `ddgs text -q '...' -m 3` and returns summaries. ~80s for 3 parallel searches.

### Step 3: Write enrichment scripts
For each thin file, write a Python script that overwrites it with expanded content incorporating the research findings. Add:
- **More ASCII diagrams**: Architecture diagrams, data flow charts, comparison visualizations
- **Latest techniques**: New papers/tools from 2024-2025 web search results
- **Deeper fundamentals**: Background knowledge, prerequisite explanations
- **Better comparisons**: Updated benchmark tables with real numbers
- **Practical code**: More code examples with explanations
- **术语速查表**: Glossary at the end of each file

### Step 4: Verify
Re-audit file sizes after enrichment. Target: all files ≥ 10KB, thinnest ≥ 60% of thickest.

## Modular Architecture
See `references/modular-architecture.md` for multi-file patterns, renumbering pitfalls, density auditing.

### Enhancement Loop Anti-Pattern (NEW — learned 2026-05-27)
When enhancing thin files, a common trap is **rewriting the same file repeatedly without increasing its size**. The agent reads the file, generates new content of similar length, and writes it — but the file stays at the same size because the content structure hasn't fundamentally changed.

**Symptoms**: Same file written 3+ times, `wc -c` shows identical size after each write.

**Fix**: Don't rephrase existing content — ADD new sections. Pick what's MISSING (deeper explanations, more examples, additional subsections) and insert them. If writing twice doesn't increase size by >20%, stop and move on.

### Large-Scale Model/Topic Guide Generation (25+ files)
When creating a guide series with many individual topic files (e.g., 25 classic ML models), the most reliable approach is:
1. Write a Python script to `/tmp/gen_NN_MM.py` that uses the `hp()` template function pattern (CSS reuse + wrapper)
2. Each script generates 2-3 model/topic files (not more — content truncation risk)
3. Execute via `terminal("python3 /tmp/gen_NN_MM.py")` — this bypasses execute_code sandbox limitations
4. Each file should target 9-14KB — enough for 8-dimension framework without bloating

**Do NOT use delegate_task for HTML content generation** — on mimo-v2.5-pro, subagents consistently timeout at 600s when generating detailed HTML files. All 3 parallel subagents timed out in testing. The write_file + terminal approach is 10x more reliable.

**Script template pattern** (reuse CSS from existing file):
```python
CSS = open(os.path.join(BASE, "01-ExistingFile.html"), encoding="utf-8").read().split("<style>")[1].split("</style>")[0]
def hp(title, prev, nxt, nav, body):
    # Standard wrapper with nav, container, footer
    ...
def w(path, content):
    with open(os.path.join(BASE, path), "w", encoding="utf-8") as f: f.write(content)
    print(f"  {path} ({os.path.getsize(os.path.join(BASE, path)):,}B)")
```

**Batch size guidance**: 2-3 files per script is the sweet spot. 5+ files risks the script content itself being too large for a single write_file call.

### Existing guide deepening/细化 pitfalls

## Enrichment Workflow (审核补强)

When the user says "检查一遍" "再丰富一下" "补充更多图" "最新技术" after initial guide creation:

### Step 1: Quality Audit (two dimensions)
```bash
# Dimension 1: File sizes
for f in *.html; do sz=$(wc -c < "$f"); echo "$f: $((sz/1024))KB"; done

# Dimension 2: Content richness (diagrams + code blocks)
for f in *.html; do
  a=$(grep -c 'class="ascii"' "$f")
  c=$(grep -c '<pre><code>' "$f")
  echo "$f: ${a}图 ${c}码"
done
```

**Quality thresholds** (validated across 42-file session):
- Each module MUST have ≥2 ASCII diagrams AND ≥1 code block
- Files with 0-1 diagrams or 0 code blocks are priority enrichment targets
- Overview modules (01) can have fewer code blocks but still need ≥2 diagrams

### Step 2: Search latest developments
Use delegate_task with 3 parallel subagents to search for latest papers, tools, and trending techniques via ddgs CLI.

### Step 3: Prioritize enrichment targets
Focus on files missing diagrams/code blocks first, then files under 10KB.

### Step 4: Rewrite with expanded content
For each target, create enriched version with:
- More ASCII diagrams (architecture, data flow, comparison visualizations)
- Latest techniques from 2024-2025 web search results
- Deeper fundamentals and prerequisite explanations
- Updated benchmark tables with real numbers
- Practical code examples with explanations

### Step 5: Verify improvement
Re-audit file sizes AND content richness after enrichment.

**Key insight**: Users often accept initial guides but notice missing diagrams, outdated info, and thin coverage on reflection. The enrichment pass is where guides become truly useful. Proactively offer enrichment after creating 10+ files.

**Enrichment depth pitfall**: When deepening files incrementally (adding 1-2KB per pass), the user's auto-continuation system will keep firing because the improvement is too small. **Rule**: When deepening, rewrite the ENTIRE file with substantially more content (target +5KB per deepening pass), not just append a few paragraphs. In one session, 15+ deepening passes only grew files from 5KB to 7KB because each pass was too incremental.

### f-string Curly Braces in HTML/JSON Content
**CRITICAL**: When generating HTML/JSON content inside Python f-strings, ALL literal curly braces must be doubled: `{{` and `}}`. This includes JSON objects, Python dict literals in code examples, and any literal braces. Missing this causes `ValueError: Invalid format specifier` errors. **Safer approach**: Use string concatenation (`+`) instead of f-strings for HTML with code examples:
```python
CSS = """..."""
content = '''<!DOCTYPE html>...<style>''' + CSS + '''</style>...'''
```

### Enrichment Workflow (when user asks to "review/enrich/补充" existing guides)
When the user asks to review and enrich existing guides, follow the systematic enrichment workflow in `references/guide-enrichment-workflow.md`. Key steps:
1. **Audit file sizes** — find thinnest files (< 11KB)
2. **Parallel research** — use 3 subagents with ddgs to gather latest 2024-2025 findings
3. **Rewrite thinnest files** — add more ASCII diagrams, latest research, foundational knowledge
4. **Verify depth consistency** — target depth ratio < 160% (thinnest ≥ 60% of thickest)

## Bulk File Creation: write_file vs Python Scripts

When creating 10+ files, there are two approaches:

**Approach 1: Individual write_file calls (RELIABLE)**
- One `write_file` call per file inside `execute_code`
- Each call takes ~1 second
- Works for any content, no escaping issues
- Best for 5-15 files

**Approach 2: Python script to /tmp then execute via terminal (FAST but FRAGILE)**
- Write a Python script to `/tmp/gen_XX.py` using `write_file`
- Run with `terminal("python3 /tmp/gen_XX.py")`
- **PITFALL**: Triple-quoted strings with embedded HTML cause `SyntaxError: unterminated triple-quoted string` when the HTML contains backslashes (e.g., regex patterns like `\d`, `\s`)
- **WORKAROUND**: Use single-quoted strings with explicit `\n` for newlines, OR use `write_file` directly for each file
- **PITFALL**: The heredoc approach (`cat > /tmp/script.py << 'EOF'`) often fails silently in WSL — the file may not be created
- **BEST PRACTICE**: For 20+ files, write the Python script via `write_file` to `/tmp/gen_XX.py`, then execute via `terminal`. Avoid triple-quoted HTML content — use string concatenation or single-line strings with `\n`.

## Deepening Existing Guides: Diminishing Returns

When the user asks to "丰富内容" or "再检查一遍":

1. **Establish clear exit criteria FIRST**: Define what "done" means (e.g., "all modules ≥2 ASCII diagrams + ≥1 code block + ≥8KB")
2. **Audit before deepening**: Run a single command to check all file sizes and content metrics
3. **Prioritize by impact**: Deepen core technical modules (02-04) before overview/summary modules (01, 05-06)
4. **Overview modules don't need 14-21KB**: Modules titled "总览" or "前沿" naturally have less technical depth. 6-8KB with 2 diagrams and 1 code block is sufficient.
5. **Stop when criteria are met**: Don't keep deepening in a loop. State the criteria, verify they're met, and declare completion.
6. **PITFALL: Infinite deepening loop** — The user may keep sending "继续完善" without explicit feedback. After 2-3 rounds of deepening with no new user corrections, establish completion criteria and verify. Don't deepened the same file 3+ times.

## Massive Guide Generation (20+ files)
For generating 10-30+ HTML guides, see `references/massive-guide-generation-workflow.md`. Key: write 2-3 files per Python script to /tmp, run via terminal. delegate_task times out on mimo for HTML generation.

For batch generation pitfalls (minification, triple-quote issues, verification), see `references/batch-generation-pitfalls.md`.

## SVG Diagram Upgrade Pattern (SVG图表升级模式)

When the user says "ASCII图简陋" or wants professional diagrams, upgrade key ASCII blocks to SVG. The architecture-diagram skill provides the design system (semantic colors, grid background, markers).

**Which diagrams to upgrade:** Only the top 1-2 most complex diagrams per file. Keep simple 3-step flows and code-like structures as ASCII. Target 8-12 SVG diagrams total per guide.

**SVG helper functions pattern (Python script):**
```python
SVG_DEFS = '''<defs>
  <pattern id="grid" .../>
  <marker id="arrow" .../>
  <marker id="arrow-cyan" .../>  # one per semantic color
</defs>'''

def box(x, y, w, h, fill, stroke, label, label2=None, fs=13):
    # CRITICAL: compute yoff FIRST, don't use inline ternary in f-string
    yoff = -2 if label2 else 5  # {5 if not label2 else -2} causes TypeError!
    cx, cy = x+w//2, y+h//2+yoff
    t2 = '...' if label2 else ''
    return '<rect .../><text .../>' + t2

def arrow(x1, y1, x2, y2, color="#475569"):
    # Map color to marker name
    cmap = {"#22d3ee":"arrow-cyan", "#34d399":"arrow-emerald", ...}
    mk = cmap.get(color, "arrow")
    return '<line ... marker-end="url(#'+mk+')"/>'

def txt(x, y, text, color="#94a3b8", fs=11, anchor="middle"):
    return '<text ...>'+text+'</text>'
```

**Semantic color mapping (from architecture-diagram skill):**
| Component Type | Fill (rgba) | Stroke |
|---|---|---|
| Frontend/Input | rgba(8,51,68,0.4) | #22d3ee (cyan) |
| Backend/Process | rgba(6,78,59,0.4) | #34d399 (emerald) |
| Database/Storage | rgba(76,29,149,0.4) | #a78bfa (violet) |
| Orchestration | rgba(251,146,60,0.3) | #fb923c (amber) |
| Hardware/Risk | rgba(136,19,55,0.4) | #fb7185 (rose) |

**CSS requirement:** Every file with SVG needs `.diagram{...}` and `.diagram-title{...}` CSS classes. Inject before `</style>` if missing.

**Replacement pattern:** Find `<div class="ascii">...</div>` blocks via `html.split('<div class="ascii">')`, replace the first N matches with SVG divs. Keep remaining ASCII blocks unchanged.

**Pitfall:** The box() function's f-string `{y+h//2+{5 if not label2 else -2}}` causes `TypeError: unsupported operand type(s) +: 'int' and 'set'`. The inner `{5...}` is parsed as a set literal, not an f-string expression. Fix: compute `yoff = -2 if label2 else 5` as a separate variable first.

## Coverage Audit Methodology (内容覆盖度审计)

When creating a multi-module guide (8+ files), run a systematic coverage audit before declaring done. The user WILL catch missing topics.

**Step 1: Define topic checklist** based on the domain. For infrastructure/framework guides, always include:
- Core architecture components
- Performance/scalability (elasticity, autoscaling, TCO)
- Fault tolerance (migration, failover, graceful shutdown)
- API/SDK usage examples
- Deployment (Docker, K8s, cloud)
- Ecosystem integration
- Cost optimization

**Step 2: Run regex coverage check:**
```python
import re, os
files = sorted([f for f in os.listdir('.') if f.endswith('.html') and f != 'index.html'])
topics = [("TopicName", r"keyword1|keyword2|keyword3"), ...]
for name, pat in topics:
    total = sum(len(re.findall(pat, open(f).read(), re.I)) for f in files)
    status = "OK" if total >= 5 else "WARN" if total >= 2 else "GAP"
    print(f"  {status} {name}: {total}处")
```

**Step 3: Patch gaps** — add missing content to existing files rather than creating new files. Use `patch()` with old_string/new_string for targeted insertions.

**Step 4: Re-audit** to verify all gaps are closed.

**Common gaps in architecture guides:**
- Elasticity/autoscaling (Planner, SLA-driven scaling) — often mentioned briefly but not deeply covered
- Fault tolerance (request migration, graceful shutdown) — critical for production but often omitted
- API/SDK usage — developers need code examples, not just architecture diagrams
- Cost/TCO analysis — decision-makers need this but engineers often skip it

## Pitfalls

When the user asks to "细化" (expand/refine/detail) an existing guide:

1. **Analyze current depth**: Use `execute_code` + `read_file` to check all file sizes and identify shallow modules (ones with only a README.html or under 10KB). Do NOT use `delegate_task` — it times out on mimo.
2. **Plan sub-file structure**: Each shallow module gets split into a sub-directory with numbered files: `00-总览.html`, `01-TopicA.html`, `02-TopicB.html`, etc.
3. **Create sub-files in batches**: Use `execute_code` with 3-5 `write_file` calls per batch for efficiency.
4. **Update index.html**: Change card links from `模块/README.html` to `模块/00-总览.html` and update descriptions to reflect new sub-files. Use the `patch` tool with `*** Begin Patch` / `*** End Patch` syntax for targeted HTML edits.
5. **Update hero metadata**: Bump file count and learning duration in the index hero section.

### Multi-Brand Guide Expansion (e.g., "国产LLM系列" with 16 brands)

When a guide covers **multiple brands/topics**, each with its own sub-directory, and some are "empty shells" (only index.html, no sub-files):

1. **Audit all brands**: Use `terminal` to count files per directory. Categorize as:
   - **Full** (has 4+ sub-files): needs gap-filling chapters
   - **Partial** (has 2-3 sub-files): needs most chapters created
   - **Empty shell** (only index.html + 学习指南): needs all chapters created
2. **Design unified chapter template**: Define a standard 11-12 chapter structure that works for ALL brands. Example for LLM providers:
   ```
   01-公司背景与模型演进.html    # Company history, timeline
   02-核心架构设计.html          # Transformer variant, MoE/Dense
   03-注意力机制创新.html        # GQA/MLA/Linear Attention
   04-预训练策略与数据工程.html   # Data pipeline, scaling law
   05-后训练与对齐.html          # SFT/RLHF/DPO/GRPO
   06-推理能力与长上下文.html     # Reasoning, context extension
   07-多模态与跨模态.html        # Vision/audio/video
   08-系统工程与部署优化.html     # Distributed training, inference
   09-性能评估与基准测试.html     # Benchmarks, comparisons
   10-应用场景与生态系统.html     # API, products, ecosystem
   11-论文精读与学习资源.html     # Papers, learning path
   ```
3. **Research in parallel**: Use `terminal` + `curl` to scrape official docs for all brands simultaneously. Chinese AI platforms are the best source — see `references/chinese-ai-platform-docs.md`.
4. **Create in batches via delegate_task**: For 10+ brands, use `delegate_task` with **3 concurrent subagents** (max_concurrent_children=3). Each subagent handles ONE brand's full set of new chapters.
   - **Critical**: Each subagent should create **4-5 files max** to avoid 600s timeout
   - For brands needing 10+ files, split across 2 subagents (files 01-05, then 06-11)
   - Always specify **full Windows paths** in the goal — subagents may write to `/home/` instead of `/mnt/d/学习/` if paths are ambiguous
   - Example: `"Write to /mnt/d/学习/国产LLM系列/Kimi/05-注意力机制创新.html"`
5. **Brand-specific CSS theming**: All brands use the same dark theme CSS variables (--bg:#0d1117 etc.) for visual consistency across the entire collection.
6. **Update all navigation chains**: After creating chapters for a brand:
   - Update the brand's `index.html` to list all chapters in a chapter-list table
   - Update the top-level `index.html` footer with total file count
7. **Verification pass**: After all subagents complete, run `find ... | wc -l` per brand to verify expected file counts. Check for files written to wrong paths (common with subagents).
8. **Skip brands the user excludes**: If user says "X不需要", don't touch that brand's files.
9. **User consultation for prioritization**: When expanding 10+ brands, ask the user whether to:
   - Expand all at once (large batch, some subagent timeouts expected)
   - Start with most important brands first, then continue
   - Only expand specific brands
   Present the current state (file counts per brand) so the user can decide.

## Incremental Updates (New Model Versions, API Changes)

When updating an existing guide with new information (e.g., a company releases a new model version):

1. **Research first**: Scrape official API docs (see "Scraping Chinese AI Platform Docs" below) to get factual details — model IDs, context lengths, feature descriptions.
2. **Create a new chapter file**: Add `NN-NewTopic.html` following the existing file naming pattern. Include navigation links to previous/next chapters.
3. **Update navigation chains**: Patch the PREVIOUS chapter's "next" link to point to the new file. Patch the new file to link back.
4. **Update the module index.html**: Add new timeline entries, model comparison rows, and description updates. Use targeted `patch` calls — one patch per logical section.
5. **Update the top-level index.html**: Refresh the model family card description and tags to reflect the new information.
6. **Verify after patching**: Always re-read the end of patched files to catch misplaced content (see Pitfalls).

### Scraping HuggingFace for Model Metadata

HuggingFace model cards contain structured metadata (parameters, architecture, context length, release dates) that is faster to obtain than reading full papers. Use for quick model enumeration and comparison.

**Search pattern** (via ddgs CLI):
```bash
ddgs text -q 'site:huggingface.co OrgName ModelName' -m 5
```

**Key fields to extract from snippets**:
- Model size: "X billion parameters", "XB", "X-YB"
- Architecture: "MoE", "Dense", "Mixture-of-Experts"
- Context: "context length", "128K", "1M"
- Active params: "activated per token", "XA active"
- Release: "Updated X weeks ago", date in snippet

**Model page scraping** (direct):
```bash
# Get model card metadata (JSON-LD in page)
curl -sL "https://huggingface.co/api/models/OrgName/ModelName" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Siblings: {len(d.get(\"siblings\",[]))} files')
print(f'Tags: {d.get(\"tags\",[])}')
print(f'Pipeline: {d.get(\"pipeline_tag\",\"?\")}')
"
```

**Important**: Do NOT download model weight files (*.safetensors, *.bin) — only fetch metadata and model cards. The user explicitly forbade downloading model source files from HuggingFace.

**Best use cases**:
- Finding all model sizes in a family (e.g., Qwen3.5 has 0.8B to 397B-A17B)
- Getting MoE config (total params, active params, expert count)
- Checking if a model is multimodal (pipeline_tag: "image-text-to-text")
- Finding quantized variants (GGUF, AWQ, GPTQ)
- Confirming release dates and org names

### Per-Generation Architecture Detail Pattern (逐代架构详解)

When the user wants to understand how a model family evolved architecturally across versions, create a dedicated "逐代架构详解" page per provider. This is distinct from the overview index and the learning guide.

**Structure**:
```
Provider/
├── index.html                    ← Overview (company, models, links)
├── 学习指南-Provider全系列.html     ← Systematic learning (concepts, methods)
├── 01-Topic.html                 ← Deep dive on specific topic
└── NN-逐代架构详解.html            ← Per-generation architecture comparison
```

**逐代架构详解 content template**:
1. **总览对比表** — All generations in one table (params, active, context, attention, FFN, training data, cost)
2. **Per-generation cards** — Each generation gets a card with:
   - Badge: `首次引入` / `沿用` / `升级` for each component
   - Spec grid: key numbers (params, tokens, context)
   - **Diff table** vs previous generation (what changed, ↑↓ arrows)
   - Architecture formulas (actual from papers, not invented)
   - Code/ASCII diagrams for novel components
3. **创新演进表** — Which innovation appeared in which generation, and which subsequent models inherited it
4. **论文阅读顺序** — Recommended paper reading order

**Example**: DeepSeek 逐代架构详解 covers:
- V2: MLA + MoE first appearance (236B/21B)
- V3: FP8 + MTP + aux-loss-free (671B/37B)
- R1: GRPO algorithm (same arch as V3)
- V4: CSA+HCA + mHC + Muon (1.6T/49B)
With diff tables showing exactly what changed each generation.

### Scraping Chinese AI Platform Docs

Chinese AI companies publish structured model documentation on their developer platforms. These are far more reliable than web search for technical details:

| Company | Model List URL | API Docs URL |
|---------|---------------|--------------|
| Kimi (Moonshot) | `platform.moonshot.cn/docs/models` | `platform.moonshot.cn/docs/api/models-overview` |
| DeepSeek | `platform.deepseek.com/api-docs` | `api-docs.deepseek.com` |
| Qwen (Alibaba) | `help.aliyun.com/zh/model-studio/` | `dashscope.aliyuncs.com` | `tongyi.aliyun.com` (product page with model list in JSON/JS) |
| Zhipu (GLM) | `open.bigmodel.cn/dev/api` | `open.bigmodel.cn` | |

**Scraping technique** (for Next.js/Mintlify-based doc sites):
```bash
# Extract readable text from doc pages (strip JS/CSS noise)
curl -sL --max-time 15 "https://platform.moonshot.cn/docs/models" 2>/dev/null \
  | sed 's/<[^>]*>//g' | sed '/^$/d' \
  | grep -i "model\|模型\|context\|上下文\|参数" | head -40

# Look for banner announcements (often in inline JS)
curl -sL "https://platform.moonshot.cn/docs/models" 2>/dev/null \
  | grep -oP '"content":"[^"]*"' | head -5
```

These sites are typically Next.js with Mintlify, so content is embedded in JSON/JS chunks. The `sed 's/<[^>]*>//g'` approach extracts usable text even from SSR-rendered pages.

### Batch Creation Pattern (Recommended: Python Script via Terminal)

**Best approach for 20+ files**: Write a Python script to `/tmp/gen_moduleXX.py` and run it via `terminal`. This is faster than individual `write_file` calls because you define CSS once and reuse a template function.

```python
#!/usr/bin/env python3
"""Generate Module XX files."""
import os
BASE = "/mnt/d/学习/<topic-name>"

# Extract CSS from an existing file (consistent styling)
with open(os.path.join(BASE, "01-DirName", "01-ExistingFile.html"), encoding='utf-8') as f:
    CSS = f.read().split("<style>")[1].split("</style>")[0]

def hp(title, prev, nxt, nav_title, content):
    """Generate a complete HTML page with nav."""
    pv = '<a href="'+prev+'">&larr; '+os.path.basename(prev).replace('.html','')+'</a>' if prev else '<span></span>'
    nx = '<a href="'+nxt+'">'+os.path.basename(nxt).replace('.html','')+' &rarr;</a>' if nxt else '<span></span>'
    return ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>'+title+' | Guide</title>\n<style>'+CSS+'</style>\n</head>\n<body>\n'
            '<div class="nav">'+pv+'<span>'+nav_title+'</span>'+nx+'</div>\n'
            '<div class="container">\n'+content+'\n</div>\n'
            '<div class="footer"><p>Guide · '+title+'</p>'
            '<p><a href="../index.html">返回总目录</a></p></div>\n</body>\n</html>')

def w(path, content):
    full = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  {path} ({os.path.getsize(full):,}B)")

# Then call w() for each file:
w("01-Dir/01-SubTopic.html", hp("01-Title", None, "02-Next.html", "Nav Title", """...content..."""))
    w("01-Dir/02-SubTopic.html", hp("02-Title", "01-SubTopic.html", "03-Next.html", "Nav", """...content..."""))
# ... etc
print("Done!")
```

## Auditing & Maintaining Hub Index Pages

When the user asks to "fix", "update", "audit", or "整理目录" for the central hub page (D:\学习\index.html), use the systematic workflow in `references/hub-index-audit-workflow.md`.

Key steps:
1. `tail -20` the file to check for truncation (common failure — write_file can cut off at ~500 lines)
2. `find` all actual guide directories and cross-reference against hrefs in the index
3. Count HTML files per section for accurate stats (the template has stale hardcoded numbers)
4. Regenerate with real data — stats, section counts, missing cards/sections

**Pitfall**: The grouped landing page template (`references/grouped-landing-page-template.html`) has hardcoded placeholder stats. Always override with actual `find | wc -l` counts.

**Pitfall**: For hub pages with 30+ cards (e.g., D:\学习\index.html with all AI/LLM sections), the full HTML can exceed 600 lines. Prefer generating via a Python script that writes the file (`/tmp/gen_hub.py`) rather than relying on write_file's output size limits. Always `tail -5` the result to confirm it ends with `</html>`.

**For batch generation of 20+ model/topic files (e.g., 25 classic models, 16 vendor guides)**: Do NOT use delegate_task — it times out on mimo. Write Python scripts to `/tmp/gen_batchN.py` with embedded HTML content and CSS template, then execute via `terminal("python3 /tmp/gen_batchN.py")`. Each script handles 3-5 models. See `references/batch-html-generation-pattern.md` for the full template and workflow.

Run with: `python3 /tmp/gen_moduleXX.py`

**Key rules for Python-generated HTML**:
- NEVER use f-strings for HTML content — CSS/JS curly braces cause `NameError`
- Use string concatenation (`'a' + 'b'`) for HTML templates
- Use triple-quoted strings for content blocks
- Extract CSS from an existing file via `split("<style>")[1].split("</style>")[0]` for consistency
- Each script should handle one module (directory) at a time
- Print file sizes after creation to verify depth

**Preferred approach for bulk generation (30+ files across multiple topics): write Python scripts to `/tmp` then execute via `terminal`**:
1. Use `write_file` to create `/tmp/gen_<topic>.py` — this avoids heredoc issues and escaping problems
2. Run with `terminal("python3 /tmp/gen_<topic>.py")` — reliable, no timeout issues
3. Each script handles ONE topic (7 files: index + 6 modules)
4. Use single-quoted strings for HTML content in Python (HTML uses double quotes, so no conflicts)
5. For HTML content with single quotes (rare), use `\'` escaping or build from string lists

**String escaping pitfalls in Python scripts**:
- NEVER put `\n` inside single-quoted strings passed to `hp()` — Python interprets `\` as line continuation. Use actual newlines in triple-quoted strings instead.
- Backslash-heavy content (regex, Windows paths) breaks in single-quoted strings. Use raw strings or escape properly.
- HTML with both single and double quotes: use `\"` for HTML attributes inside single-quoted Python strings.
- The `execute_code` sandbox has a 50KB stdout cap — keep scripts under 40KB.
- `delegate_task` max_concurrent_children=3 — split research into batches of 3.

- **Run each script immediately after writing** — don't write multiple scripts then run them all. Write→run→write→run.

**Why 2-3 files per script (not 4-5)**: On mimo-v2.5-pro, scripts generating 4+ files tend to produce shorter/sparser content for later files in the batch (the model "races" to finish). Scripts with 2-3 files produce uniform depth across all files. This was validated across 25+ file generations in a single session.

### Subagent Partial Output Discovery (NEW — learned 2026-06-25)
When `delegate_task` times out at 600s, the subagent often **has already created partial output** (3-8 files). Before retrying or switching to direct creation:
1. **Check what was created**: Run `search_files` or `ls` on the target directory
2. **Assess quality**: Check line counts of partial files — they may be complete and high-quality
3. **Only create the MISSING files**: Don't redo work that was already done
4. **Pattern**: Subagent for Kimi created 3 chapters before timeout; GLM created 8 chapters. Both were high quality (140-218 lines each).

This was validated when creating 3 parallel vendor deep-dive guides:
- GLM subagent: timed out at 600s but produced 8/11 chapters (73%)
- Kimi subagent: timed out at 600s but produced 3/11 chapters (27%)
- Qwen subagent: timed out at 600s, produced 0 chapters

**Rule**: After a subagent timeout, ALWAYS check for partial output before recreating files. Use `search_files(path=dir, pattern="*.html")` to inventory what exists.

### Verify Before Fixing (NEW — learned 2026-06-25)
User corrected: "请仔细校验再处理" (verify carefully before processing). This means:
1. **Read the actual content** of files flagged as "thin" — some compressed single-line files contain substantial content (5KB+ of actual HTML)
2. **Don't assume emptiness** based on line count alone — a 13-line file may have 5KB of dense HTML
3. **Check for existing content** before overwriting — read first, then decide if it needs expansion
4. **Present findings before acting** — show the user what you found, then propose a fix

### Large Project Organization Pattern (NEW — learned 2026-06-25)
When a learning project directory contains an outlier subdirectory that's disproportionately large (e.g., 429MB out of 481MB total):
1. **Identify the outlier**: `du -sh */` per subdirectory
2. **Check if it fits the project theme**: Federated learning (429MB with 72 PDFs) doesn't fit an LLM-focused project
3. **Move it out**: `mv /path/to/outlier /path/to/new/location` — reduces project size by 89%
4. **Verify**: Check new project size after move
5. **Don't delete**: The content is still valuable, just doesn't belong in this project

**Alternative (fewer files)**: Use `write_file` tool directly. Each call takes ~1 second. Fine for 5-15 files, but slow for 50+.

## Paper-Based Learning Guides

When creating learning guides based on actual technical papers (not just web search), see also `references/paper-to-learning-guide-workflow.md` for the full pipeline (find paper → scrape sources → build foundation module → create guide).

### Step 1: Search & Download Papers
For Chinese-origin papers, check ChinaXiv first (see `references/chinese-preprint-platforms.md`).
```bash
# Search for paper URLs (arXiv)
ddgs text -q 'ModelName technical report arxiv paper' -m 3

# Search for Chinese papers on ChinaXiv
ddgs text -q '公司名 论文关键词 site:chinaxiv.org' -m 3
# Also search news articles which link directly to papers
ddgs text -q '论文关键词 论文 原文 PDF' -m 5

# Download PDFs (arXiv)
curl -sL -o Paper-Name.pdf "https://arxiv.org/pdf/XXXX.XXXXX"

# ChinaXiv may need User-Agent
curl -sL -H 'User-Agent: Mozilla/5.0' -o paper.pdf "https://chinaxiv.org/abs/YYYYMM.NNNNN"
```

### Step 2: Extract Text with pymupdf
Write extraction script to file first (heredocs get BLOCKED), then run:
```python
# /tmp/extract_pdfs.py
import fitz, os
dir = '/path/to/papers'
for f in sorted(os.listdir(dir)):
    if f.endswith('.pdf'):
        doc = fitz.open(os.path.join(dir, f))
        text = ''.join(page.get_text() for i, page in enumerate(doc) if i < 15)
        with open(os.path.join(dir, f.replace('.pdf', '.txt')), 'w') as out:
            out.write(text[:30000])  # First 30K chars per paper
```
Run with: `python3 /tmp/extract_pdfs.py`

### Step 3: Read & Analyze Paper Content
Use `read_file` + `terminal` grep to extract key sections:
```bash
grep -n "Architecture\|formula\|algorithm\|training\|benchmark" paper.txt | head -30
```

### Step 4: Write Guides with Paper Content as Basis
- Include actual formulas from papers (not invented ones)
- Reference specific arXiv IDs and page numbers
- Use comparison tables with real benchmark scores
- Each guide should have a "论文清单" section linking to local PDFs

### Chronological Model/Technology History Pattern (时间线模型史)
When the user asks to learn "all classic models in a field's development history" (e.g., "从深度学习到LLM的所有经典模型"), organize as a chronological timeline:

**Structure**:
- `index.html` — Timeline overview with phase headers, model cards, dependency arrows, learning order recommendations
- `01-ModelName.html` through `NN-ModelName.html` — One file per model, numbered chronologically
- Group into 3-5 phases (e.g., "Phase 1: Foundations", "Phase 2: Breakthrough", "Phase 3: Modern")
- Each model file follows the 8-dimension framework
- Include a "dependency chain" section in index.html showing which models must be learned before others

**Key design decisions**:
- Number models sequentially (01-25) within phases, not by phase-number (don't use 1-1, 1-2, 2-1...)
- Include a year badge on each model card in the index
- Cross-reference related models within each file ("关联技术" section links to other models in the series)
- Include ASCII timeline visualization in the index page

**Depth consistency pitfall (critical for 20+ files)**: When generating many model files in sequence, the first 3-5 files tend to be significantly deeper (14-15KB) than later ones (6-7KB) because the agent generates content more concisely over time. After creating ALL files, ALWAYS:
1. Run a size audit: `for f in *.html; do wc -c < "$f"; done`
2. Identify files below 60% of the median size
3. Rewrite the thinnest 3-5 files with expanded content
4. Target: all files within 60-140% of the median (8-14KB range acceptable)

**Batch generation strategy for 20+ models**:
- Batch 1-2: Write manually with full detail (sets the CSS and template)
- Batch 3-8: Use Python scripts to `/tmp/gen_NN_NN.py`, 2-3 models per script
- Final batch: Deepen pass for consistency
- Total time: ~15-20 turns for 25 models

### Pitfalls
- arxiv PDFs download fine via `curl -sL` — no special headers needed
- pymupdf must be installed in system Python (`pip install pymupdf`), NOT in execute_code sandbox
- Extract first 15 pages only — most technical content is in the first half
- Paper text extraction gives raw text (no formatting) — use grep to find key sections

### Depth Audit Timing Pitfall
When creating 10+ module guides, do the depth consistency audit **in the same session** as creation, before declaring done. See `references/research-and-depth-pitfalls.md` for detailed pitfalls.

## Multi-Guide Project Management (学习提示词 files)

When the user has structured learning plans (like 学习提示词-P0.md), read the prompt file first to understand:
- Total number of guides and files per guide
- Exact file names and content requirements per file
- Target size (14-21KB/file)
- Specific topics, papers, and tools to cover

**Workflow for multi-guide projects:**
1. Read the prompt file to get full scope
2. Create ALL index.html files for all guides first (establishes structure)
3. Generate content files guide-by-guide, 2-3 files per script
4. Verify file counts after each guide is complete
5. Update todo list to track progress

## Python Script Batch Generation Pattern

For generating 5+ HTML files, use Python scripts written to `/tmp/` then executed via `terminal`. This is 5-10x faster than individual `write_file` calls.

**Script template structure:**
```python
#!/usr/bin/env python3
import os
BASE = "/path/to/output"
CSS = """*{margin:0;...}"""  # Full CSS string

def hp(title, prev, nxt, nav, body):
    # Generate complete HTML page with nav, container, footer
    ...

def w(path, content):
    with open(os.path.join(BASE, path), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  {path} ({os.path.getsize(os.path.join(BASE, path)):,}B)")

# Content for each file
w("01-Topic.html", hp("Title", None, "02-Next.html", "Nav", """...content..."""))
w("02-Next.html", hp("Title", "01-Topic.html", "03-After.html", "Nav", """...content..."""))
```

**Key rules for batch scripts:**
- Extract CSS from an existing file: `CSS = open(file).read().split("<style>")[1].split("</style>")[0]`
- 2-3 files per script is the sweet spot (scripts get too large for 4+ files)
- Each file targets 10-15KB of body content (total file ~12-17KB with wrapper)
- Run with `python3 /tmp/gen_XX.py`
- NEVER use f-strings for HTML content — curly braces cause NameError
- Use triple-quoted strings for content blocks
- Print file sizes after creation to verify depth

**Batch size guidelines per script call:**
- 2 files: ~25KB script, reliable
- 3 files: ~35KB script, usually works
- 4+ files: script may be too large for single write_file call

## Batch Guide Creation from Prompt Files

When the user has predefined `学习提示词-P*.md` files listing topics and specifications:

1. **Read the prompt file first** — it contains exact file names, section structures, and depth requirements per topic.
2. **Create all directories upfront** — `mkdir -p` for each guide directory.
3. **Create all index.html files first** — navigation structure in place before content.
4. **Generate content in batches of 2-3 files per script** — write Python script to `/tmp/gen_XX.py`, run via `terminal`, repeat.
5. **Don't ask for confirmation between batches** — when user says "继续", they want the next batch, not a status update.
6. **Depth consistency audit after each guide** — thinnest file should be ≥60% of thickest file. If not, deepen before moving to next guide.

### Historical Development Guide Pattern
When creating a "从X到Y的发展历程" guide (e.g., "从深度学习到LLM"):
- Group models/technologies into **chronological phases** (3-5 phases)
- Index page uses **timeline layout** with phase headers and color-coded cards
- Each model gets a **standard 8-dimension page** with prev/next navigation
- Include **dependency chains** in the index (which models are prerequisites for others)
- Target 8-15KB per model page, 15-25 models total

## Multi-Vendor Deep-Dive Guide Creation (多厂商技术深度学习指南)

When creating "技术深度学习" guides for multiple vendors/models (e.g., Chinese LLM providers), follow this pattern:

### Unified Chapter Structure
Each vendor gets the same 12-file structure (index + 11 chapters):
```
Vendor/Vendor系列深度学习/
├── index.html                    ← Navigation with chapter list
├── 01-概述与演进时间线.html        ← Company history, model evolution timeline
├── 02-核心架构设计.html            ← Architecture (MoE/Dense, attention variant)
├── 03-注意力机制创新.html          ← Unique attention mechanism (MLA/CSA/Lightning/DSA)
├── 04-预训练策略与数据工程.html     ← Training data, optimizer, scaling
├── 05-后训练与对齐.html            ← SFT/RLHF/DPO/GRPO pipeline
├── 06-推理能力与长上下文.html       ← Context extension, reasoning mode
├── 07-Agent能力深度.html           ← Agent framework, tool calling, multi-agent
├── 08-系统工程与部署优化.html       ← Deployment, API pricing, hardware requirements
├── 09-性能评估与基准测试.html       ← Benchmark results, comparison tables
├── 10-应用场景与生态系统.html       ← Products, ecosystem, enterprise solutions
└── 11-论文精读与学习资源.html       ← Papers, GitHub, API docs, learning path
```

### Chapter Content Guidelines
- Each chapter: 150-250 lines, 8-15KB
- Must include ASCII architecture diagrams for key innovations
- Must include comparison tables (vs other vendors)
- Must include practical details (API pricing, deployment configs)
- Use consistent dark theme CSS across all vendors

### Cross-Reference Pattern
After creating deep-dive guides, add bidirectional cross-references:
- **Forward**: From vendor overview index → deep-dive index ("深入学习")
- **Reverse**: From deep-dive index → vendor overview ("厂商概览")
- **Cross-vendor**: Link to 2026年中模型更新全景.html for horizontal comparison

### Vendor Priority Order
When user asks "其他系列呢?", prioritize by market impact:
1. DeepSeek (MoE pioneer, MIT open source)
2. Qwen (largest model family, Apache 2.0)
3. Kimi (Agent Swarm, coding focus)
4. GLM (full-stack domestic, Huawei Ascend)
5. MiniMax (Lightning Attention, unique tech route)
6. ByteDance/豆包 (largest user base)
7. Xiaomi/MiMo (multimodal, ecosystem integration)
8. 百度/ERNIE (cost efficiency, search integration)

## Cross-Reference Injection Pattern (跨章节交叉引用)

When a knowledge base has multiple directories with no inter-links:
1. Identify high-value cross-reference pairs (e.g., basics ↔ deep-dive, theory ↔ practice)
2. Add a `<div class="highlight">` box before the footer in each file
3. Use relative paths from the current file to the target
4. Create bidirectional links (A→B and B→A)
5. Include a brief description of what the linked section covers

Example:
```html
<div class="highlight">
<strong>🔗 相关深入章节：</strong><br>
• <a href="../../02-模型架构/MoE训练与路由/index.html">MoE训练与路由</a> — 路由机制/负载均衡/通信优化
</div>
```

## Project-Level Audit Workflow (项目级审计)

When user asks to "整理" an entire learning project (500+ files):
1. **Inventory**: Count files and sizes per directory
2. **Identify empty shells**: Files with <20 lines (CSS-only, placeholders)
3. **Check missing index.html**: Every directory needs a navigation page
4. **Check cross-references**: Are sections linked to each other?
5. **Check content duplication**: Same topic in multiple directories?
6. **Check oversized content**: Directories that should be separate (e.g., 429MB PDFs)
7. **Create audit report**: Structured markdown with P0-P3 priorities
8. **Fix systematically**: P0 (empty shells, missing index) → P1 (thin files, cross-refs) → P2 (naming, organization)

## Cross-Platform Comparison Guide Pattern (对比学习指南)

When creating guides for competing platforms (e.g., NVIDIA vs Huawei, PyTorch vs JAX), create **parallel guide series** with a dedicated comparison chapter:

```
D:\学习\
├── NVIDIA集合通信\        ← Platform A (6 files)
│   └── 06-对比与面试.html  ← Cross-platform comparison
├── 昇腾超节点集合通信\     ← Platform B (6 files)
│   └── 06-面试专题.html    ← Cross-platform comparison
```

**Key design decisions:**
- Each platform gets its own complete guide (don't merge into one)
- Each guide's final chapter is a **cross-platform comparison** with:
  - Side-by-side spec tables (bandwidth, latency, scale, power)
  - Architecture philosophy comparison (not just numbers)
  - "Which to use when" decision framework
  - Interview questions covering BOTH platforms
- Navigation bars should **cross-link** to the other platform's guide
- Use the same CSS theme across both for visual consistency

**Research workflow:**
1. Search and create Platform A guide first (establishes CSS/template)
2. Search and create Platform B guide using same structure
3. Create comparison chapters last (need both platforms' data to compare)
4. Cross-validate claims across platforms

## SVG Diagram Upgrade Pattern (图要优化)
When the user says "图太简陋" / "ascii图不够" / "要更专业的图", upgrade key ASCII diagrams to SVG. Don't wait — the user considers ASCII diagrams a quality deficiency, not a stylistic choice.

**What to upgrade**: The top 8-12 most impactful diagrams per guide (architecture overviews, comparison visuals, topology diagrams). Leave simple 3-step flows and code-like structures as ASCII.

**SVG design system** (from `references/svg-diagram-integration.md`):
- Dark background: `#020617` with grid pattern `#1e293b`
- Semantic colors: cyan(frontend) / emerald(engine) / violet(storage) / amber(orchestration) / rose(hardware)
- Components: rounded rects with semantic fill+stroke, centered labels
- Arrows: `<marker>` definitions with color variants
- Layout: `viewBox` for responsive width, `overflow-x:auto` container

**Python generation pitfall (CRITICAL)**: f-strings with nested curly braces in HTML/SVG content cause `SyntaxError` or `TypeError`. Specifically, `{5 if not label2 else -2}` inside an f-string is parsed as a set literal. **Workaround**: compute values in separate variables, use string concatenation instead of f-strings for HTML:
```python
# WRONG: f'<text y="{y+h//2+{5 if not label2 else -2}}"'
# RIGHT:
yoff = -2 if label2 else 5
cx, cy = x+w//2, y+h//2+yoff
return '<rect x="'+str(x)+'" .../>'
```

**Workflow**: Generate SVGs via Python scripts to `/tmp/svg_upgrade_pN.py`, execute via `terminal`. Each script handles 2-3 files. Add `.diagram` CSS to all files for consistent styling.

## Forward Linking Pattern (向前串联 — 模块间逻辑关联)

A common weakness in multi-module guides: each module is self-contained but doesn't explain how it connects to later modules. The reader learns isolated topics without understanding the dependency chain.

**When to apply**: After creating all modules, add a "向前串联" section to each module (before the terminology table) that explicitly connects the current topic to later modules.

**Structure per module**:
```
X.Y.Z 向前串联：[当前主题]如何影响[后续主题]
  • 链条①: [具体机制] → 影响模块N的[具体方面]
  • 链条②: [具体机制] → 影响模块M的[具体方面]
  • 链条③: [具体机制] → 影响模块K的[具体方面]
  • ASCII因果链图: A → B → C → D (with module references)
```

**Example** (collective communication guide):
- Module 01 (Chips): "封装即命运" — TSV density → NVLink-C2C bandwidth (→module 04)
- Module 04 (NVLink): 14x bandwidth gap → NCCL path selection (→module 10)
- Module 05 (RDMA): Memory registration → NCCL init overhead (→module 10)
- Module 08 (Primitives): Communication volume formula → Algorithm choice (→module 13)

**Key rule**: Each "向前串联" must reference SPECIFIC later modules with concrete mechanisms, not vague "this is related to that". The reader should be able to follow the chain: "Because X in module A, Y happens in module B, which causes Z in module C."

Also add an "内部工作机制" (Internal Mechanism) section to modules that only explain "what" but not "how":
- Hardware modules: How does the physical mechanism work? (SerDes, crossbar, DMA, TLP routing)
- Software modules: How does the code/API actually execute? (call chain, kernel execution, stream management)
- Algorithm modules: Step-by-step data movement with concrete numbers

**Audit markers for these patterns**:
```bash
# Check forward linking coverage
grep -c '向前串联' module*.html    # Should be 1 per module (8+ for a 14-module guide)
grep -c '内部机制\|工作机制' module*.html  # Should be 1 per hardware/software module
```

## ASCII Diagram Consistency Standardization

When a guide has 50+ ASCII diagrams accumulated across multiple sessions, visual inconsistencies creep in. Standardize with this audit-and-fix workflow:

### Step 1: Audit character styles
```bash
echo -n "双线框 ╔═╗: " && grep -c '╔' *.html | awk -F: '{s+=$2}END{print s}'
echo -n "双线 ═: " && grep -c '═' *.html | awk -F: '{s+=$2}END{print s}'
echo -n "实心箭头 ▼: " && grep -c '▼' *.html | awk -F: '{s+=$2}END{print s}'
echo -n "空心箭头 ↓: " && grep -c '↓' *.html | awk -F: '{s+=$2}END{print s}'
```

### Step 2: Standardize to single convention
- **Boxes**: Always `┌─┐└─┘│` (single-line), never `╔═╗╚═╝║` (double-line)
- **Vertical flow**: Always `↓`, never `▼`
- **Horizontal flow**: `→` (general), `──→` (emphasis on key path)
- **Separators**: `───` (single), never `═══` (double)
- **Connection lines**: `──────` (single), never `══════` (double)

### Step 3: Batch fix with sed
```bash
# Fix double-line box characters → single-line
sed -i 's/═/─/g; s/╔/┌/g; s/╗/┐/g; s/╚/└/g; s/╝/┘/g; s/║/│/g; s/╦/┬/g; s/╩/┴/g; s/╠/├/g; s/╣/┤/g; s/╬/┼/g' *.html

# Fix solid arrows → open arrows
sed -i 's/▼/↓/g' *.html
```

### Step 4: Verify
```bash
echo -n "双线 ═: " && grep -c '═' *.html | awk -F: '{s+=$2}END{print s}'
echo -n "双线框 ╔: " && grep -c '╔' *.html | awk -F: '{s+=$2}END{print s}'
# Should both be 0
```

**Wide line check** (diagrams should fit in ~80-90 chars):
```bash
for f in *.html; do
  wide=$(sed -n '/class="ascii"/,/<\/div>/p' "$f" | awk 'length > 90' | wc -l)
  [ "$wide" -gt 0 ] && echo "$(basename $f): $wide wide lines"
done
```

## Theory-to-Practice Bridge Pattern (理论到实践的桥梁)

A common gap in deep technical guides: strong theory (formulas, algorithms, proofs) but weak practice (no code, no configs, no troubleshooting). The user will say "拿出写书的精神" and expect BOTH.

**When to apply**: After completing all theory modules, check if any module lacks code examples. If the guide covers algorithms/implementations but has 0 `<pre><code>` blocks, it's missing the practice dimension.

**Create a dedicated "实操" module** containing:
1. **API/Code examples** — Real code calling the theoretical primitives (e.g., `dist.all_reduce()` for collective communication)
2. **Configuration recipes** — Copy-paste configs (e.g., NCCL environment variables, DeepSpeed JSON)
3. **Benchmarking commands** — How to measure what the theory predicts (e.g., nccl-tests)
4. **Profiling workflow** — How to diagnose performance issues (e.g., PyTorch Profiler)
5. **Production case studies** — Real problems with root cause and solution
6. **Common mistakes** — Pitfalls that theory alone doesn't prepare you for

**Example**: Collective communication guide had Ring AllReduce theory (module 13, 105KB) but no PyTorch code. Fixed by adding module 14 (35KB) with DDP/FSDP/TP code, nccl-tests, Profiler, and 3 production cases.

## Breadth + Depth Audit (审查方法论)

When reviewing an existing guide, audit on TWO independent dimensions. See `references/breadth-depth-audit-methodology.md` for the full method.

**Quick version**:
1. **Breadth**: `grep -rl "keyword" *.html | wc -l` for every expected topic. Missing = gap.
2. **Depth**: Count markers per file: 为什么(Why), 工作方式(How), 公式(Formula), 代码(Code), 对比(vs), 图解(Diagram). Modules with <3 "为什么" or 0 "工作方式" are surface-level.
3. **Fix**: For each surface-level module, add design rationale, internal mechanism, formulas, code, and limitations.

## Subagent Rate-Limit Fallback Pattern

When `delegate_task` subagents hit HTTP 429 (rate limit) on their first API call:
1. **Don't retry immediately** — the rate limit persists for minutes
2. **Fall back to main agent** — do the patches directly with `patch` tool
3. **Reduce concurrency** — if 3 subagents all 429'd, try 2 or 1 next time
4. **Stagger with sleep** — add `sleep 3-5` between sequential calls

This was validated in a session where all 3 subagents hit 429 on first attempt, but the main agent's direct patches succeeded immediately.

## Pitfalls (精简版)

完整踩坑记录见 `references/pitfalls-consolidated.md`（35条，按7类整理）。核心要点：

**生成工具**：不要用delegate_task生成HTML(mimo超时)，用Python脚本+terminal。delegate_task可用于搜索(ddgs)。

**Python脚本**：不用f-strings(花括号冲突)、不用三引号嵌套、不用heredoc(静默失败)、每脚本2-3文件。

**SVG helper函数**：`box()` 等生成SVG rect+text的函数中，**禁止在f-string内嵌套花括号表达式**（如 `{5 if not label2 else -2}`）。Python会将其解析为set literal导致 `TypeError`。必须先计算值再拼接：
```python
# ❌ 错误 — 嵌套花括号
return f'<text y="{y+h//2+{5 if not label2 else -2}}" ...>'

# ✅ 正确 — 先计算再拼接
yoff = -2 if label2 else 5
cx, cy = x+w//2, y+h//2+yoff
return '<text x="' + str(cx) + '" y="' + str(cy) + '" ...>' + label + '</text>'
```
同样，HTML内容中含单引号时（如中文引号'超级GPU'），三引号字符串会提前终止。用字符串拼接代替三引号。

**HTML质量检查**：检查 `<p>` 标签平衡时，`<p` 正则会误匹配SVG内部标签（`<path`, `<polygon`, `<pattern`）。**必须先剥离SVG内容再计数**：
```python
svg_sections = re.findall(r'<svg.*?</svg>', content, re.DOTALL)
html_content = content
for svg in svg_sections:
    html_content = html_content.replace(svg, '')
# 然后在 html_content 上计数 <p>, <li> 等
```

**深度**：首次就要15-20KB，不要占位后期加深。批量后审计一致性(最薄≥最厚60%)。加深=整体重写+新增章节。

**内容**：禁用"强大/显著"等虚词。先基础后前沿。必须有作者视角(经验/判断/类比)。数据必须搜索验证。

**工作流**：说写就必须同一turn写(不要宣布-然后卡住)。用脚本批量(不要一turn一文件)。不要过早声明完成。

**文件**：路径`D:\学习\`，暗色HTML(不要markdown)，必须有导航。

**SVG升级**：只升级最复杂的1-2张图/文件(总计8-12张SVG)。语义化配色(青/翠绿/紫/琥珀/玫红)。每个SVG文件需要.diagram CSS。f-string花括号嵌套必须先算变量。

**覆盖度审计**：声明完成前必须做regex覆盖度扫描。基础设施指南必查：弹性扩缩、容错、API示例、成本分析。发现缺口优先patch现有文件，不新建。
