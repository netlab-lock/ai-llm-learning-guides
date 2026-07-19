# Modular HTML Structure for Learning Guides

## User Preference (Strong)

When a guide covers a broad domain (e.g., "optimization methods"), **split into multiple self-contained HTML files** in a subdirectory, NOT one giant file.

User explicitly said: "我们的内容结构要高内聚，低耦合。分块建html" (High cohesion, low coupling. Build HTML in blocks.)

## Principles

- **High cohesion:** Each file covers ONE topic/technique family. Can be read independently.
- **Low coupling:** Files don't duplicate content. Cross-reference via `<a href>` links.
- **Index page:** `00-index.html` as hub with navigation, overview, learning path, and classification tree.
- **Naming:** `01-Topic-Name.html`, `02-Topic-Name.html`. Numbered, kebab-case.

## Directory Structure

```
D:\学习\AI-LLM技术\<TopicName>\
├── 00-index.html          # Hub: nav + overview + learning path + classification
├── 01-Subtopic-A.html     # Self-contained module
├── 02-Subtopic-B.html     # Self-contained module
├── ...
└── 08-Tools-Code.html     # Tools + code examples + reference
```

## Template Pattern

Each content file has:
1. Shared nav sidebar (links to all files including index)
2. `<h1>` title
3. Hero summary box
4. Sections with `<h2>`, subsections with `<h3>`/`<h4>`
5. ASCII diagrams, tables, formulas, code blocks, exercises
6. Footer with cross-links back to index

## Pitfalls

### 1. Section Numbering After Patches

When inserting new sections between existing ones via `patch()`, ALL subsequent section numbers must be renumbered. Common mistake: inserting §3 causes old §3/§4/§5 to need renumbering to §4/§5/§6.

**Fix:** After any patch that inserts a new `<h2>` section, grep for all `<h2>` tags and verify sequential numbering.

### 2. Nav Sidebar as Content

The nav sidebar contains `<h2>` which may confuse grep-based audits. When auditing section structure, exclude the nav area (grep content `<h2>` only, not sidebar ones).

### 3. Cross-Link Integrity

After generating all files, verify all `href="*.html"` links resolve to existing files. Broken links break the reading flow.

### 4. Content Completeness Audit

After initial generation, audit each module for missing topics:
```bash
for kw in "topic1" "topic2" ...; do
  files=$(grep -rl "$kw" 0[1-8]*.html 2>/dev/null | tr '\n' ' ')
  [ -z "$files" ] && echo "MISSING: $kw"
done
```

### 5. User Demand for Thoroughness

User said "务必做到详尽" (must be thorough/exhaustive). After generating, always:
1. Audit for missing topics by keyword
2. Check section numbering is sequential
3. Verify cross-links
4. Check file sizes are roughly balanced (not one 50KB file next to a 5KB one)

## Why Not Monolithic

User explicitly rejected single large files (>80KB). Reasons:
- Hard to navigate by topic
- Can't update one section without touching unrelated content
- Breaks the "high cohesion, low coupling" principle
