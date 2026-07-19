# Existing Project Organization & Audit (2026-06)

When the user asks to "整理" (organize), "审计" (audit), or "检查" (check) an EXISTING learning guide project (not creating new content), follow this systematic approach.

## Phase 1: Full Project Audit

### 1.1 File Inventory
```bash
# Count files per directory
for d in <root>/*/; do
    name=$(basename "$d")
    count=$(find "$d" -name "*.html" -type f 2>/dev/null | wc -l)
    size=$(du -sh "$d" 2>/dev/null | cut -f1)
    echo "$name: $count HTML, $size"
done

# Total
find <root> -name "*.html" -type f | wc -l
du -sh <root>
```

### 1.2 Empty Shell Detection
Find files that are pure CSS templates with no actual content:
```bash
# Files with <20 lines (likely empty shells)
find <root> -name "*.html" -type f | while read f; do
    lines=$(wc -l < "$f")
    if [ "$lines" -lt 20 ]; then
        echo "⚠️ $f: ${lines}行"
    fi
done
```

**Thresholds:**
- <5 lines: 🔴 Pure CSS shell, no content
- 5-20 lines: 🟡 Thin content or navigation-only index
- 20-50 lines: Check if content is substantive

### 1.3 Index Coverage Check
```bash
# Check which directories have index.html
for d in <root>/*/; do
    if [ -f "$d/index.html" ]; then
        echo "✅ $(basename "$d")"
    else
        echo "❌ $(basename "$d") - MISSING index.html"
    fi
done
```

### 1.4 Cross-Reference Analysis
```bash
# Check for cross-references between sections
# Search for href patterns pointing to other directories
grep -r 'href=".*\.\./' <root>/*.html | head -20
```

## Phase 2: Priority Classification

### P0 — Critical (affects basic usability)
- Missing top-level index.html files
- Empty shell files (pure CSS, no content)
- Placeholder files (README.html with <10 lines)
- Broken navigation links

### P1 — High (affects content quality)
- Thin content files (key concepts with <50 lines)
- No cross-references between sections (knowledge islands)
- Content duplication without cross-links
- Outdated information

### P2 — Medium (affects project structure)
- Non-standard naming (00-index.html vs index.html)
- Large files that should be split (PDFs, etc.)
- Missing breadcrumb navigation
- Inconsistent CSS themes

### P3 — Low (optimization)
- Adding global navigation
- Content enrichment for already-substantive files
- Visual improvements

## Phase 3: Repair Strategy

### For Missing Index Files
Create navigation index.html for each directory:
- Title with directory name
- Brief description
- Links to all subdirectories
- Links back to parent index
- Prev/next navigation

### For Empty Shells
1. Read the existing CSS template
2. Create comprehensive content matching the file's intended topic
3. Maintain the same dark theme CSS
4. Add navigation links (prev/next/back to index)
5. Include: ASCII diagrams, tables, practical examples

### For Cross-References
Add bidirectional links between related sections:
- Forward link: Overview → Deep-dive
- Reverse link: Deep-dive → Overview

Format:
```html
<div class="highlight">
<strong>🔗 相关深入章节：</strong><br>
• <a href="RELATIVE_PATH">章节名称</a> — 简短描述
</div>
```

### For Content Duplication
When the same topic exists in multiple directories:
1. Verify if it's true duplication or different purposes
2. If different purposes (e.g., "技术深度学习" vs "厂商概览"), add cross-references
3. If true duplication, consider merging or clearly differentiating

## Pitfalls

- **Don't create new content before fixing existing issues.** Audit first, then repair.
- **Don't merge directories without checking their purpose.** Two directories about the same topic may serve different functions.
- **Always read before writing.** Check existing content structure before modifying.
- **Use relative paths for cross-references.** Absolute paths break when files move.
- **Don't declare "complete" too early.** The user will keep pushing if they see gaps.
- **But also know when to stop.** If the user keeps saying "继续" without specific direction, declare completion and ask for specific guidance.
