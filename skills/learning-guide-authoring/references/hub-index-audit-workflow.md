# Hub Index Page Audit & Regeneration

When the user asks to "fix", "update", "audit", or "整理目录" for a central hub/landing page (like D:\学习\index.html), follow this systematic workflow.

## Diagnosis Phase

1. **Check for truncation** — `tail -20` the file. If it ends mid-HTML-tag or mid-card, it was truncated during a previous write_file call.
2. **Enumerate actual directories** — `find <root> -maxdepth N -mindepth M -type d | sort` to discover all real guide folders.
3. **Cross-reference index vs disk** — Compare every `href="..."` in the index against actual `index.html` files on disk.
4. **Count HTML files per section** — `find <section> -name "*.html" | wc -l` for accurate stats.
5. **Identify missing sections** — New top-level categories (e.g., 08-评测体系, 09-厂商与前沿) added after the index was last written will be completely absent.

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| File ends mid-card at ~500 lines | write_file truncated output | Full regeneration |
| Stats show "300+ HTML" but actual is 700+ | Stats hardcoded, never updated | Recount and update |
| Entire category section missing | Guide added after index was built | Add section + cards |
| Cards link to nonexistent paths | Directory was renamed/moved | Verify hrefs against disk |
| "NEW" badge on stale items | Badge never removed | Remove or add date logic |

## Regeneration Steps

```
# 1. Get total HTML count
find <root> -name "*.html" | wc -l

# 2. Get count per top-level section
for d in <root>/<category>*/; do echo "$(basename "$d"): $(find "$d" -name '*.html' | wc -l)"; done

# 3. List all guide index.html files (depth 2-3)
find <root> -maxdepth 3 -mindepth 2 -name "index.html" -type f | sort

# 4. Count distinct guide projects (index.html at depth 2)
find <root> -maxdepth 2 -mindepth 2 -name "index.html" -type f | wc -l
```

## Stats Calculation

- **文档项目**: Count of top-level `index.html` files across all categories
- **HTML 页面**: Total `.html` file count (use `find ... | wc -l`)
- **学科方向**: Count of top-level category directories (01-基础理论, 02-模型架构, etc.)
- **section-count per card**: Count of `.html` files in that specific guide folder

## Pitfalls

- **Don't use write_file for files > ~400 lines in one shot.** The hub index for D:\学习\ grew to 500+ lines and got truncated. For very large hub pages, either generate in sections or use terminal with heredoc/echo.
- **Always verify the written file.** `tail -5` after writing to confirm it ends with `</html>`.
- **Relative paths from hub**: Cards use paths relative to the hub location (e.g., `AI-LLM技术/08-评测体系/LLM评测体系/index.html`), not absolute.
- **The template in references/grouped-landing-page-template.html has hardcoded stats** — always override them with actual counts.
