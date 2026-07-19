# Batch HTML Generation Pitfalls & Patterns (2026-05-27)

## Pitfall: Triple-Quote Syntax Errors

When generating multiple HTML files in one `execute_code` script, Python's parser fails with:

```
SyntaxError: closing parenthesis ')' does not match opening parenthesis '['
```

This happens when two long triple-quoted strings (100+ lines each) are placed consecutively in a list or function call.

**Fix**: 
- Use string concatenation (`+=`) for building HTML body strings
- Split into separate `execute_code` calls (2-3 files per call)
- Never put two 100+ line triple-quoted HTML strings in the same Python block

## Pitfall: "写进文档" vs "生成指南"

When user says "将提示词写进文档", they mean **save prompts as reference documents for later use**, NOT "execute the prompts to generate full guides immediately".

Multi-direction guide generation (10+ files × N directions = 40+ files) is a multi-hour commitment. Always confirm:
- (a) save prompts for later, or  
- (b) execute prompts to generate content now

## Proven Batch Pattern

```python
from hermes_tools import write_file

OUTPUT_DIR = "/mnt/d/学习/AI-LLM技术/TopicName"
CSS = """<style>...</style>"""  # Define once

def mkp(t, nav, body):
    return f'<!DOCTYPE html>...{CSS}...{nav}{body}...'

def nav(p, n):
    pp = f'<a href="{p[1]}">⬅ {p[0]}</a>' if p else '<span></span>'
    nn = f'<a href="{n[1]}">{n[0]} ➡</a>' if n else '<span></span>'
    return f'<div class="nav">{pp}<a href="index.html">📖 目录</a>{nn}</div>'

# Build body with concatenation (not triple-quote blocks)
body = '<h1>Title</h1>'
body += '<h2>Section</h2>'
body += '<p>Content...</p>'

# Write 2-3 files per execute_code call
write_file(path=f"{OUTPUT_DIR}/01-Topic.html", 
           content=mkp("Title", nav(None, ("Next","02-Next.html")), body))
```

## Pitfall: F-String Curly Brace Escaping in HTML Code Blocks

When generating HTML via Python f-strings, any `{` or `}` inside `<pre><code>` blocks (JSON examples, Python dict literals, format strings) gets interpreted as f-string format specifiers, causing:

```
ValueError: Invalid format specifier '"user", "content": query' for object of type 'str'
```

This is especially common with code examples like:
```python
# These break inside f-strings:
messages=[{"role": "user", "content": query}]
result = executor.invoke({"input": "question"})
```

**Fix options (in order of preference):**

1. **Avoid f-strings entirely** — use string concatenation:
   ```python
   content = '''<!DOCTYPE html>...<style>''' + CSS + '''</style>...
   <pre><code>messages=[{"role": "user", "content": query}]</code></pre>
   ...'''
   ```
   This is the most reliable approach. Build CSS as a separate variable, concatenate it in.

2. **Double-brace escaping** (fragile, easy to miss):
   ```python
   f'''<pre><code>messages=[{{"role": "user", "content": query}}]</code></pre>'''
   ```
   Must escape EVERY `{` and `}` in code blocks. Miss one = runtime error.

3. **Per-module Python scripts** — write each module as a separate `/tmp/gen_XX.py` using concatenation, run via `terminal("python3 /tmp/gen_XX.py")`. This isolates failures and makes debugging faster.

**Recommended pattern for multi-module guides:**
```python
# gen_module_XX.py — one script per module
CSS = """:root{--bg:#0d1117;..."""  # CSS as raw string (no f-string needed)

content = '''<!DOCTYPE html>
<html><head><style>''' + CSS + '''</style></head>
<body>
<pre><code>  # Curly braces work fine here — no f-string!
dict = {"key": "value"}
</code></pre>
</body></html>'''

with open(out_path, "w", encoding="utf-8") as f:
    f.write(content)
```

## File Size Targets

- Aim for 8-16 KB per file
- If content exceeds 20 KB, split into multiple files
- After enrichment, verify all files ≥ 4KB with `terminal("du -h ...")`

## Pitfall: Duplicate Sections When Patching

When using `patch()` to insert content before `<h2>小结</h2>` (or any section header), multiple patches targeting the same anchor can create **duplicate sections**. This is especially common with summary sections.

**Detection**:
```bash
for f in *.html; do
  count=$(grep -c '<h2>小结</h2>' "$f")
  [ "$count" -gt 1 ] && echo "DUPLICATE: $f has $count summary sections"
done
```

**Fix**: Read the file, find the second occurrence, and remove it while keeping the first (which contains the actual summary table):
```python
with open(path, "r") as f:
    content = f.read()
first = content.find('<h2>小结</h2>')
second = content.find('<h2>小结</h2>', first + 1)
if second > 0:
    next_section = content.find('<div class="next-prev">', second)
    content = content[:second] + content[next_section:]
    with open(path, "w") as f:
        f.write(content)
```

## Pitfall: Grep Regex Patterns for Topic Coverage Audits

When auditing topic coverage with grep, patterns like `Chain.of.Thought` treat `.` as a regex wildcard matching ANY character. This causes false positives (e.g., `Chain-of-Thought` matches, but so does `ChainXofYThought`).

**Fix**: Escape dots with `\.` for literal matching, or use simpler keywords:
```bash
# Bad — . is wildcard
grep -c "Chain.of.Thought" file.html

# Good — escaped dots
grep -c "Chain\.of\.Thought" file.html

# Better — use simpler unique keywords
grep -c "CoT\|Chain-of-Thought" file.html
```

**Also**: Always do a SECOND verification pass with broader/simpler patterns before concluding a topic is missing. Initial strict patterns often produce false negatives:
```bash
# First pass (strict, may miss)
grep -ci "Self.Refine" 03*.html  # 0 results

# Second pass (broader)
grep -ci "Self-Refine\|自精炼\|自改进" 03*.html  # 1 result — was covered!
```

## Pitfall: execute_code Tool Call Limit

The `execute_code` sandbox has a limit of ~50 tool calls per execution block. When auditing many files with many patterns, you can hit this limit mid-execution.

**Fix**: Split audit scripts into smaller batches, or use `terminal()` for grep-heavy audits instead of `execute_code()`.

## Post-Generation Enrichment Pattern (2026-06)

After generating all modules, run element-count audit:
```bash
for f in *.html; do
  chars=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  tips=$(grep -c 'class="tip"' "$f")
  warns=$(grep -c 'class="warn"' "$f")
  exs=$(grep -c 'class="exercise"' "$f")
  deeps=$(grep -c 'class="deep"' "$f")
  printf "%-35s %5d字 tip:%d warn:%d ex:%d deep:%d\n" "$f" "$chars" "$tips" "$warns" "$exs" "$deeps"
done
```

Minimum per module: 1 tip, 1 warn, 1 exercise, 1 deep box. Enrich 0-count modules via `hermes_tools.patch()`. See `references/content-audit-enrichment-workflow.md` for full workflow.
