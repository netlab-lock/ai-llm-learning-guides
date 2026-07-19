# Session Pitfalls — 2026-05-28

## Interpretation Pitfalls

1. **"将X写进文档" ≠ "执行X"**: When user says "将提示词写进文档", they mean **save to a file for later use**, not execute the prompts to generate content. Always confirm before executing a large batch of work.

2. **"整理目录/内容" ≠ "总结"**: When user says "整理学习内容" or "整理目录", they mean **reorganize files, fix broken links, update parent indexes, create missing index.html files** — not provide a summary of what exists. Checklist for "整理":
   - Scan for directories missing `index.html`
   - Verify all `href` links in parent `index.html` point to existing files
   - Update gap lists and progress trackers
   - Fix broken paths

3. **Don't declare completion prematurely**: If the user keeps pushing after you say "done", re-examine whether you actually missed something. Check file sizes — HTML files under 4KB are likely thin and need enrichment.

## Technical Pitfalls

4. **execute_code triple-quote breakage**: When embedding Python code examples inside HTML strings within Python triple-quoted strings, inner `"""` will break the outer string. Use single-line string concatenation (`+=`) instead of triple-quotes for HTML content that contains `<pre><code>` blocks.

5. **Knowledge base organization workflow**:
   ```
   1. Find directories missing index.html
   2. Check parent index.html for broken href links
   3. Verify file sizes (flag <4KB as thin)
   4. Update gap list document
   5. Update parent index.html with new cards
   ```

6. **Batch HTML enrichment pattern**:
   - Use `execute_code` with `write_file` calls for each file
   - Build HTML content with string concatenation (`+=`) not triple-quotes
   - CSS template as a Python variable, reused across all files
   - `mkp()` wrapper function for consistent page structure
   - `nav()` function for prev/next navigation
