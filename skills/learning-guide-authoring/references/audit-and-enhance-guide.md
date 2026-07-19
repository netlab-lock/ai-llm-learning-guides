# Audit & Enhance Existing Learning Guides

Workflow for systematically reviewing and upgrading existing HTML learning guides.

## When to Use

- User says "再检查一遍", "查缺补漏", "更加详尽", "补充更多知识点"
- User asks to check for new developments ("最近有没有新技术")
- User wants multi-angle content (面试/工作/研究/学习)
- Existing guide was created months ago and needs updating

## Step 1: Inventory & Gap Analysis

```python
from hermes_tools import read_file
import re

files = [...]  # list of HTML files
for f in files:
    result = read_file(path, offset=1, limit=2000)
    content = result["content"]
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    ascii_count = len(re.findall(r'class="ascii"', content))
    table_count = len(re.findall(r'<table', content))
    tip_count = len(re.findall(r'class="tip"', content))
    warn_count = len(re.findall(r'class="warn"', content))
    # Report per-file stats
```

Output a table: module name, line count, word count, ASCII count, table count, tip count, warn count.

## Step 2: Keyword Coverage Check

```bash
base='/path/to/guide/'
for kw in 'keyword1' 'keyword2' ...; do
  cnt=$(grep -rl "$kw" ${base}*.html 2>/dev/null | wc -l)
  if [ $cnt -eq 0 ]; then echo "❌ $kw"; fi
done
```

Build a list of 30-50 domain keywords. Any uncovered keyword = a gap to fill.

## Step 3: Web Search for New Developments

Use `ddgs text -q "topic 2025 2026 latest" -m 5` with 3-5 second delays between searches.
Focus on: new hardware generations, new library versions, new papers, new standards.

**Pitfall**: ddgs rate-limits after 2-3 rapid queries. Add `sleep 5` between calls.

## Step 4: Parallel Enhancement via Subagents

```python
delegate_task(tasks=[
    {"goal": "Read file X, add section Y before Z", "toolsets": ["file"]},
    {"goal": "Read file A, add section B before C", "toolsets": ["file"]},
    {"goal": "Read file D, add section E before F", "toolsets": ["file"]},
])
```

**Pitfall**: Max 3 concurrent subagents. mimo model hits HTTP 429 with more.
**Pitfall**: Subagents don't have web_search — use `toolsets=["file"]` not `["web"]`.
**Pitfall**: If subagent hits 429, do the task directly with `patch` tool instead.

## Step 5: Direct Patches for Remaining Gaps

Use `patch` tool with `mode="replace"` to insert content before known anchor text.
Always include enough context in `old_string` for unique matching.

## Step 6: Create Summary Document

Build a "知识全景图" (knowledge overview) HTML that includes:
- Knowledge architecture diagram (ASCII)
- Module content map table
- Interview question bank (分级: 入门/中级/高级/专家)
- Production tuning guide / checklist
- Research frontier trends
- Learning path (day-by-day schedule)
- One-page cheatsheet (bandwidth, formulas, env vars, parallelism patterns)
- Related fields overview

## Multi-Angle Content Addition

When user asks for 面试/工作/研究/学习 angles:

| Angle | Content Type | Example |
|-------|-------------|---------|
| 面试 | Q&A with detailed answers, 分级难度 | "Q: AllReduce通信量？ A: 2D(N-1)/N" |
| 工作 | Env vars, tuning checklist, fault diagnosis | NCCL_DEBUG=INFO workflow |
| 研究 | Paper recommendations, trend analysis | "DualPipe (DeepSeek-V3, 2024)" |
| 学习 | Day-by-day path, prerequisite graph | "Day 1: 芯片基础→GPU架构" |

## Pitfalls

- **HTML file too large for patch**: If a file exceeds ~60KB, patches may fail. Split content into new files.
- **Section renumbering**: When inserting new sections (e.g., 3.9 → 3.10), manually update all subsequent section numbers.
- **Cross-file links**: When adding a new module, update index.html AND the next-prev links in adjacent modules.
- **Subagent style consistency**: Always specify "Follow the same HTML style: dark theme, class='ascii', class='tip', Chinese language" in the goal.

## Research-Then-Update Workflow (validated 2026-06)

When user says "检查X做得怎么样" — they want BOTH audit AND update in one session.

### Phase 1: Audit (parallel)
1. `search_files` with multiple patterns to find all related files
2. Read key files (overview, comparison, individual deep-dives)
3. `ddgs text` for current state-of-the-art (3-5 queries)
4. Build gap analysis: existing content vs current reality

### Phase 2: Report to user
Present findings as:
- ✅ What's good (quality assessment)
- ❌ What's missing (gaps with priority P0/P1/P2)
- ⚠️ What's outdated (wrong status, stale versions)

### Phase 3: Execute updates (with user approval)
Use TODO tracking for systematic execution:
1. Create new files first (write_file)
2. Update existing files (patch for small changes)
3. Fix navigation links last
4. Update README/index files

### Key insight
Users who ask "检查+评判" expect you to ALSO do the updates, not just report. The audit is the first half; fixing is the second. Don't wait for explicit "请更新" — proceed after presenting the gap analysis.
