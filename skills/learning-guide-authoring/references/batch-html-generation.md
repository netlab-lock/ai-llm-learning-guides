# Batch HTML Generation Patterns

Learned from 2026-05-28 session generating 44 HTML files across 4 learning guide directions.

## Pattern: execute_code with write_file

For generating 10+ HTML files, use `execute_code` with `write_file` calls inside a Python script. This is 5-10x faster than individual `write_file` tool calls.

```python
from hermes_tools import write_file, terminal

OUTPUT_DIR = "/mnt/d/学习/AI-LLM技术/TopicName"
terminal(f"mkdir -p '{OUTPUT_DIR}'")

# Single-line minified CSS to save characters
CSS = """<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#0f1117;color:#c9d1d9;font-family:'Segoe UI',system-ui,sans-serif;line-height:1.8;padding:20px;max-width:1000px;margin:0 auto}h1{color:#58a6ff;font-size:1.8em;margin:20px 0 10px;border-bottom:2px solid #30363d;padding-bottom:10px}h2{color:#79c0ff;font-size:1.4em;margin:25px 0 10px}h3{color:#d2a8ff;font-size:1.2em;margin:20px 0 8px}p{margin:10px 0}.nav{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;margin-bottom:25px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}.nav a{color:#58a6ff;text-decoration:none;font-size:0.9em}pre{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;overflow-x:auto;margin:15px 0;font-size:0.9em}code{background:#161b22;padding:2px 6px;border-radius:4px;font-size:0.9em;color:#e6edf3}pre code{background:none;padding:0}table{border-collapse:collapse;width:100%;margin:15px 0}th,td{border:1px solid #30363d;padding:10px 12px;text-align:left}th{background:#161b22;color:#58a6ff}tr:nth-child(even){background:#161b22}.highlight{background:#1a2332;border-left:4px solid #58a6ff;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}.formula{background:#1a1a2e;border:1px solid #30363d;border-radius:8px;padding:16px;margin:15px 0;text-align:center;font-family:'Courier New',monospace;color:#e6edf3}.ascii-art{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:15px 0;font-family:'Courier New',monospace;font-size:0.85em;line-height:1.4;white-space:pre;overflow-x:auto}ul,ol{margin:10px 0 10px 25px}li{margin:5px 0}.warning{background:#2d1b00;border-left:4px solid #d29922;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}.tip{background:#0d2818;border-left:4px solid #3fb950;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}.footer{margin-top:40px;padding-top:20px;border-top:1px solid #30363d;font-size:0.85em;color:#8b949e}.ref{margin-top:30px;padding:16px;background:#161b22;border-radius:8px;border:1px solid #30363d}.ref h2{margin-top:0}.ref a{color:#58a6ff}</style>"""

def mkp(title, nav_html, body, suffix="GuideName"):
    return f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title} - {suffix}</title>{CSS}</head><body>{nav_html}{body}<div class="footer">{suffix} &copy; 2026</div></body></html>'

def nav(prev, next):
    pp = f'<a href="{prev[1]}">⬅ {prev[0]}</a>' if prev else '<span></span>'
    nn = f'<a href="{next[1]}">{next[0]} ➡</a>' if next else '<span></span>'
    return f'<div class="nav">{pp}<a href="index.html">📖 目录</a>{nn}</div>'

# Generate 2-3 files per execute_code block
write_file(path=f"{OUTPUT_DIR}/01-Topic.html", 
           content=mkp("Title", nav(None, ("Next","02-Next.html")), "<h1>Content</h1>..."))
```

## Enrichment Quality Check

After generating files, check quality and enrich thin files:

```bash
# Find thin files (<6KB)
for f in /path/to/guide/*.html; do
  size_kb=$(du -k "$f" | awk '{print $1}')
  if [ "$size_kb" -lt 6 ]; then
    echo "THIN: $(basename $f) - ${size_kb}KB"
  fi
done

# Count content richness
for f in /path/to/guide/*.html; do
  code=$(grep -c '<pre>' "$f")
  table=$(grep -c '<table>' "$f")
  formula=$(grep -c 'class="formula"' "$f")
  printf "%-40s code:%1s table:%1s formula:%1s\n" "$(basename $f)" "$code" "$table" "$formula"
done
```

**Target:** 4-8 h2 sections, 1-3 tables, 1-2 code blocks, 1-2 ASCII diagrams per file.

## Key Learnings

1. **Don't declare completion too early** — user will push back if files are thin (<4KB)
2. **2-3 files per execute_code block** — sandbox has size limits
3. **Single-line CSS** — saves characters in the sandbox
4. **Helper functions** — `mkp()` and `nav()` reduce boilerplate significantly
5. **Check before declaring done** — run `du -k` and content richness checks
