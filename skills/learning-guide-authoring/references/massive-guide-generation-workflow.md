# Massive Guide Generation Workflow (20+ files)

When generating 10-30+ HTML guides in one session, use this workflow:

## Batch Script Pattern
Write Python scripts to `/tmp/gen_XX.py` generating 2-3 files each, run via `python3 /tmp/gen_XX.py`.

```python
#!/usr/bin/env python3
import os
BASE = "/mnt/d/学习/<topic>"
CSS = """*{margin:0;...}"""  # Extract from existing file

def hp(title, prev, nxt, nav, body):
    pv = f'<a href="{prev}">&larr; ...</a>' if prev else '<span></span>'
    nx = f'<a href="{nxt}">... &rarr;</a>' if nxt else '<span></span>'
    return f'<!DOCTYPE html>\n<html>...{body}...</html>'

def w(p, c):
    with open(os.path.join(BASE, p), "w", encoding="utf-8") as f: f.write(c)
    print(f"  {p} ({os.path.getsize(os.path.join(BASE, p)):,}B)")

w("01-file.html", hp("Title", None, "02.html", "Nav", r"""...content..."""))
```

## Rules
- **2-3 files per script** — not 1 (too slow), not 10+ (too large to debug)
- **Never use f-strings for HTML** — CSS/JS curly braces cause NameError
- **Use r"""...""" raw strings** for HTML content
- **delegate_task consistently times out** on mimo for HTML generation (600s). Use terminal directly.
- **Chinese quotes in Python**: "配方" inside double-quoted strings causes SyntaxError. Fix with `sed -i 's/中文"引号"/中文引号/' script.py`

## Depth Consistency Audit
After all files created, check sizes:
```bash
for f in *.html; do [ "$(basename "$f")" = "index.html" ] && continue; sz=$(wc -c < "$f"); echo "$((sz/1024))KB $f"; done | sort -n
```
Target depth ratio: <160% (thickest/thinnest). If >180%, enrich thinnest files.

## Enrichment Pattern
For thin files, write a new script that rewrites them with:
- More ASCII architecture diagrams
- Latest 2024-2025 research findings
- Detailed math formulas
- Comparison tables
- Code examples
Target: each file 12-20KB.
