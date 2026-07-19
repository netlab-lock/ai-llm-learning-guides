# Modular Multi-File Learning Guide Patterns

Patterns learned from building a 12-module, 289KB optimization methods guide.

## Architecture

```
topic-guide/
├── 00-index.html          ← Hub with multiple classification views
├── 01-TopicA.html         ← Self-contained module per major topic
├── 02-TopicB.html
├── ...
└── NN-Tools-Code.html     ← Practical tools + code
```

## Index Page Multi-View Design

The index page should provide 4 views for maximum discoverability:

1. **模块导航** — card grid, one card per module with brief description
2. **按问题分类** — table: Problem | Theory Module | Solving | Approximation | Scenario
3. **按场景分类** — table: Scenario | Keywords | Typical Problems | Entry Point
4. **学习路线** — phased progression from basics to advanced
5. **全景分类树** — ASCII tree showing full taxonomy

## Cross-Reference Pattern

Every module nav sidebar links to ALL modules. Current module gets class="active".
Body content links to related modules with context: "→ 模块X·具体章节"

## Audit Checklist

1. Section numbering: h2 sequential, no duplicate h3 within same h2 parent
2. Link integrity: every href target exists on disk
3. Content density: text chars per module balanced (±30%)
4. Cross-references: every module links to related modules
5. Consistency: same CSS/nav/footer across all files

## Merging Modules

When merging related modules:
- Keep independent section numbering per part
- Add visual divider between parts
- Label parts clearly
- Don't renumber — divider makes dual-numbering acceptable

## Python Generation Pattern

Use a single script that defines shared CSS + nav, generates all files, then verifies.
For reorganization: extract body content, re-wrap with clean template.
