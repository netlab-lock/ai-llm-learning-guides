# Large HTML File Merging Pattern

## Problem
When building large HTML guides (100KB+), content is often created in fragments by subagents or multiple rounds. These fragments need to be merged into the main file.

## Solution: Python Merge Script

Use a Python script to find a marker in the HTML file and insert content before it:

```python
#!/usr/bin/env python3
# Read main file
with open('main.html', 'r', encoding='utf-8') as f:
    main = f.read()

# Read fragment
with open('fragment.html', 'r', encoding='utf-8') as f:
    fragment = f.read()

# Find insertion point (usually footer)
marker = '<footer style='
idx = main.find(marker)

if idx > 0:
    new = main[:idx] + fragment + '\n\n' + main[idx:]
    with open('main.html', 'w', encoding='utf-8') as f:
        f.write(new)
    print(f'Updated: {len(new)} chars ({len(new)//1024}KB)')
```

## Key Points

1. **Always write the script to a file first** (`/tmp/merge.py`), then run it with `terminal("python3 /tmp/merge.py")`
2. **Find a unique marker** in the HTML (footer, closing tags, etc.) to use as insertion point
3. **Use UTF-8 encoding** explicitly for Chinese content
4. **Verify after merge** with `wc -l -c` to check line count and file size
5. **Update the index.html** to reflect new file size and content

## When to Use

- Guide exceeds 100KB and needs iterative expansion
- Subagents create content fragments that need merging
- Multiple rounds of content addition to an existing guide
