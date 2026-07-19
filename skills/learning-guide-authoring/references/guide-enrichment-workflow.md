# Guide Enrichment Workflow (4-Phase Audit & Enhance)

When the user says "查缺补漏/检查一遍/补充内容/做的更详尽/再丰富一点", follow this systematic 4-phase workflow.

## Phase 1: Systematic Audit

### Step 1.1: Extract Structure from ALL Files
```python
# Audit script — generates depth report for all guide files
import os, re
guide_dir = "/path/to/guide"
files = sorted([f for f in os.listdir(guide_dir) if f.endswith('.html') and f != 'index.html'])
print(f"{'File':<40} {'Lines':>6} {'KB':>6} {'H2':>4} {'H3':>4} {'Tables':>7} {'ASCII':>6} {'Tips':>5} {'Warn':>5}")
for fname in files:
    path = os.path.join(guide_dir, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.count('\n')
    kb = len(content) / 1024
    h2 = len(re.findall(r'<h2', content))
    h3 = len(re.findall(r'<h3', content))
    tables = len(re.findall(r'<table', content))
    ascii_blocks = len(re.findall(r'class="ascii"', content))
    tips = len(re.findall(r'class="tip"', content))
    warns = len(re.findall(r'class="warn"', content))
    print(f"{fname:<40} {lines:>6} {kb:>6.1f} {h2:>4} {h3:>4} {tables:>7} {ascii_blocks:>6} {tips:>5} {warns:>5}")
```

### Step 1.2: Search for Missing Keywords
Build a list of topics that SHOULD be covered. For each keyword, grep in BOTH English and Chinese:
```bash
base='/path/to/guide/'
for kw in 'keyword1' '关键词2' 'keyword3'; do
  cnt=$(grep -rl "$kw" ${base}*.html 2>/dev/null | wc -l)
  if [ $cnt -eq 0 ]; then echo "  ❌ $kw"; else echo "  ✅ $kw ($cnt files)"; fi
done
```

**Pitfall**: English keywords in grep miss Chinese content (e.g., "overlap" misses "重叠"). Always check both languages.

### Step 1.3: Build Gap Matrix
Create a matrix: module × gap type:
- **Missing topics**: completely absent from the guide
- **Shallow coverage**: mentioned but not explained in depth
- **Outdated info**: needs updating with latest developments
- **Missing angles**: no interview questions, no practical examples, no debugging guide

## Phase 2: Targeted Enhancement

### Step 2.1: Prioritize
1. Completely missing topics (highest impact)
2. Shallow coverage of important topics
3. Outdated information
4. Missing interview/work angles

### Step 2.2: Parallel Enhancement
Use **delegate_task with max 3 subagents** for independent module enhancements:
```python
delegate_task(tasks=[
    {"goal": "Read FILE_A and add [topic] content BEFORE 术语速查表...", "toolsets": ["file"]},
    {"goal": "Read FILE_B and add [topic] content BEFORE 术语速查表...", "toolsets": ["file"]},
    {"goal": "Read FILE_C and add [topic] content BEFORE 术语速查表...", "toolsets": ["file"]},
])
```

**Pitfall**: Max 3 subagents (429 rate limit errors with 4+). Run multiple batches if needed.

### Step 2.3: Content Requirements
Each enhancement MUST include:
- **ASCII diagram** explaining the concept visually
- **Comparison table** showing trade-offs or evolution
- **Tip or Warn box** with practical insight
- **Concrete examples** with numbers (bandwidth, latency, compression ratio)

### Step 2.4: Insertion Point
Standard insertion point: **BEFORE the 术语速查表 section** in each module. Search for `术语速查表` as anchor.

## Phase 3: Multi-Angle Enrichment

### Step 3.1: Interview Questions
Add "🆕 面试深度题与工作实战" sections to core modules (4-5 questions per module):
- Questions at 4 difficulty levels: ⭐⭐ 入门 → ⭐⭐⭐ 中级 → ⭐⭐⭐⭐ 高级 → ⭐⭐⭐⭐⭐ 专家
- Each question has: question text, detailed answer, module reference
- Include "工作实战" subsection with production configs

### Step 3.2: Production Environment
Include real-world configurations:
- NCCL environment variable presets (company-specific: Meta, Google, NVIDIA, ByteDance)
- Debugging workflows (decision trees for common failures)
- Performance benchmarking commands (nccl-tests, ib_write_bw)
- Troubleshooting tables (symptom → cause → fix)

## Phase 4: Knowledge Summary ("知识全景图")

Create a comprehensive summary file that ties everything together from 4 dimensions:

### 4.1 面试速查 (Interview Quick Reference)
- TOP 20 questions organized by difficulty level
- Brief answers with module references
- One-page formula/cheat sheet

### 4.2 工作实战 (Work Practice)
- Tuning guides (environment variables, parameters)
- Troubleshooting decision trees (ASCII flowcharts)
- Performance benchmarks (theoretical vs actual)

### 4.3 研究前沿 (Research Frontier)
- 6 major technology trends with impact ratings
- Recommended papers table (title, year, contribution, source)
- Technology landscape diagram

### 4.4 学习路径 (Learning Path)
- Day-by-day study plan with checkpoints
- Knowledge dependency graph (ASCII)
- "检验" criteria for each stage

### 4.5 Additional Sections
- **一页速查表**: bandwidth, communication volume formulas, key configs
- **相关领域速览**: adjacent topics (memory optimization, profiling tools, distributed frameworks)
- **并行策略与通信原语对照**: mapping table of parallelism strategies to collective operations

## Pitfalls (Enrichment-Specific)

1. **Max 3 subagents** — HTTP 429 rate limits with 4+
2. **Check both EN/CN keywords** — grep for "overlap" AND "重叠"
3. **Update ALL nav links** — after adding new modules, fix forward/back links in existing modules
4. **Always update index.html** — add new badges, roadmap, module cards
5. **First output must be comprehensive** — user will keep pushing "更详尽"; don't save depth for round 2
6. **Insertion point consistency** — always BEFORE 术语速查表, not at end of file
7. **Verify after each phase** — re-run audit script to check improvements
8. **Skill size limit** — if SKILL.md hits 100KB, put detailed workflows in references/ files
