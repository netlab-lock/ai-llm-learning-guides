# Multi-Round Audit Workflow for Learning Guides (2026-06)

When the user asks "检查指南是否还有需要补充的内容" or "audit the guide", use this systematic multi-round audit process. Each round catches different types of gaps.

## Round 1: Element Counting
Count teaching elements per module. Every module should have at least 1 of each:
```bash
for f in *.html; do
  chars=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  tips=$(grep -c 'class="tip"' "$f")
  warns=$(grep -c 'class="warn"' "$f")
  exs=$(grep -c 'class="exercise"' "$f")
  deeps=$(grep -c 'class="deep"' "$f")
  ascii=$(grep -c 'class="ascii"' "$f")
  tables=$(grep -c '<table' "$f")
  printf "%-30s %5d字 tip:%d warn:%d ex:%d deep:%d 图:%d 表:%d\n" "$f" "$chars" "$tips" "$warns" "$exs" "$deeps" "$ascii" "$tables"
done
```
Action: Enrich modules with 0-count elements.

## Round 2: Topic Coverage
Define expected topics per module, then grep for each:
```bash
echo -n "CoT: "; grep -c "CoT\|Chain-of-Thought" 03*.html
```
Pitfall: grep patterns with dots treat . as regex wildcard. Use \. for literal dots.

## Round 3: Global Missing Topics + Cross-References
Check for important topics missing from the ENTIRE guide:
```bash
echo -n "Grounding: "; grep -cirl 'grounding\|事实锚定' *.html | wc -l
```
Also check cross-references between non-adjacent modules. Add tip boxes linking related modules.

## Round 4: Per-Module Subtopic Audit
Define specific subtopics each module should cover. Always do a SECOND verification pass with broader patterns before concluding missing — initial grep patterns are often too strict.

## Round 5: Section-Level Density + HTML Correctness
Check density at h2-section level:
```bash
for f in *.html; do
  total=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  h2=$(grep -c '<h2' "$f")
  avg=$((total / h2))
  printf "%-30s %5d字 / %2d节 = %4d字/节\n" "$f" "$total" "$h2" "$avg"
done
```
Target: 1500-2500 chars per h2 section. Red flag: below 1200. Ratio highest/lowest should be below 2.0.

## When to Stop
After Round 5, the guide is typically complete. If user keeps asking, declare completion and ask for specific direction.
