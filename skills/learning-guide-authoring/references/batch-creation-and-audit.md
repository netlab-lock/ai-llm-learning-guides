# Batch HTML Guide Creation & Content Audit

## Pitfall: Two CSS Style Conventions in AI-LLM技术 Project

The project has TWO distinct CSS styles. When repairing or adding files to an existing directory, MUST match the convention already used there:

### Style A: Sidebar Nav (newer files, used in 2025+)
- Fixed left sidebar (260px) with all chapter links
- `.nav` class, `.nav-title`, `.nav a.active`
- `.main { margin-left: 260px }`
- Used in: 11-推理模型, Agent深度实战, 多模态生成, 国际LLM-*, AI基础设施, 端侧部署, AI-Coding, 模型安全进阶, 推理时计算

### Style B: Inline Top-Bar Nav (older files, 2024 era)
- Horizontal nav bar at top with chapter links
- `.nav { display:flex; flex-wrap:wrap; gap:8px }`
- No sidebar, content centered with `max-width:1000px; margin:0 auto`
- Used in: RLHF训练深度, 模型量化前沿, LLM评测体系, 训练数据工程, 分布式训练系统

**Rule**: Before writing files into an existing directory, read the first 3 lines of one existing file to detect which style is in use.

## Pitfall: Python f-strings with HTML Content

When using `execute_code` to write HTML, NEVER use f-strings for HTML content containing curly braces in math/variable notation like `{r_1, r_2, ..., r_k}`. Python will interpret these as variable references and throw `NameError`.

**Solution**: Use the `write_file` tool directly instead of `execute_code` with f-strings.

## Parallel File Creation Workflow

When creating 10+ HTML files:
1. Create the directory with `terminal("mkdir -p ...")`
2. Use `delegate_task` with `role: "leaf"` and `toolsets: ["file"]`
3. Batch 3-4 files per worker for MiMo (5-6 for stronger models). **Pitfall**: 10+ files per delegate_task causes timeouts with MiMo.
4. Each worker must receive: exact CSS template, nav sidebar HTML, content plan per file
5. Verify with `terminal` after each batch: count files, check sizes
6. **Pitfall**: MiMo 429 rate limiting — add 10s cooldown between delegate_task calls

### Proven Pattern: Orchestrator Parallel Delegation (2026-06 validated)

For creating 10-15 substantial HTML modules (500-800 lines each, 22K+ total):

1. **Plan modules first** — list all file names, key topics per module, and target line counts
2. **Create directory** — `terminal("mkdir -p ...")`
3. **Delegate in batches of 3** using `role: "orchestrator"` with 3 tasks:
   - Each task specifies: save path, all sections to cover, design requirements, target lines
   - Include "read existing HTML first for style reference" in task instructions
   - Use `toolsets: ["file", "terminal", "web"]` for sub-agents that need web research
4. **Run 4-5 batches sequentially** — each batch creates 3 files (~1800-2500 lines per batch)
5. **Verify after all batches** — `wc -l`, `du -h`, check filenames
6. **Patch parent index.html** — add card linking to new guide
7. **Fix filename inconsistencies** — sub-agents may produce inconsistent spacing/casing

**Token budget**: Each sub-agent task (~30K output tokens per 700-line module). MiMo handles this well.
**Time**: ~10min per batch of 3 modules. Full 14-module guide ≈ 50min total.
**Quality**: Sub-agents produce self-contained HTML with inline SVG, tables, code blocks. Review for consistency but content is usually solid.

### Pitfall: Sub-Agent Filename Inconsistency

Sub-agents may produce filenames with spaces or different conventions (e.g., `13-KV Cache工程调优实战.html` vs `13-KV-Cache工程调优实战.html`). **Always run a rename check** after all batches complete:
```bash
cd /path/to/dir && for f in *; do new=$(echo "$f" | sed 's/ /-/g'); [ "$f" != "$new" ] && mv "$f" "$new"; done
```

## Pitfall: Patch Mode Creates Duplicate Lines (2026-06 validated)

When using `patch` action with `mode: "patch"`, if the `old_string` matches an existing line but the `new_string` APPENDS new content after it (instead of replacing), the result is **both the old and new lines coexisting**. This happened when fixing numerical values in tables — the old row stayed and the corrected row was added below.

**Prevention**: After every `patch` operation, verify with `grep -c` that the old value no longer exists:
```bash
grep -c "old_value" file.html  # should be 0 after fix
```

**Recovery**: Use `replace` mode to remove the duplicated old lines, or use `execute_code` with direct string replacement on the file content.

## Pitfall: Sub-Agent Nav-Bar Inconsistency (2026-06 validated)

Sub-agents create **wildly different navigation patterns** even within the same guide:
- Some create `nav-bar` with simple prev/next links
- Some create `nav-logo` + `nav-links` with section anchors
- Some create no navigation at all
- Some use `← / →` arrows, others use `上一章 / 下一章`

