# HTML Generation Patterns for Learning Guides

## Reliable Methods (ranked by reliability)

### 1. Direct write_file (most reliable, one file per call)
```python
from hermes_tools import write_file
write_file("/mnt/d/学习/Topic/file.html", html_content)
```
- **Pros**: Always works, immediate feedback on file size
- **Cons**: Slow for many files (one call per file)
- **Use when**: < 10 files, or when other methods fail

### 2. Python script via terminal (fast for many files)
```bash
# Write script to /tmp/ first, then execute
cat > /tmp/gen_topic.py << 'PYEOF'
#!/usr/bin/env python3
import os
# ... script content ...
PYEOF
python3 /tmp/gen_topic.py
```
- **Pros**: Fast (many files in one call)
- **Cons**: Heredoc sometimes fails silently (file not written), string escaping issues
- **Pitfall**: ALWAYS verify the script exists before running: `ls -la /tmp/gen_topic.py`

### 3. execute_code (for small batches of 1-3 files)
```python
from hermes_tools import write_file
# Create 2-3 files in one call
write_file("path1.html", content1)
write_file("path2.html", content2)
```
- **Pros**: Good for small batches
- **Cons**: String escaping issues with triple quotes containing HTML

## CSS Extraction Pattern (MANDATORY for consistency)

When creating multiple files for the same guide, extract CSS from an existing file:

```python
# From terminal
CSS = open("/path/to/existing.html").read().split("<style>")[1].split("</style>")[0]

# Or from terminal command
# sed -n '/<style>/,/<\/style>/p' /path/to/file.html
```

**Never hardcode CSS** in each file — extract once, reuse everywhere.

## HTML Template Function Pattern

```python
def hp(title, prev, nxt, nav_title, body):
    pv = '<a href="{}">&larr; {}</a>'.format(prev, prev.replace('.html','')) if prev else '<span></span>'
    nx = '<a href="{}">{} &rarr;</a>'.format(nxt, nxt.replace('.html','')) if n nxt else '<span></span>'
    return ('<!DOCTYPE html>\n<html lang="zh-CN">\n<head><meta charset="UTF-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
            '<title>'+title+'</title>\n<style>'+CSS+'</style>\n</head>\n<body>\n'
            '<div class="nav">'+pv+'<span>'+nav_title+'</span>'+nx+'</div>\n'
            '<div class="container">\n'+body+'\n</div>\n'
            '<div class="footer"><p><a href="index.html">返回总览</a></p></div>\n</body>\n</html>')
```

**Key rule**: Use `.format()` or string concatenation, NOT f-strings, when the HTML content contains curly braces (CSS, JSON examples).

## String Escaping Pitfalls

### Problem: Triple-quoted strings with HTML
```python
# THIS FAILS with SyntaxWarning for backslashes
content = '''
<pre><code>def foo():
    path = "C:\\Users\\test"  # ← backslash causes issues
</code></pre>
'''
```

### Solution: Use write_file directly instead of embedding in Python
```python
# Write HTML content directly via write_file
from hermes_tools import write_file
write_file("path.html", html_content)
```

## Depth Consistency Audit

After creating all files, ALWAYS audit depth:
```bash
cd "/mnt/d/学习/Topic/"
for f in *.html; do
  [ "$(basename "$f")" = "index.html" ] && continue
  lines=$(wc -l < "$f"); size=$(wc -c < "$f")
  echo "$f: ${lines}行, $((size/1024))KB"
done
```

**Target**: All modules within 60-100% of the deepest module's size.
**Priority for deepening**: Core technical modules (02-04) > Overview (01) > Summary (05-06).

## File Size Targets

| Module Type | Target Size | Notes |
|-------------|-------------|-------|
| Core technical (02-04) | 14-21KB | Detailed code, ASCII diagrams, formulas |
| Overview (01) | 8-12KB | Concept introduction, taxonomy |
| Summary (05-06) | 6-10KB | Comparison tables, future directions |
| Index | 5-8KB | Navigation, learning roadmap |

## Batch Deepening Workflow

When user requests "详尽，透彻" (thorough):

1. Check all file sizes: `wc -c /path/*.html`
2. Sort by size (ascending)
3. Deepen smallest files first
4. Focus on core technical modules (02-04)
5. Re-audit after each batch
6. Continue until all modules ≥ 8KB (or user says stop)

**Preferred method**: Use `hermes_tools.patch()` to add content to existing HTML files. This is 3-5x faster than regenerating entire files. Insert tip/warn/exercise/deep boxes before or after existing `<h2>` sections. See `references/content-audit-enrichment-workflow.md` for detailed patterns.

**Two-pass workflow** (proven 2026-06): Generate "good enough" first, then audit with element counting (tip/warn/exercise/deep box counts per file), then enrich weakest modules via patch(). This produces better results than trying to generate perfect content on the first pass — especially for 10+ module guides where the agent's quality degrades over long generation sessions.
