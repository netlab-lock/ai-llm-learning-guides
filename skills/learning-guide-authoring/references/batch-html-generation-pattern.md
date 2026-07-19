# Batch HTML Generation Patterns (P3 Session Learnings)

## Problem: write_file Duplication Detection

When using `write_file` repeatedly on the same path, the tool may report success but the file content doesn't actually change. This happened in the P3 session where 28 files stayed at 5-9KB across 20+ write_file calls — the tool was deduplicating or caching.

**Root cause**: write_file with identical or very similar content blocks gets optimized away. The file appears to be "written" (no error) but the on-disk content is unchanged.

**Verification**: Always check `wc -c` AFTER writing, not just the tool's return status.

## Recommended Approach: Python Script via Terminal

For batch creation (5+ files), the most reliable approach is:

1. Write a Python script to `/tmp/gen_<topic>.py` using `write_file`
2. Execute via `terminal("python3 /tmp/gen_<topic>.py")`
3. Verify sizes with `wc -c`

### CSS Extraction for Consistency

When generating multiple files, extract CSS from an existing file to ensure visual consistency:

```python
CSS = open(os.path.join(BASE, "01-ExistingFile.html"), encoding="utf-8").read().split("<style>")[1].split("</style>")[0]
```

This avoids manually copying CSS and ensures all files in a guide look identical.

### Template Pattern

```python
#!/usr/bin/env python3
import os
BASE = "/mnt/d/学习/AI-LLM技术/<TopicDir>"
os.makedirs(BASE, exist_ok=True)

# Extract CSS from existing file in the guide
CSS = "<style>...</style>"  # Copy from a known-good file

def hp(title, prev, nxt, nav_title, body):
    pv = '<a href="{}">&larr; {}</a>'.format(prev, prev.replace('.html','')) if prev else '<span></span>'
    nx = '<a href="{}">{} &rarr;</a>'.format(nxt, nxt.replace('.html','')) if nxt else '<span></span>'
    return '<!DOCTYPE html>\n<html lang="zh-CN">\n<head><meta charset="UTF-8">\n<meta name="viewport" content="width=device-width,initial-scale=1.0">\n<title>{}</title>\n{}\n</head>\n<body>\n<div class="nav">{}<span>{}</span>{}</div>\n<div class="container">\n{}\n</div>\n<div class="footer"><p><a href="index.html">返回总览</a></p></div>\n</body>\n</html>'.format(title, CSS, pv, nav_title, nx, body)

def w(name, content):
    path = os.path.join(BASE, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("  {}: {}KB".format(name, os.path.getsize(path)//1024))

# Generate files
w("index.html", "...")
w("01-Topic.html", hp("01 Title", None, "02-Next.html", "模块 01", """...body..."""))
# ... more files
```

### Key Rules
- **No f-strings** in HTML content — CSS/JS curly braces cause NameError
- **Use triple quotes** for HTML body content (rarely conflicts with HTML attributes)
- **Use `.format()`** for template variables
- **Print file sizes** after each write to verify
- **One script per topic** (7 files) — don't try to generate all 42 files in one script

## Depth Achievement Strategy

Target: 14-21KB per module file.

**What makes a module reach 14KB+**:
- 3-4 ASCII architecture diagrams (each ~500 bytes)
- 2-3 code blocks with comments (each ~1-2KB)
- 2-3 comparison tables (each ~500 bytes)
- Detailed explanations with sub-sections (h3, h4)
- Deep-dive boxes (.deep class)
- Exercise sections
- Formula blocks

**What keeps modules at 5-7KB** (insufficient):
- Only 1-2 ASCII diagrams
- Short code snippets without comments
- Brief explanations without sub-sections
- Missing exercises and deep-dive boxes

## File Size Audit Pattern

After creating all files, always audit:
```bash
for f in *.html; do
  sz=$(wc -c < "$f"); kb=$((sz/1024))
  echo "$f: ${kb}KB"
done
```

Target: all modules within 60-100% of the deepest module's size.

## Enhancement Ceiling

After batch generation with the Python script template, files typically land at 7-14KB. Attempting to "enhance" them by rewriting with the same template produces the same size — the body content is the ceiling. To grow files:

1. **Add new sections** (new h2/h3 blocks) with additional ASCII diagrams, formulas, tables
2. **Expand existing sections** with deeper explanations, more code examples
3. **Add exercises** at the end of each file
4. **Do ONE pass per file** — if it doesn't grow, move on

See `references/enhancement-loop-anti-pattern.md` for the full anti-pattern description.
