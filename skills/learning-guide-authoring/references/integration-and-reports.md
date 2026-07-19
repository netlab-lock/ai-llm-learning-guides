# Integration Workflow & Research Report Guidelines

## Integrating New Content into Existing Series

When adding a new chapter/page to an existing HTML learning guide series (e.g., adding "K3" to a Kimi series that covers K2):

### Step 1: Discover Existing Structure
```
search_files(path=<series_dir>, pattern="*", target="files")
```
- Read the `index.html` to understand chapter numbering, CSS theme, nav pattern
- Read one existing chapter to extract the exact CSS block (copy it verbatim)
- Note: outer overview pages and inner deep-dive pages often have DIFFERENT CSS

### Step 2: Match CSS Exactly
- Copy the CSS `:root` variables, class definitions, and layout rules from existing files
- Do NOT introduce new CSS classes unless absolutely necessary
- Keep font families, color schemes, spacing consistent
- Use the same `.card`, `.note`, `.warn`, `.tip`, `.deep`, `.ascii`, `.tag-*` classes

### Step 3: Create New Files
- Outer overview: `<N>-<Title>.html` at the series root
- Inner deep-dive: `<N>-<Title>.html` in the `深度学习/` subdirectory
- Use `delegate_task` with 2 parallel subagents for large file creation
- Pass the exact CSS block in the context so subagents match the style

### Step 4: Update Index Files (CRITICAL)
- **Inner index**: Add row to the chapter table, update ASCII chapter list, update footer date
- **Outer index**: Update milestone timeline, model cards, chapter list, footer
- Use `patch` tool with `*** Begin Patch / *** End Patch` syntax
- Always verify with `read_file` after patching

### Step 5: Cross-Reference
- New overview page should link to deep-dive: `<a href="深度学习/12-X.html">→ 深入学习</a>`
- Deep-dive nav bar should link to adjacent chapters
- Both indexes should reference the new files

## Research Report Workflow

**RULE: When the user asks for a "调研报告" (research report), ALWAYS save it to a file proactively. Do NOT just output to terminal.**

### Preferred Output Format: HTML with SVG Diagrams
- User explicitly prefers **SVG diagrams over ASCII art** ("最好是svg图，而非ascii图")
- Use the `architecture-diagram` skill's design system for SVG creation
- Dark theme (#020617 background), JetBrains Mono font, semantic color mapping
- Self-contained single HTML file, no external dependencies (except Google Fonts)

### Report Structure Template
1. Header with title, subtitle, date, sources
2. Table of Contents (linked)
3. Background & Significance (with timeline SVG)
4. System Architecture (with architecture SVG)
5. Algorithm Details (with mechanism diagrams + math + analogies)
6. Benchmarks (with comparison tables + bar chart SVGs)
7. Real-world Applications (cards)
8. Limitations (callout boxes)
9. Summary & Outlook (cards)

### SVG Diagram Types to Include
- **Timeline/evolution**: Model version history with milestone markers
- **Architecture overview**: System components with data flow arrows
- **Mechanism diagrams**: Algorithm internals (attention patterns, routing, etc.)
- **Comparison bar charts**: Benchmark scores as horizontal bars
- **Conceptual diagrams**: Analogies visualized (e.g., library → attention)

### File Naming
- Standalone report: `<topic>-report.html` in the user's working directory
- Integrated guide: Follow the series naming convention

## Pitfalls

1. **Don't output long reports to terminal only** — user will ask "有没有保存？"
2. **Don't use ASCII art when SVG is possible** — user considers ASCII "简陋"
3. **Don't forget to update BOTH indexes** — outer and inner, if the series has both
4. **Don't introduce new CSS** — match existing files exactly
5. **Don't skip nav bars** — every page needs prev/next/index navigation
6. **Subagent CSS mismatch** — always pass the exact CSS block in delegate_task context
