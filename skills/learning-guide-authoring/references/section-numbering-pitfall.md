# Pitfall: Section Numbering Breaks After Patching

**Discovered**: 2026-06-24 during optimization guide modular restructuring

## The Problem

When using `patch()` to insert new sections into an existing HTML file, the section numbering of subsequent sections becomes inconsistent.

Example:
- Original: §1, §2, §3 (with §3.1, §3.2, §3.3)
- Insert new §3 → old §3 still has §3.1, §3.2, §3.3 (should be §4.1, §4.2, §4.3)
- Result: two sets of §3.x subsections

## The Fix

After any patch that inserts a new `<h2>` section:
1. Read all `<h2>` and `<h3>` headings with `grep '<h[23]' file.html`
2. Check if numbering is sequential (no duplicates, no gaps)
3. Patch any wrong numbers immediately

## Prevention

When designing the generation script (`gen_topic.py`), use a section counter variable rather than hardcoded numbers. If sections are generated as functions, number them dynamically.

## Example Patch Sequence

```python
# Insert new section 3 before old section 3
patch(file, "<h2>3. OldSection</h2>", "<h2>3. NewSection</h2>...<h2>4. OldSection</h2>")
# Then fix subsection numbers:
patch(file, "<h3>3.1 OldSub</h3>", "<h3>4.1 OldSub</h3>")
patch(file, "<h3>3.2 OldSub</h3>", "<h3>4.2 OldSub</h3>")
```