**Post-creation fix**: After all batches complete, run a standardization pass:
1. Define a canonical nav-bar template with: `← 目录 | ← 上一模块 | 模块标题 | 下一模块→ | 目录→`
2. For each file: `grep -n "nav-bar\|<body>" file.html` to find the insertion point
3. If file has a nav-bar: replace the entire `<nav>...</nav>` block
4. If file has no nav-bar: insert after `<body>`
5. Verify: `for f in *.html; do grep -c "nav-bar" "$f"; done` — all should be ≥1

**Canonical template**:
```html
<nav class="nav-bar">
  <a href="00-index.html">← 目录</a>
  <span style="opacity:0.4">|</span>
  <a href="PREV_FILE.html">← PREV_TITLE</a>
  <span class="title">模块NN: TITLE</span>
  <a href="NEXT_FILE.html">NEXT_TITLE →</a>
  <a href="00-index.html">目录 →</a>
</nav>
```

## Content Audit Methodology

**IMPORTANT**: Always load the `learning-guide-quality-rubric` skill first! It defines the 5-dimension scoring system (内容密度/教学设计/结构完整性/知识准确性/可读性) and S/A/B/C/D/F grading. Do NOT just count lines.

### Step 1: Python-Based File Analysis (NOT shell)
**Pitfall**: Shell-based `grep -c` / `sed | wc -c` fails on files with special characters, spaces in paths, or nested quotes. The bulk scan will return 0 chars for files that actually have 800+ lines. Use Python `open()` + `re` directly.

```python
import os, re
from hermes_tools import terminal

base = "/path/to/project/"
result = terminal("find '" + base + "' -name '*.html' ! -name 'index.html' -type f")
all_files = [f.strip() for f in result['output'].strip().split('\n') if f.strip()]

records = []
for fp in all_files:
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    text = re.sub(r'<[^>]*>', '', content)
    chars = len(re.sub(r'\s+', '', text))
    h2 = len(re.findall(r'<h2', content))
    h3 = len(re.findall(r'<h3', content))
    tables = len(re.findall(r'<table', content))
    pre = len(re.findall(r'<pre', content))
    tips = len(re.findall(r'class="tip', content))
    warns = len(re.findall(r'class="warn', content))
    deeps = len(re.findall(r'class="deep', content))
    ascii_c = len(re.findall(r'class="ascii', content))
    svg = len(re.findall(r'<svg', content))
    size_kb = len(content.encode('utf-8')) // 1024
    records.append({'file': fp.replace(base, ''), 'chars': chars, 'h2': h2, 'h3': h3,
                    'tables': tables, 'pre': pre, 'tips': tips, 'warns': warns,
                    'deeps': deeps, 'ascii': ascii_c, 'svg': svg, 'size_kb': size_kb})
```

Then apply the rubric's 5-dimension scoring formula to grade each file.

### Step 2: SVG Validation
Use `search_files` to count `<svg[\s>]` and `</svg>` patterns. Counts must match per directory.

### Step 3: HTML Structure Check
Use `search_files` to count `</html>` per file. Each file must have exactly 1.

### Step 4: Priority Classification (per rubric)
- C级 (< 300分): Major rewrite — add content + all pedagogical elements (tip/warn/deep/ASCII/table)
- B级 (300-379): Enhancement — add missing pedagogical elements
- A级 (380-449): Good, minor optimization only
- S级 (450+): Benchmark quality, maintain only

### Step 5: Content Depth Metrics (per file)
```bash
for f in *.html; do
  lines=$(wc -l < "$f")
  tables=$(grep -c "<table" "$f" 2>/dev/null || echo 0)
  svgs=$(grep -c "<svg" "$f" 2>/dev/null || echo 0)
  callouts=$(grep -c "callout" "$f" 2>/dev/null || echo 0)
  analogies=$(grep -c "通俗\|类比\|直觉" "$f" 2>/dev/null || echo 0)
  echo "$f: L=$lines T=$tables SVG=$svgs callout=$callouts 类比=$analogies"
done
```
Targets per module: lines≥600, tables≥3, SVGs≥3, callouts≥3.
Modules with 0 analogies/类比 keywords = missing three-layer explanation pattern (P1).

### Step 6: Technical Accuracy Spot-Check
For numerical-heavy guides, verify 2-3 key calculations manually:
- Check model parameter counts (L, n_heads, d_head) against known specs
- Verify derived quantities (memory = f(params))
- Check environment variable names against official docs
- Verify paper attributions (author, year, institution)

### Step 7: Cross-Reference Check
```bash
for f in *.html; do refs=$(grep -c "模块\|Module" "$f"); echo "$refs refs  $f"; done
```
Modules with 0 cross-references = isolated content (P2).

## Index File Update Pattern

When adding new subdirectories to an existing directory, patch the parent `index.html`:
1. Find the last card in the `.card-grid` before `</div>`
2. Insert new `<a href="..." class="card">` block before the closing `</div>`
3. Also update the main `index.html` at the project root if adding a top-level directory

## Typical Session Output Scale

A single session can produce:
- 3 parallel delegate_task batches × 5 files = 15 files per round
- 3-4 rounds = 45-60 files in one session
- Plus index updates and quality audits
- Total realistic output: 100-150 HTML files in a focused session
