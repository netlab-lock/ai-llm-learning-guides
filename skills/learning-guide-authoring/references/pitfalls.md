# Pitfalls for Learning Guide Authoring

## Large File Handling (>75KB)

When working with large HTML guides (>75KB), be aware:
- `read_file` in `execute_code` truncates content at ~75KB
- Footer markers and insertion points may not be found in truncated content
- **Workaround**: Use `terminal` with a Python script to read/modify large files
- Example:
  ```python
  # Write script to /tmp/modify.py
  with open('large_file.html', 'r', encoding='utf-8') as f:
      content = f.read()
  # ... modify content ...
  with open('large_file.html', 'w', encoding='utf-8') as f:
      f.write(new_content)
  ```
- Then run via `terminal("python3 /tmp/modify.py")`

## Subagent Timeout for Large Tasks

- `delegate_task` subagents timeout at 600s
- For large HTML generation tasks, use direct `write_file` + `terminal` instead
- Break large tasks into: (1) write script, (2) execute script, (3) verify output

## DuckDuckGo Search Unreliability

- `ddgs` CLI may return empty results or timeout for Chinese queries
- Fallback: Try English queries, or use `web_extract` on known URLs
- Multiple retry attempts with different query phrasings may be needed
