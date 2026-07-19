# Guide System Gap Analysis & Phased Expansion Workflow

Used when the user has an existing multi-directory guide system and wants to systematically identify gaps and expand.

## Phase 1: Audit

1. **Inventory all directories** — `find <root> -maxdepth 1 -type d | sort`
2. **Count files per directory** — `for dir in */; do count=$(find "$dir" -name "*.html" ! -name "index.html" | wc -l); size=$(du -sh "$dir" | cut -f1); echo "$dir | $count files | $size"; done`
3. **Check subdirectories** — `for dir in */; do find "$dir" -mindepth 1 -maxdepth 1 -type d; done`
4. **Identify thin directories** — any directory with < 5 files or < 50KB deserves scrutiny
5. **Read index.html files** — understand the declared scope vs actual coverage

## Phase 2: Gap Analysis

Organize gaps by priority:
- **P0 — Core gaps** that break knowledge system completeness (e.g., missing a whole paradigm shift)
- **P1 — Important gaps** that affect practical capability (e.g., missing deployment guides)
- **P2 — Nice-to-have** frontier topics

For each gap, estimate:
- Number of files needed (typically 6-15 per topic)
- Directory placement (new directory vs subdirectory of existing)
- Dependencies on other topics

## Phase 3: Phased Execution

Split into 2-3 phases:
- **Phase 1**: Core gaps (highest impact, most files)
- **Phase 2**: Practical capability gaps
- **Phase 3**: Frontier/deep-dive topics

Each phase can be parallelized:
1. Create all directories first
2. Delegate file creation in parallel batches (5 files per worker)
3. Update all index.html files after content is created

## Index Update Pattern

After creating new content, update indexes at 3 levels:

### Subdirectory index.html
Standard card-grid layout linking to all files in the directory.

### Parent directory index.html
Add a new card to the existing card-grid:
```html
<a href="NewDir/index.html" class="card" style="text-decoration:none">
  <div class="card-title">🏷️ New Directory</div>
  <div class="card-desc">Brief description of content.</div>
  <span class="card-tag">Category</span>
</a>
```

### Root index.html
Add a new `dir-card` section with full file listing:
```html
<div class="dir-card">
  <div class="dir-card-header">
    <div class="dir-icon">🧠</div>
    <h3><a href="NewDir/">NewDir</a></h3>
  </div>
  <div class="dir-meta">
    <span class="dir-badge">N 个文件</span>
    <span class="dir-badge">XXX KB</span>
  </div>
  <p class="dir-desc">Description.</p>
  <div class="dir-subs"><h4>专题目录</h4><ul>
    <li><a href="NewDir/01-File.html">01 Title</a></li>
    ...
  </ul></div>
</div>
```

Use `search_files` to find insertion points (before `<!-- 提示词 -->` or similar markers), then `patch` to insert.

## Verification

After all phases complete:
```bash
total=$(find <root> -name "*.html" | wc -l)
size=$(du -sh <root> | cut -f1)
lines=$(find <root> -name "*.html" -exec wc -l {} + | tail -1 | awk '{print $1}')
echo "$total files | $size | $lines lines"
```

## Example: 2026-06 AI-LLM Expansion

- **Audit**: 699 HTML files across 14 directories, 54MB
- **Gaps identified**: Reasoning models, multimodal generation, international LLM vendors, Agent depth, data engineering, AI infra
- **Phase 1**: 67 files (reasoning + multimodal + 5 vendors)
- **Phase 2**: 37 files (Agent + data eng + AI infra)
- **Result**: 879 HTML files, 56MB, 166K lines
