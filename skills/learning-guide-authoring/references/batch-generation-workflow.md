# Batch Generation Workflow for Multi-Direction Learning Guides

## Prompt-First Workflow

When user asks to create guides for a topic with multiple sub-directions:

1. **Write prompts first** — one detailed prompt per direction, stored in `提示词/<方向名>.md` alongside the guide directory
2. Each prompt specifies: file list (title/topic/content for each), audience, output path, conventions
3. **User reviews** before generation
4. **Generate** — execute prompts to produce HTML
5. **Update gap list** — `学习缺口清单.md` with completion status

## Batch Generation Technique

When generating 10+ HTML files for one direction:

```python
# Pattern: define shared CSS + helpers ONCE, then batch write
from hermes_tools import write_file, terminal

OUTPUT_DIR = "/mnt/d/学习/.../<方向名>"
terminal(f"mkdir -p '{OUTPUT_DIR}'")

CSS = """<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#0f1117;color:#c9d1d9;...}
h1{color:#58a6ff;...}
h2{color:#79c0ff;...}
h3{color:#d2a8ff;...}
.nav{background:#161b22;...}
.highlight{background:#1a2332;...}
.formula{background:#1a1a2e;...}
.ascii-art{background:#161b22;...}
table{border-collapse:collapse;...}
th,td{border:1px solid #30363d;...}
th{background:#161b22;color:#58a6ff}
.warning{background:#2d1b00;...}
.tip{background:#0d2818;...}
.footer{margin-top:40px;...}
.ref{margin-top:30px;...}
</style>"""

def mkpage(title, nav_html, body):
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>{CSS}</head>
<body>{nav_html}{body}
<div class="footer">© 2026</div></body></html>"""

def nav(prev, nxt):
    p = f'<a href="{prev[1]}">⬅ {prev[0]}</a>' if prev else '<span></span>'
    n = f'<a href="{nxt[1]}">{nxt[0]} ➡</a>' if nxt else '<span></span>'
    return f'<div class="nav">{p}<a href="index.html">📖 目录</a>{n}</div>'
```

Then write files in batches of 2-4 per `execute_code` block:
```python
write_file(path=f"{OUTPUT_DIR}/01-xxx.html", content=mkpage("...", nav(...), """...body..."""))
write_file(path=f"{OUTPUT_DIR}/02-xxx.html", content=mkpage("...", nav(...), """...body..."""))
```

## Pitfalls

- **Token budget**: Each execute_code block has a limit. Don't try all 10 files in one block — split into 2-4 blocks.
- **Index first**: Generate `index.html` first with full course table and learning path overview.
- **Navigation consistency**: Each file's nav must link to correct prev/next files.
- **Subagent timeout**: delegate_task times out on mimo — use execute_code + write_file directly instead.

## Progress Tracking

Maintain `学习缺口清单.md` with:
- Checkbox list: `- [ ]` / `- [x]` per direction
- File counts + sizes per direction
- Status table: 方向/优先级/状态/文件数
- Overall framework analysis
