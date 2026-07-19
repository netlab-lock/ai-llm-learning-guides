# Batch Guide Generation from Learning Checklists

When the user has a checklist file (like `学习提示词-P3.md`) with multiple topics to generate as learning guides, use this workflow to create them efficiently.

## Pattern: Checklist-Driven Batch Generation

### Step 0: Read the Checklist
Read the checklist file to understand all topics, their output paths, and required files per topic.

### Step 1: Research All Topics in Parallel
Use `delegate_task` with `toolsets=["terminal"]` + `ddgs text -q '...' -m 5`.

**CRITICAL**: Max `max_concurrent_children=3`. Split research into batches of 3 topics each. Example for 6 topics:
- Batch 1: Topics 1-3 (runs in ~120s)
- Batch 2: Topics 4-6 (runs in ~180s)

Each research task should search 2-3 queries per topic and return structured findings with URLs.

### Step 2: Generate Topic Files Sequentially
For each topic:
1. `mkdir -p` for the topic directory
2. Write a Python script to `/tmp/gen_TOPIC.py` that creates all files (index + modules)
3. Run via `terminal("python3 /tmp/gen_TOPIC.py")`
4. Verify file sizes with `wc -c`

**Do NOT** try to generate all topics in one script — it will timeout. One topic per script.

### Step 3: Verify Depth Consistency
After all topics are generated:
```bash
for dir in /path/to/topic*/; do
  echo "=== $(basename $dir) ==="
  for f in "$dir"*.html; do
    size=$(wc -c < "$f")
    echo "  $(basename $f): $((size/1024))KB"
  done
done
```

Target: each module file 14-21KB. If any file is under 12KB, deepen it.

### Step 4: Verify HTML Structure
```bash
for f in $(find . -name "*.html" | sort); do
  opens=$(grep -o '<div' "$f" | wc -l)
  closes=$(grep -o '</div>' "$f" | wc -l)
  [ "$opens" -ne "$closes" ] && echo "DIV MISMATCH: $f"
done
```

## Pitfalls

1. **delegate_task max is 3 concurrent** — splitting 6 research tasks into one call fails with "Too many tasks: 6 provided, but max_concurrent_children is 3". Always batch in groups of 3.
2. **Python script per topic, not one giant script** — a script generating 42 files across 6 topics will timeout. Split into one script per topic (~7 files each).
3. **Chinese paths in PowerShell** — when running Python scripts from WSL targeting `/mnt/d/学习/`, use the WSL path directly. PowerShell encoding issues only affect Windows-side execution.
4. **write_file in execute_code requires 'path' param** — omitting causes silent failure loop (documented in execute_code quirks).
5. **Don't use f-strings for HTML templates** — CSS/JS curly braces cause NameError. Use string concatenation or `CSS` variable extracted from existing file.
6. **Research data quality** — ddgs search may return empty on some queries. Always include fallback queries and use arxiv direct lookups as backup.
7. **File size targets for batch guides** — same as single guides (14-21KB per module), but be aware that the first topic often gets more depth than later ones due to fatigue. Audit consistency after completion.
8. **Python script fallback to write_file** — If Python scripts fail due to HTML escaping issues (backslashes in ASCII art, CSS curly braces, nested quotes), fall back to `write_file` directly for each HTML file. This is slower (1 file per call) but 100% reliable. For 42 files across 6 topics, expect ~40-50 turns with `write_file` vs ~15 turns with Python scripts. The tradeoff is reliability vs speed.
9. **Overview modules don't need 14KB** — Modules 01 (总览) and 05-06 (前沿/总结) naturally stay at 5-8KB. They serve as navigation and orientation, not deep technical content. Don't waste turns trying to deepen them to 14KB. Focus deepening effort on modules 02-04 (core technical content).
