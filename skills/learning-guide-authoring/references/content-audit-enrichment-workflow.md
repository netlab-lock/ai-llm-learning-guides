# Content Audit & Enrichment Workflow (2026-06)

Discovered during Agent学习指南 creation. After generating a multi-module guide, systematically audit and enrich weak modules to meet quality standards.

## Step 1: Quantitative Audit

Count content elements per file to identify weak modules:

```bash
cd "/path/to/guide"
for f in *.html; do
  chars=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  tips=$(grep -c 'class="tip"' "$f")
  warns=$(grep -c 'class="warn"' "$f")
  exs=$(grep -c 'class="exercise"' "$f")
  deeps=$(grep -c 'class="deep"' "$f")
  h2s=$(grep -c '<h2' "$f")
  printf "%-35s %5d字 tip:%d warn:%d ex:%d deep:%d h2:%d\n" "$f" "$chars" "$tips" "$warns" "$exs" "$deeps" "$h2s"
done
```

### Content Density Targets

| Element | Minimum per Module | Purpose |
|---------|-------------------|---------|
| tip boxes | 1 | Practical advice |
| warn boxes | 1 | Pitfalls and warnings |
| exercise boxes | 1 | Hands-on practice |
| deep boxes | 1 | Historical/technical deep dive |
| ASCII diagrams | 2 | Visual explanation of concepts |
| tables | 3 | Structured comparisons |
| h2 sections | 5-8 | Logical structure |
| text chars | 8000+ | Substantial content |

### Red Flags

- Any module with 0 tip/warn/exercise/deep boxes → needs enrichment
- Module < 60% of average char count → needs major enrichment
- Module with < 2 ASCII diagrams → needs visual content
- Module with < 3 tables → needs structured comparisons

## Step 2: Content Coverage Audit

Check for domain-specific keywords that should be covered:

```bash
# Check if specific topics are covered
for keyword in "TopicA" "TopicB" "TopicC"; do
  echo -n "$keyword: "
  grep -ci "$keyword" module_file.html
done
```

## Step 2: Topic Coverage Audit

After quantitative audit, check if domain-specific keywords are covered. Define expected topics per module:

```python
expected_topics = {
    "01": ["ConceptA", "ConceptB", "KeyTerm1"],
    "02": ["ConceptC", "ConceptD", "KeyTerm2"],
    # ...
}

for mod, keywords in expected_topics.items():
    missing = []
    for kw in keywords:
        r = terminal(f"grep -ci '{kw}' '{base}/{files_map[mod]}'")
        count = int(r.get("output", "0").strip() or "0")
        if count == 0:
            missing.append(kw)
    if missing:
        print(f"Module {mod} missing: {', '.join(missing)}")
```

Also check for **globally important topics** that should exist SOMEWHERE in the guide:

```bash
cd /path/to/guide
for topic in "TopicA" "TopicB" "TopicC"; do
  count=$(grep -cirl "$topic" *.html | wc -l)
  [ "$count" -eq 0 ] && echo "MISSING GLOBALLY: $topic"
done
```

### Pitfall: Sandbox grep limitations
The `execute_code` sandbox may have issues with grep patterns containing dots (interpreted as regex wildcards). Use `terminal()` directly for reliable grep checks, not `execute_code` + subprocess.

## Step 2b: Cross-Reference Audit

Check that modules link to related content in OTHER modules, not just sequential prev/next:

```bash
# Count cross-module references (non-sequential)
for f in *.html; do
  refs=$(grep -oP 'href="[0-9]+-[^"]*\.html"' "$f" | sort -u | wc -l)
  echo "$f: $refs cross-module links"
done
```

**Target**: Each module should have 2-5 cross-references to related modules.
**Common missing links**:
- Module on "推理" should link to "架构" (where推理is used)
- Module on "记忆" should link to "工具" (RAG as tool) and "安全" (data poisoning)
- Module on "安全" should link to "评估" (security benchmarks)
- Module on "框架" should link to "多Agent" (frameworks implement multi-agent)

### Pattern: Add cross-reference tip box

```python
patch(
    "/path/to/module.html",
    old_string="""<h2>小结</h2>""",
    new_string="""<div class="tip"><strong>💡 相关模块：</strong>Topic X的详细内容见<a href="0Y-module.html">模块Y</a>，相关实践见<a href="0Z-module.html">模块Z</a>。</div>

<h2>小结</h2>""",
    replace_all=False
)
```

Place cross-reference tips **before the summary table** — readers checking the summary will see related modules.

## Step 3: Enrichment via patch()

Use `hermes_tools.patch()` to add content to existing HTML files WITHOUT rewriting them. This is much more efficient than regenerating entire files.

### Pattern: Add a content box before a section

```python
from hermes_tools import patch

# Add tip box before a section
patch(
    "/path/to/module.html",
    old_string="""<h2>3. Some Section</h2>""",
    new_string="""<div class="tip"><strong>💡 Practical advice:</strong>Content here.</div>

<h2>3. Some Section</h2>""",
    replace_all=False
)
```

### Pattern: Add deep dive after a section

