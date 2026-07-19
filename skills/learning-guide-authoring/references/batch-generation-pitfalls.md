# Batch HTML Generation Pitfalls & Patterns

Learned from 2026-05 session generating 40+ HTML files across 4 learning guide directions.

## Pitfalls

### 1. HTML Minification Confusion
`write_file` produces minified HTML (all on one line). This causes:
- `wc -l` reports 1 line (misleading)
- `du -k` shows 4KB minimum (filesystem block size)

**Verification**: Use `wc -c` for byte count, `grep -o '<h2>' | wc -l` for section count.

### 2. Python f-string Curly Brace Escaping (CRITICAL)
When generating HTML via Python f-strings, ANY `{` or `}` in the HTML content must be escaped as `{{` / `}}`. This bites when the HTML contains:
- JSON objects in code examples: `{"key": "value"}` → `{{"key": "value"}}`
- Python dicts in code examples: `{"input": "query"}` → `{{"input": "query"}}`
- JavaScript/CSS code blocks
- LangChain/OpenAI API examples with dict parameters

**Symptom**: `ValueError: Invalid format specifier` at runtime.
**Detection**: After writing the script, `grep -n '{"' /tmp/gen_XX.py` to find unescaped braces.
**Best practice**: Avoid f-strings entirely for HTML generation. Use string concatenation (`+`) for the CSS/NAV template parts, and raw triple-quoted strings for the content body. Only use f-strings for the few variable substitutions (title, nav links).

### 3. Python Triple-Quote with Chinese in Code Blocks
When generating HTML containing `<pre><code>` blocks with Python code that has Chinese characters, Python may misparse `"""` as ending the outer string.

```python
# BROKEN — Chinese period inside triple-quoted Python string
body = '''<pre><code>prompt = """请判断哪个更好。"""</code></pre>'''

# FIXED — Use string concatenation
body = '<pre><code>prompt = "请判断哪个更好。"</code></pre>'
```

### 4. User Workflow: "将提示词写进文档"
When user says this, they mean **save prompts as documents for LATER use** — do NOT immediately execute them. Always:
1. Save prompts to `.md` files first
2. Ask before generating actual content
3. Generate only when explicitly asked

### 5. Subagent Timeout on mimo (RESOLVED 2026-06)
Previously `delegate_task` timed out (600s) on mimo model for file generation tasks. As of 2026-06, **delegate_task with 5 files per batch works reliably** (~5-8min per batch). Use parallel delegate_task as the primary method for 30+ files. Fall back to execute_code + write_file only if delegate_task fails.

## Patterns

### Batch Generation Template
```python
from hermes_tools import write_file, terminal

OUTPUT_DIR = "/mnt/d/学习/AI-LLM技术/专题名"
terminal(f"mkdir -p '{OUTPUT_DIR}'")

CSS = """<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f1117;color:#c9d1d9;...}
/* full CSS here */
</style>"""

def mkp(title, nav_html, body):
    return f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>{title}</title>{CSS}</head><body>{nav_html}{body}</body></html>'

def nav(prev, nxt):
    pp = f'<a href="{prev[1]}">#{prev[0]}</a>' if prev else '<span></span>'
    nn = f'<a href="{nxt[1]}">{nxt[0]}</a>' if nxt else '<span></span>'
    return f'<div class="nav">{pp}<a href="index.html">Index</a>{nn}</div>'

# Write 3-5 files per execute_code call
write_file(path=f"{OUTPUT_DIR}/01-Topic.html", content=mkp("Title", nav(None, ("Next","02-Next.html")), body))
```

### Content Richness Verification
```bash
for f in *.html; do
  h2=$(grep -o '<h2>' "$f" | wc -l)
  table=$(grep -o '<table>' "$f" | wc -l)
  code=$(grep -o '<pre>' "$f" | wc -l)
  bytes=$(wc -c < "$f")
  printf "%s h2:%s table:%s code:%s %sB\n" "$f" "$h2" "$table" "$code" "$bytes"
done
```
Target: 4-8 h2 sections, 1-3 tables, 1+ code blocks per file. Minimum 3KB per file.
User enrichment standard ("丰富"): EVERY file must have code examples (`<pre>`), formulas (`class="formula"`), tables (`<table>`), AND ASCII diagrams (`class="ascii-art"`). Files missing any element will trigger repeated enrichment requests until all 4 elements present.

### Enrichment Strategy
When user asks to "丰富" (enrich) guides:
1. Check file sizes first (`wc -c`)
2. Identify files under target size (target: 4KB+ per file)
3. Enrich thinnest files first
4. Add: formulas, ASCII diagrams, code examples, comparison tables, benchmark data
5. Verify with content richness check after

### Enrichment Completion Signals
**Critical lesson**: When user repeatedly asks "还有哪些值得补充的点" after you declare completion, they are NOT satisfied. Do NOT just repeat "目标已完成" — instead:
1. Actually read the thin files to check if content is substantive
2. Check for missing elements: code blocks (`<pre>`), formulas, tables, ASCII diagrams
3. Add genuinely missing content (new topics, not just padding)
4. Only declare complete after verifying ALL files have all 4 element types

**Anti-pattern**: Declaring "目标已完成" 5+ times while user keeps asking = BAD. The user is signaling that content is still insufficient. Keep enriching until files are genuinely comprehensive.

### Content Element Checklist
Every file should have AT LEAST:
- [ ] `<h2>` sections (4-8 per file)
- [ ] `<table>` comparisons (1-3 per file)
- [ ] `<pre><code>` examples (1+ per file)
- [ ] `class="formula"` or `class="ascii-art"` (1+ per file)

Files missing any element should be flagged for enrichment.
