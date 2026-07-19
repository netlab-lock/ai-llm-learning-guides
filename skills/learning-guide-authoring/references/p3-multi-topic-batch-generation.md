# P3 Multi-Topic Batch Generation Workflow

Workflow validated across a 42-file, 6-topic session (2026-05-27).

## Session Stats
- 6 topics × 7 files each = 42 HTML files
- Final total: 371KB
- Core modules (02-04): 9-17KB each
- Overview/summary modules (01, 05, 06): 5-8KB each
- Enrichment passes: 15+ rounds

## Workflow

### Phase 1: Research (parallel)
Run 3 parallel delegate_task subagents searching for all topics upfront:
```python
delegate_task(tasks=[
    {"goal": "Search for Topic1 latest research via ddgs CLI", "toolsets": ["terminal"]},
    {"goal": "Search for Topic2 latest research via ddgs CLI", "toolsets": ["terminal"]},
    {"goal": "Search for Topic3 latest research via ddgs CLI", "toolsets": ["terminal"]},
])
```
Then another batch of 3 for remaining topics. Total research time: ~3-4 minutes.

### Phase 2: Create directories and index files
```bash
mkdir -p "/mnt/d/学习/AI-LLM技术/Topic1" "/mnt/d/学习/AI-LLM技术/Topic2" ...
```
Create all index.html files first (establishes structure).

### Phase 3: Generate content files
Use `write_file` directly for each HTML file. One file per call.
- Start with core modules (02-04) — these are most important
- Then overview (01) and summary (05, 06)
- Each file takes ~1 second to write
- Expected output: 4-8KB per file (Python scripts trade depth for speed)

### Phase 4: Depth consistency audit
```bash
for d in Topic1 Topic2 ...; do
  for f in "/path/$d"/*.html; do
    a=$(grep -c 'class="ascii"' "$f")
    c=$(grep -c '<pre><code>' "$f")
    if [ "$a" -lt 2 ] || [ "$c" -lt 1 ]; then
      echo "NEEDS WORK: $d/$(basename $f): ${a}图 ${c}码"
    fi
  done
done
```

### Phase 5: Enrichment passes
Focus on files missing diagrams/code blocks. Rewrite ENTIRE files (not incremental appends).
Target: +5KB per deepening pass on core modules.

## Key Learnings
1. **Research all topics upfront** — don't interleave research and creation
2. **write_file is more reliable than Python scripts** for HTML with ASCII art and backslashes
3. **Core modules (02-04) are most important** — prioritize depth there
4. **Overview modules (01, 05, 06) naturally stay shorter** — 5-8KB is acceptable
5. **Incremental deepening (1-2KB per pass) is futile** — rewrite entire files for substantial growth
6. **Quality audit has TWO dimensions** — file size AND content richness (diagrams + code)
