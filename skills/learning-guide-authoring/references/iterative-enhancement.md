# Iterative Enhancement & Audit Methodology

Learned from building a 13-module, 500KB collective communication guide (2026-06).

## When to Use

User says: "检查广度和深度" / "查缺补漏" / "补充知识点" / "更加详尽全面深入"

## Phase 1: Breadth Audit (keyword coverage)

```bash
base='/path/to/guide/'
# Define domain-specific keywords
for kw in 'keyword1' 'keyword2' ...; do
  cnt=$(grep -rl "$kw" ${base}*.html 2>/dev/null | wc -l)
  if [ $cnt -eq 0 ]; then echo "❌ $kw"; else echo "✅ $kw ($cnt)"; fi
done
```

Build a checklist: missing topics by category (hardware/algorithms/libraries/systems/frontier).

## Phase 2: Depth Audit (quality markers)

For each existing section, check:
- ASCII diagrams? (not just text)
- Concrete numbers? (not just "faster/slower")
- Step-by-step walkthroughs? (not just high-level)
- Comparison tables? (not just one-sided)
- Formulas with real values substituted?
- Interview-worthy Q&A?

Flag sections that are "概念层" (concept-only) as needing deepening.

## Phase 3: Parallel Enhancement

Use `delegate_task` with ≤3 subagents. Each gets:
- A specific file + insertion point + content spec
- Uses `read_file` + `patch` to add content

**Pitfall**: Subagents modifying the SAME file simultaneously → conflicts.
Assign each subagent to a DIFFERENT file, or non-overlapping insertion points.

**Pitfall**: Subagent rate limits (HTTP 429). If 2/3 fail, do the remaining manually.

## Phase 4: Re-audit

Repeat Phase 1+2 to verify gaps filled. Update index/nav if new modules added.

## Multi-Dimensional Content

When user asks from "面试/工作/研究/学习" angles:
- 面试: `class="deep"` Q&A cards with detailed answers
- 工作: production checklists, env var tables, debugging flowcharts
- 研究: paper refs, theoretical models, mathematical proofs
- 学习: learning path timelines, prerequisite chains, exercises

## Parallel File Modification Pattern

```
delegate_task(tasks=[
  {"goal": "Read file_A, add section X before anchor Y", "toolsets": ["file"]},
  {"goal": "Read file_B, add section Z before anchor W", "toolsets": ["file"]},
  {"goal": "Read file_C, add section V before anchor U", "toolsets": ["file"]},
])
```

After completion:
1. `wc -l -c *.html | tail -1` — verify all files grew
2. `grep -c 'class="ascii"' *.html` — verify diagrams added
3. Update index.html badges/roadmap/footer LAST

## Large Guide Enhancement Priority

For guides with 10+ modules, 200KB+:
1. Prioritize by impact: smallest/shortest modules first
2. Use `grep -n` to find insertion points before patching
3. After all patches, verify: `wc -l -c *.html`
4. Create "知识全景图" summary tying everything together
