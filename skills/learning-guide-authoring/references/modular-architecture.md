# Modular Multi-File Architecture (高内聚低耦合)

When the guide exceeds ~15KB or covers multiple distinct sub-topics, split into modular files. User may request this explicitly ("分块建HTML", "高内聚低耦合") or it may be the right approach for broad topics.

## Structure
```
topic-name/
├── 00-index.html          Hub page: navigation cards, overview, learning roadmap
├── 01-subtopic-A.html     Self-contained module
├── 02-subtopic-B.html     Self-contained module
├── ...
└── NN-reference.html      Tools, code examples, quick-reference tables
```

## Principles
1. **High Cohesion**: Each file covers ONE topic completely. A reader gets full value from any single file without reading others.
2. **Low Coupling**: Files link to each other via `<a href>` but never duplicate content. If topic X is in module 3, module 5 links to it rather than re-explaining.
3. **Shared Navigation Sidebar**: Every file has the same nav sidebar linking all modules. Use a template function to generate it.
4. **Hub Page (00-index)**: Card grid of all modules + learning roadmap + classification tree.
5. **Balanced Density**: After generating, audit text-char counts per file. If any file is <60% of the average, it needs enrichment.

## Generation Pattern
Use a Python script with:
- `CSS` constant (shared styles)
- `NAV` constant with `{base}` placeholder for relative paths
- `wrap(title, body)` function that returns full HTML
- One function per module (`gen_01()`, `gen_02()`, ...)
- All write to the output directory

## Cross-Reference Format
```html
<a href="03-DP.html" style="color:var(--accent)">三</a>
```
Always use relative paths (no `../` needed since all files are in the same directory).

## Pitfalls

### Section Renumbering After Patches
**CRITICAL**: When inserting a new section via `patch()` (e.g., adding §3 before old §3), ALL subsequent section numbers must be renumbered. Old §3→§4, §4→§5, etc. Missing this creates duplicate numbering (two §3s) which confuses readers.

**Fix pattern**: After each insertion patch, do a separate patch for every subsequent `<h2>` and `<h3>` that needs renumbering. Use `grep -oP '<h[23]>\K\d+' file` to verify sequential numbering.

### Content Density Auditing
After generating all files, run:
```bash
for f in *.html; do
  chars=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  echo "$f: $chars chars"
done
```
If the ratio of largest/smallest > 2.0, the smallest module needs enrichment.

### Section-Level Density Metric (2026-06)
Check density at the section level, not just file level:
```bash
for f in *.html; do
  total=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  h2=$(grep -c '<h2' "$f")
  avg=$((total / h2))
  printf "%-30s %5d字 / %2d节 = %4d字/节\n" "$f" "$total" "$h2" "$avg"
done
```
- Healthy: 1500-2500 chars per h2 section
- Red flag: < 1200 chars/section (sections too thin, need enrichment)
- Red flag: ratio highest/lowest > 2.0 (unbalanced, enrich thin modules)

### Link Integrity Verification
After all files are generated:
```bash
for f in *.html; do
  links=$(grep -oP 'href="\K[^"#]+\.html' "$f" | sort -u)
  for link in $links; do
    [ ! -f "$link" ] && echo "BROKEN: $f -> $link"
  done
done
```

### Nav Sidebar Shows as h2 in Grep
The nav sidebar `<h2>` title appears in `grep '<h2'` output. This is NOT a content heading — it's the sidebar title. Don't confuse it with missing content structure.

### Cross-Reference Verification
After generating all files, verify cross-references exist between related modules (not just prev/next):
```bash
for f in *.html; do
  refs=$(grep -oP 'href="[0-9]+-[^"]*\.html"' "$f" | sort -u | wc -l)
  echo "$f: $refs cross-module links"
done
```
Modules should have 2-5 cross-module links. If a module has only prev/next links (count=2), add tip boxes linking to related content in other modules.

### Patches Multiply Across Rounds
When the user keeps asking "还有没有可以补充的地方" (any more gaps), do a systematic audit FIRST:
1. List all key topics for the domain
2. `grep -rl "keyword" *.html` to find coverage
3. Identify genuine gaps (topics that belong in the module's scope)
4. Patch only gaps, not cosmetic improvements
5. After patching, re-audit section numbering and link integrity

Do NOT keep making minor tweaks to declare "complete" — the user will notice. Find real gaps or state completion clearly.

### NP/Approximation/Complexity Coverage Checklist
When creating optimization or algorithm guides, ensure these topics are covered:
- P/NP/NP-complete/NP-hard definitions with Venn diagram
- Polynomial reduction concept
- Classic NPC problems: SAT, 3-SAT, Clique, Vertex Cover, Set Cover, Graph Coloring, Subset Sum, Hamiltonian
- Classic NP-hard optimization: TSP, Bin Packing, Scheduling (with Graham notation)
- Approximation classes: PTAS, FPTAS, APX, inapproximability
- Key approximation algorithms: VC 2-approx, Set Cover ln(n), Christofides 3/2, GW 7/8, Knapsack FPTAS
- Application scenarios for EACH problem (this is what users find most valuable)