```python
patch(
    "/path/to/module.html",
    old_string="""<h2>Next Section</h2>""",
    new_string="""<div class="deep"><strong>🔬 Deep analysis:</strong>Detailed content.</div>

<h2>Next Section</h2>""",
    replace_all=False
)
```

### Pattern: Add exercise before summary

```python
patch(
    "/path/to/module.html",
    old_string="""<h2>小结</h2>""",
    new_string="""<div class="exercise"><strong>🧪 Hands-on exercise:</strong>
<pre><code>code example here</code></pre>
</div>

<h2>小结</h2>""",
    replace_all=False
)
```

### Pattern: Enrich summary table

```python
patch(
    "/path/to/module.html",
    old_string="""<tr><td>Concept</td><td>Old description</td></tr>
</table>""",
    new_string="""<tr><td>Concept</td><td>Old description</td></tr>
<tr><td>NewConcept</td><td>New description</td></tr>
</table>""",
    replace_all=False
)
```

## Step 4: Verification

After enrichment, re-run the quantitative audit:

```bash
# Check final sizes
du -sh /path/to/guide/
# Compare before/after
# Target: all modules within 60-100% of largest module
```

## Priority Order for Enrichment

1. **Weakest module** (lowest char count, fewest elements)
2. **Core technical modules** (most important for learning)
3. **Modules missing exercises** (user needs hands-on practice)
4. **Modules missing deep boxes** (user wants depth)

## Enrichment Content Ideas

### tip boxes
- Tool/framework recommendations
- "Start with X, only add Y when needed"
- Links to official docs

### warn boxes
- Common mistakes and pitfalls
- "Don't do X"
- Performance/security warnings

### exercise boxes
- Complete code examples
- Step-by-step tutorials
- "Try this yourself" prompts

### deep boxes
- Historical context
- "Why it had to be this way"
- Research paper insights
- Real-world case studies

## Example: Agent Guide Enrichment Results

```
Module  Before   After   Growth
09      5144字   15878字  +209%
10      6108字   13451字  +120%
08      7064字   14304字  +102%
11      6280字   12629字  +101%
Total   ~86K字   ~170K字  +97%
```

Key lesson: The audit-enrich cycle is more efficient than trying to generate perfect content on the first pass. Generate "good enough" first, then systematically improve based on metrics.

## Multi-Round Audit Pattern (2026-06 Agent Guide, updated)

When user asks to "再次检查" (re-check) after an initial enrichment round, use a **5-round audit** — each round checks DIFFERENT things:

**Round 1 — Quantitative**: Element counts (tip/warn/exercise/deep/ascii/table) + char counts. Enrich weakest modules.

**Round 2 — Topic Coverage**: Grep for domain-specific keywords per module. Fix missing topics (add sections, tables, code examples). Add cross-references between related modules.

**Round 3 — Global Gaps**: Check for important topics missing from the ENTIRE guide (not just one module). Use `grep -cirl 'topic' *.html | wc -l` to find globally absent concepts. Add them to the most relevant module.

**Round 4 — Per-Module Subtopic Audit**: Define 3-4 specific subtopics that SHOULD exist in each module. Grep for them. This catches gaps that global keyword checks miss (e.g., "Least-to-Most prompting" belongs in the reasoning module, "vertical industry agents" belongs in the applications module). Verify with a second grep using broader patterns — initial patterns may be too strict.

**Round 5 — Section-Level Density + HTML Correctness**:
- Calculate `chars_per_section = total_chars / h2_count` per module
- If ratio of highest/lowest > 2.0, enrich the thin modules
- Check for **duplicate sections** (especially `<h2>小结</h2>` appearing twice) — this happens when patching adds content before a section that was already present
- Thin sections (<15 lines for framework/product descriptions) need enrichment

Each round should produce a clear "before/after" comparison. Stop when:
- All modules have 6 element types (tip/warn/exercise/deep/ascii/table)
- All domain keywords are covered
- Cross-references exist between related modules
- No globally important topics are missing
- Section density ratio < 2.0
- No duplicate sections

**Anti-pattern**: Running the same audit script 3 times without changing the criteria = no progress. Each round must check DIFFERENT things.

### Round 5 Detail: Section-Level Density Metric

```bash
# Calculate characters per h2 section
for f in 0[1-9]*.html 1[01]*.html; do
  total=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  h2=$(grep -c '<h2' "$f")
  avg=$((total / h2))
  printf "%-30s %5d字 / %2d节 = %4d字/节\n" "$f" "$total" "$h2" "$avg"
done
```

- Healthy range: 1500-2500 chars per h2 section
- Red flag: < 1200 chars/section (sections are too thin)
- Red flag: ratio highest/lowest > 2.0 (unbalanced density)

### Round 5 Detail: Duplicate Section Detection

When using `patch()` to insert content before `<h2>小结</h2>`, the summary section itself is preserved. But if a later patch also targets `<h2>小结</h2>`, it may create a duplicate. Check with:

```bash
for f in *.html; do
  count=$(grep -c '<h2>小结</h2>\|<h2>Summary</h2>' "$f")
  [ "$count" -gt 1 ] && echo "DUPLICATE: $f has $count summary sections"
done
```

Fix: Read the file, find the second occurrence, remove it (keeping the first which has the summary table).
