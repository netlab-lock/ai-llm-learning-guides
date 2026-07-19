# Large HTML Guide Creation Workflow

## Pattern: Creating 200KB+ Multi-Section HTML Guides

When creating comprehensive HTML learning guides (200KB+), use this workflow:

### 1. Parallel Content Generation
- Use `delegate_task` with multiple subagents to create content in parallel
- Each subagent writes to a separate temp file (e.g., `/tmp/part1.html`, `/tmp/part2.html`)
- Subagents should NOT include `<!DOCTYPE html>`, `<head>`, `<style>`, or opening `<body>` tags in fragment files

### 2. Merge Strategy
```python
# Pattern for inserting content before footer
with open('main.html', 'r') as f:
    main = f.read()
with open('fragment.html', 'r') as f:
    fragment = f.read()

marker = '<footer style='
idx = main.find(marker)
if idx > 0:
    new = main[:idx] + fragment + '\n\n' + main[idx:]
    with open('main.html', 'w') as f:
        f.write(new)
```

### 3. Small Edits Use Patch
- For targeted changes (updating a tag, fixing a number), use `patch` tool
- For inserting new sections, use the Python merge pattern above

### 4. Verification After Each Merge
```bash
wc -l -c file.html  # Check size
grep -c '<h2' file.html  # Count sections
grep -c '<table' file.html  # Count tables
grep -c 'ascii-diagram' file.html  # Count diagrams
```

## User Preference: Maximum Depth First

**CRITICAL**: This user wants the FIRST output to be at maximum depth. Do NOT leave content for "the next round." The user will keep asking "再详尽一点" if the initial output is thin.

- Include architecture diagrams (ASCII) for every major concept
- Include comparison tables with exact numbers
- Include API pricing where available
- Include limitations and known issues
- Include practical examples (code snippets)
- Target: 100KB+ for a comprehensive guide on a major topic

## HTML Content Insertion Pattern

When the user asks to "补充" (supplement) content into an existing HTML file:

1. Read the existing file to understand structure
2. Create new content as HTML fragment (no `<html>/<head>/<body>` tags)
3. Find the footer marker: `<footer style=`
4. Insert new content before the footer
5. Verify the result (line count, section count, table count)

## Audit Workflow

When the user says "整理一下" (organize):

1. **Count files and sizes** across all directories
2. **Identify empty shells** (files with <20 lines or <2KB)
3. **Check for missing index.html** files
4. **Check for content overlaps** between sections
5. **Produce a prioritized fix list** (P0/P1/P2/P3)
6. **Start fixing** from highest priority

## CSS Template for Dark Theme

```css
:root{--bg:#0d1117;--surface:#161b22;--border:#30363d;--text:#c9d1d9;--accent:#58a6ff;--green:#3fb950;--orange:#d29922;--red:#f85149;--purple:#bc8cff}
```

Standard card classes: `card`, `card-accent`, `card-green`, `card-orange`, `card-purple`, `card-pink`, `card-cyan`
