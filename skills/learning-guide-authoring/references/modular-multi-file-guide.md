# Modular Multi-File HTML Guide Architecture

## When to Use
When creating a learning guide with 10+ files on a single topic domain.

## Structure Principles
- **One topic per file** — self-contained, independently readable
- **Shared template** — Python generator script with CSS + NAV template for consistency
- **Cross-references via links** — files link to each other but never duplicate content
- **Index page with 3 views** — 按方法分类 (by method), 按问题分类 (by problem), 按场景分类 (by scenario)
- **Consistent nav sidebar** — every file has the same sidebar, current page highlighted

## Generation Workflow
1. Write generator script to /tmp/gen_XX.py
2. Script defines shared CSS string, NAV_ITEMS list, `make_nav(active_file)`, `wrap(fname, title, body)`, `save(fname, title, body)`
3. For existing content: extract body with regex `<div class="main">...<hr`
4. Run via `terminal("python3 /tmp/gen_XX.py")`
5. Verify: link integrity (`grep -oP 'href="\K[^"#]+\.html'`), section numbering (`grep -oP '<h2>\K\d+'`)

## HTML Fragment Merging Pattern (for large single-file guides)

When building a single large HTML file (>100KB) incrementally:

1. **Create initial content** → write to target path
2. **Create expansion fragments** → write to `/tmp/expansion_*.html` (no `<html>/<head>/<body>` tags)
3. **Merge with Python script** → write to `/tmp/merge.py`:
   ```python
   with open('main.html', 'r') as f: main = f.read()
   with open('/tmp/fragment.html', 'r') as f: fragment = f.read()
   marker = '<footer style='  # reliable anchor
   idx = main.find(marker)
   new = main[:idx] + fragment + '\n\n' + main[idx:]
   with open('main.html', 'w') as f: f.write(new)
   ```
4. **Run via** `terminal("python3 /tmp/merge.py")`
5. **Verify** with `wc -l -c` and `search_files` count mode

**Why this pattern:**
- `write_file` for content >50KB may hit limits
- `patch` tool requires exact string matching — fragile for large inserts
- Python script via `write_file` + `terminal` is the most reliable approach
- Footer marker `<footer style="text-align:center` is unique and always at file end

## Pitfalls
- **Section numbering breaks on patch** — after any `patch` adding/renumbering h2/h3, verify numbers are sequential with no gaps or duplicates
- **Merged files** — keep each part's original section numbers, use visual divider, don't cascade-renumber 10+ sections
- **Large body content (>15KB)** — generate via /tmp Python script + terminal, not inline in execute_code
- **read_file format varies** — when reading files in execute_code, dict keys may differ; use `open()` as fallback
- **execute_code with hermes_tools read_file truncates** at ~500 lines / ~75KB — use `open()` directly for large files

## User Preferences (this user, 2026-06)
- "高内聚，低耦合" — strict modular separation, no duplication
- "务必做到详尽" — thoroughness critical; audit keyword coverage per module
- Problem-scenario classification valued alongside method-based classification
- Chinese content, dark theme, ASCII diagrams, code examples, exercises
- Prefers "将提示词写进文档" — save prompts as .md docs first, don't execute immediately
