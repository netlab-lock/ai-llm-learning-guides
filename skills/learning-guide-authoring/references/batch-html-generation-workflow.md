# Batch HTML Generation Workflow

When generating 10+ HTML files for a learning guide, use the following proven workflow.

## Pattern: Python Script → Terminal Execution

1. **Write script to `/tmp/gen_XX.py`** using `write_file` tool
2. **Execute via `terminal`**: `python3 /tmp/gen_XX.py`
3. **Verify output**: check file sizes printed by the script

## Script Template

```python
#!/usr/bin/env python3
import os
BASE = "/mnt/d/学习/<topic>"
CSS = open(os.path.join(BASE, "index.html"), encoding="utf-8").read().split("<style>")[1].split("</style>")[0]

def hp(title, prev, nxt, nav, body):
    pv = f'<a href="{prev}">&larr; {os.path.basename(prev).replace(".html","")}</a>' if prev else '<span></span>'
    nx = f'<a href="{nxt}">{os.path.basename(nxt).replace(".html","")} &rarr;</a>' if nxt else '<span></span>'
    return f'<!DOCTYPE html>\n<html lang="zh-CN">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{title}</title>\n<style>{CSS}</style>\n</head>\n<body>\n<div class="nav">{pv}<span>{nav}</span>{nx}</div>\n<div class="container">\n{body}\n</div>\n<div class="footer"><p>Guide · {title}</p><p><a href="index.html">返回目录</a></p></div>\n</body>\n</html>'

def w(p, c):
    with open(os.path.join(BASE, p), "w", encoding="utf-8") as f: f.write(c)
    print(f"  {p} ({os.path.getsize(os.path.join(BASE, p)):,}B)")

# Generate files here - 2-3 per script
w("01-Topic.html", hp("01 Title", None, "02-Topic.html", "Nav", """...content..."""))
w("02-Topic.html", hp("02 Title", "01-Topic.html", "03-Topic.html", "Nav", """...content..."""))
print("Done!")
```

## Batch Size Limits

- **2-3 files per script**: reliable, ~15-20s execution
- **4-5 files per script**: usually works but risky (may timeout or truncate)
- **6+ files per script**: unreliable, avoid

For a 25-file guide: ~10 scripts (2-3 files each), run sequentially.

## CSS Extraction

Always extract CSS from an existing file in the same guide for consistency:
```python
CSS = open("path/to/existing.html", encoding="utf-8").read().split("<style>")[1].split("</style>")[0]
```

## Alternative: execute_code + write_file Pattern

When CSS is a simple inline string (not extracted from existing files), `execute_code` + `write_file` works well and avoids the `/tmp` file roundtrip:

```python
from hermes_tools import write_file, terminal

OUTPUT_DIR = "/mnt/d/学习/Topic"
terminal(f"mkdir -p '{OUTPUT_DIR}'")

CSS = """<style>...inline CSS string...</style>"""

def mkp(title, nav_html, body):
    return f'<!DOCTYPE html>...{CSS}...{nav_html}...{body}...'

write_file(path=f"{OUTPUT_DIR}/01-File.html", content=mkp("Title", nav(...), """...body..."""))
```

**Advantages**: no /tmp scripts, direct verification, hermes_tools available.
**Limitations**: 
- CSS must be a simple string variable (not read from file) — f-strings with CSS curly braces work fine if CSS is already a string
- Body content with `"""` triple-quotes causes SyntaxError in for-loops — use individual write_file calls or escape
- 7-10 files per execute_code call is reliable; 12+ may hit token limits

## Pattern: Parallel delegate_task (RECOMMENDED for 30+ files)

For large-scale generation (30-100+ files), **parallel delegate_task** is significantly faster than sequential Python scripts. Validated in 2026-06 session creating 110 HTML files across 6 directories.

### How It Works
1. Create the output directory with `terminal("mkdir -p ...")`
2. Call `delegate_task` with `role: "leaf"` and `toolsets: ["file"]`
3. Each worker creates 5 files (content + optionally index.html)
4. Workers run in parallel — 3 batches of 5 = 15 files concurrently

### Template for delegate_task Calls
```
delegate_task(
  role="leaf",
  toolsets=["file"],
  goal="""
Create 5 HTML files for <output_dir>. All content in Chinese.
Self-contained HTML with dark theme, nav sidebar, callout boxes, tables, exercises.

Nav sidebar (include in ALL files, mark current as active):
<a href="01-File.html">01 Title</a>
<a href="02-File.html">02 Title</a>
...

CSS (include in ALL files):
<style>compressed single-line CSS here</style>

FILE 1: 01-File.html — <content description>
FILE 2: 02-File.html — <content description>
...

Use write_file tool for each file.
"""
)
```

### Key Requirements for Parallel Workers
- **Pass FULL compressed CSS** in the instructions (each worker is independent)
- **Pass FULL nav sidebar** with all links (worker marks current as active)
- **5 files per worker** is the sweet spot (reliable, ~5-8min per batch)
- **Describe content in detail** — workers have no shared state
- Workers create files directly with `write_file` — no /tmp scripts needed

### Speed Comparison
| Method | Files | Time | Notes |
|--------|-------|------|-------|
| Sequential Python scripts | 15 | ~15min | One script at a time |
| execute_code + write_file | 15 | ~10min | 3-5 files per call |
| **Parallel delegate_task** | **15** | **~5min** | **3 batches of 5 in parallel** |
| Parallel delegate_task | 100 | ~30min | 20 batches of 5 |

### Index File Updates
After creating new content directories, update parent index.html files:
1. Find the card-grid section in the parent index
2. Use `patch` to insert a new card entry before the closing `</div>`
3. Card format: `<a href="DirName/index.html" class="card">...</a>`
4. Update all parent indexes in the chain (subdirectory → main directory → root)

## Pitfalls

1. **NEVER use f-strings for HTML content** — CSS/JS curly braces cause `NameError`. Experienced firsthand: `{r_1}` in HTML math content was interpreted as Python variable. Use write_file directly or string concatenation.
2. **Write script to file, don't use execute_code** — execute_code sandbox has separate Python env
3. **print file sizes after each write** — enables quick depth audit
4. **Each script should be self-contained** — don't depend on variables from previous scripts
5. **Triple-quote nesting in for-loops** — When using execute_code with a for-loop that writes multiple files, body content containing `"""` (e.g. HTML `<pre><code>` with Python examples) causes SyntaxError. Fix: use individual write_file calls outside loops, or replace `"""` in body content with escaped quotes
6. **RLHF/alignment guides with formulas** — Content with many LaTeX-like formulas and ASCII art is prone to truncation in execute_code. Prefer 3-4 files per execute_code call for formula-heavy content
7. **delegate_task timeout on mimo** — Previously documented as 600s timeout. As of 2026-06, delegate_task with 5 files per batch works reliably on mimo (~5-8min per batch). If timeout occurs, reduce to 3 files per batch.

## Two-Pass Workflow

1. **Generate**: Write all files at target size (8-15KB)
2. **Audit**: `for f in *.html; do echo "$(wc -c < $f) $f"; done | sort -n`
3. **Deepen**: Write a separate script to overwrite only the thinnest files
4. **Re-audit**: Verify consistency
