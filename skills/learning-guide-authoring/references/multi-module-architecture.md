# Multi-Module HTML Guide Architecture

Learned from building a 12-file, 244KB optimization methods guide (2026-06).

## Core Principles (user enforced)

1. **High cohesion, low coupling**: Each file self-contained. Cross-ref via links, never copy-paste.
2. **Multi-perspective index**: Index page must have ≥2 views:
   - 按方法分类 (by method) — for systematic learning
   - 按问题分类 (by problem) — table: problem → theory/solving/approximation/scenario
   - 按场景分类 (by scenario) — table: domain → keywords → recommended entry
3. **Merge related topics**: "What is X" + "How to solve X" = ONE file, not two. Use `<div class="divider">` internally.
4. **Consistent depth**: Every h2 needs 2-4 h3 subsections. Flat h2 with no h3 = thin content.
5. **Domain modules**: Organized by domain sub-types (e.g., 10 network types), NOT by optimization method. Each domain section links back to theory modules.

## Section Numbering Pitfalls

When inserting new sections mid-file:
- Renumber in REVERSE order (highest first) to avoid collision
- After any merge/patch, verify: `grep -oP '<h3>\K\d+\.\d+' file | sort | uniq -d`
- Two-part merged files can have independent numbering if divider is clear

## Content Density Targets

- ~8-15K text chars per module (after stripping HTML)
- 5-20 h3 sections per module
- 3-12 code blocks per module
- 1-7 tables per module
- Each module should have ≥1 exercise

## Shared Template Pattern

Use Python script with:
- `CSS` constant (shared styles)
- `NAV_ITEMS` list (file→label pairs)
- `make_nav(active_file)` function (highlights current page)
- `wrap(active_file, title, body)` function
- `save(fname, title, body)` function

This ensures consistent nav/cross-refs across all files.

## Nav Sidebar

Every file gets identical nav sidebar. Current page gets `class="active"`. Nav items are ordered by module number. All cross-references use the nav sidebar's link targets.

## Audit Checklist

After building all modules:
1. Link integrity: `grep -oP 'href="\K[^"#]+\.html' file` → check each exists
2. Section numbering: no gaps, no duplicates
3. Content density: text chars per module should be balanced (no module <50% of average)
4. Cross-references: every module links to related modules (bidirectional)
5. Index completeness: all modules listed in both classification views
