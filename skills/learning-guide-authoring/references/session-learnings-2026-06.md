# Session Learnings: Large-Scale Guide Creation (2026-06)

## F-String Curly Brace Conflict (CRITICAL)
When writing HTML in Python execute_code with f-strings, HTML entities like `{r_1}`, `{r_2}` or CSS like `{variable}` are interpreted as Python variables → `NameError`. **Solution**: Never use f-strings for HTML content. Use `write_file` tool directly.

## Parallel Batch Creation Workflow (10+ files)
For large-scale guide creation (136 files in one session), use `delegate_task` with `role: "leaf"` and `toolsets: ["file"]`:
1. Create directory with `terminal("mkdir -p ...")`
2. Pass the full CSS block + nav sidebar HTML in the prompt (every file needs identical CSS/sidebar)
3. Batch 3-5 files per delegate_task call (each file ~120-180 lines)
4. Verify with `find ... -name "*.html" | wc -l` and `du -sh`
5. Update parent index.html files with `patch` to add new section cards

## Index Update Pattern
When adding new subdirectories to existing guide hierarchies, update 3 index files:
1. **Module index** (e.g., `07-应用技术/index.html`): Add a `<a class="card">` in the card-grid
2. **Main index** (e.g., `AI-LLM技术/index.html`): Add a `<div class="dir-card">` section
3. **New module's own index.html**: Create with chapter list and knowledge map SVG
Use `search_files` to find insertion points, then `patch` to insert.

## CSS Template Standardization
All guide files use a consistent compressed single-line CSS (see compressed-css.md). This ensures visual consistency across 900+ files.

## Navigation Sidebar Convention
- Vendor/model guides: 8-12 files per sidebar
- Deep-dive modules: 6-15 files per sidebar
- Mark current page with `class="active"`
- Use consistent link format: `<a href="filename.html">NN Title</a>`

## Scale Reference
- Session created 136 HTML files (1.4MB) across 10 new modules
- Total project: 907 HTML files, 56MB, 168K lines
- Parallel delegation: 3-5 concurrent workers, each creating 3-5 files
- Average file: 120-180 lines, 6-16KB
