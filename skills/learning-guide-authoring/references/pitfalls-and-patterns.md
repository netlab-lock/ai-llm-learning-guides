# Pitfalls and Patterns — Learning Guide Authoring

## Pitfall: Subagent Timeout for File-Heavy Tasks

**Problem:** delegate_task with file-writing tasks frequently times out at 600s on mimo-v2.5-pro. The subagent IS working and producing files, but runs out of time before completing all files.

**Symptoms:**
- Subagent completes 3-8 files out of 12 planned
- "Subagent timed out after 600.0s with N API call(s) completed"
- Files that were created are high quality — the issue is speed, not quality

**Reliable workaround:** Use `execute_code` with `write_file` to batch-create files directly. Create 3-5 files per execute_code call. This bypasses the subagent timeout entirely.

```python
from hermes_tools import write_file
CSS = "*{margin:0;padding:0;..."  # shared CSS template

def make_file(base, name, content, css=CSS):
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>{name}</title>
<style>{css}</style></head>
<body>
<div class="nav"><a href="index.html">← 目录</a></div>
{content}
<div class="footer"><p>Guide © 2026</p></div>
</body></html>"""
    write_file(f"{base}/{name}.html", html)

# Batch create: 3-5 files per execute_code call
files = [
    ("01-chapter-name", "<h1>...</h1><p>content</p>"),
    ("02-chapter-name", "<h1>...</h1><p>content</p>"),
    # ...
]
for name, content in files:
    make_file(base, name, content)
```

**When to use:** Creating 5+ HTML files with similar structure (model deep-dive guides, chapter series).

---

## Pitfall: Stay on Task — Don't Get Sidetracked

**Problem:** User has an active goal (e.g., "create guides"). Agent finds tangentially interesting information (e.g., API key for a model) and switches to exploring it instead of continuing the primary task.

**User correction:** "我不是让你写技术指南吗？你这是在干什么" (I asked you to write technical guides, what are you doing?)

**Rule:** When user has an active goal, complete it FIRST. Offer related activities only after the primary task is done or when explicitly asked.

---

## Pattern: Large Project Organization (100+ files)

When user says "整理" (organize) a large project:

1. **Audit:** Count files per directory, identify empty shells (<20 lines), check for missing index.html
2. **Create main index.html:** Link all directories with descriptions, learning paths, stats
3. **Create directory-level index.html:** For each section, link to all subdirectories
4. **Fix empty/thin files:** Rewrite with substantial content
5. **Add cross-references:** "相关章节" boxes linking related sections bidirectionally
6. **Check duplication:** Clarify relationships between overlapping directories

---

## Pattern: Model Deep-Dive Guide Template (11 Chapters)

Standard structure for LLM vendor technical deep-dive guides:

| Chapter | Topic | Content |
|---------|-------|---------|
| 01 | 概述与演进时间线 | Company background, model evolution, model matrix table |
| 02 | 核心架构设计 | MoE/Dense design, parameter scaling, routing strategy |
| 03 | 注意力机制创新 | MLA/CSA+HCA/DSA/Lightning/GQA with ASCII diagrams |
| 04 | 预训练策略与数据工程 | Training data composition, data quality pipeline |
| 05 | 后训练与对齐 | SFT→DPO/GRPO→RL pipeline, thinking mode |
| 06 | 推理能力与长上下文 | Context length, thinking budget, compression |
| 07 | 多模态/Agent能力 | Multimodal architecture OR Agent capabilities |
| 08 | 系统工程与部署优化 | GPU requirements, API pricing, frameworks |
| 09 | 性能评估与基准测试 | Benchmark results, comparison tables |
| 10 | 应用场景与生态系统 | Products, API platform, enterprise solutions |
| 11 | 论文精读与学习资源 | Papers, GitHub repos, learning path |
| index | Navigation | Chapter list, links to related guides |

Each chapter: 150-250 lines, ASCII diagrams, comparison tables, dark theme CSS.

---

## CSS Template (Standard Dark Theme)

```css
*{margin:0;padding:0;box-sizing:border-box}body{background:#0f1117;color:#c9d1d9;font-family:'Segoe UI',system-ui,sans-serif;line-height:1.8;padding:20px;max-width:1000px;margin:0 auto}h1{color:#58a6ff;font-size:1.8em;margin:20px 0 10px;border-bottom:2px solid #30363d;padding-bottom:10px}h2{color:#79c0ff;font-size:1.4em;margin:25px 0 10px}h3{color:#d2a8ff;font-size:1.2em;margin:20px 0 8px}p{margin:10px 0}.nav{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:12px 16px;margin-bottom:25px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}.nav a{color:#58a6ff;text-decoration:none;font-size:0.9em}pre{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;overflow-x:auto;margin:15px 0;font-size:0.9em}table{border-collapse:collapse;width:100%;margin:15px 0}th,td{border:1px solid #30363d;padding:10px 12px;text-align:left}th{background:#161b22;color:#58a6ff}tr:nth-child(even){background:#161b22}.highlight{background:#1a2332;border-left:4px solid #58a6ff;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}.ascii-art{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:15px 0;font-family:'Courier New',monospace;font-size:0.85em;line-height:1.4;white-space:pre;overflow-x:auto}ul,ol{margin:10px 0 10px 25px}li{margin:5px 0}.warning{background:#2d1b00;border-left:4px solid #d29922;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}.tip{background:#0d2818;border-left:4px solid #3fb950;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}.footer{margin-top:40px;padding-top:20px;border-top:1px solid #30363d;font-size:0.85em;color:#8b949e}
```
