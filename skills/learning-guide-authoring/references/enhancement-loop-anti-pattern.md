# Enhancement Loop Anti-Pattern (Learned 2026-05-27)

## Problem

When enhancing thin files after initial batch generation, the agent can get stuck in a degenerate loop: rewriting the same file repeatedly with the same template content, producing the same size each time. In one session, 15+ tool calls were wasted rewriting the same file to 5KB each time.

## Root Cause

Using `execute_code` to rewrite files with the same `hp()` template function produces the same output size. The template's body content determines the file size — wrapping it differently doesn't add content. The `write_file` tool also deduplicates identical content.

## Symptoms

- Same file rewritten 3+ times with identical size output
- Agent keeps saying "继续增强" without actual size growth
- Tool calls accumulate without progress
- Files stay at 5-8KB despite "enhancement"

## Fix

After 2-3 unsuccessful rewrites of the same file:

1. **STOP rewriting** — accept the current size
2. **Move on** to the next file
3. If size growth is truly needed, **add NEW content sections** (new h2/h3 blocks with ASCII diagrams, formulas, tables, exercises) rather than reformatting existing content

## Acceptable Sizes

- **Bulk-generated guides** (20+ files): 7-10KB per file with substantive content is acceptable
- **Individually-crafted deep dives**: 15-20KB per file is the target
- Don't waste tool calls forcing a 7KB file to 12KB when the content is already complete

## Prevention

- After initial batch generation, do ONE enhancement pass per file
- If a file doesn't grow after one rewrite, skip it
- Track progress with `execute_code` audit — if the count of thin files doesn't decrease, STOP
- The user will NOT send "继续完善" if the content is genuinely good, even if it's 8KB
