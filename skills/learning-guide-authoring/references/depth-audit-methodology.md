# Depth Audit & Enrichment Methodology

## When to apply
User says "更详尽、全面、深入", "写书的深度", "不要浮于表面", or keeps pushing for more content after 3+ rounds.

## Per-module depth checklist
Each module should have ALL of these elements:
- [ ] **Mathematical formulas** (`.formula` class) — at least 1 per quantitative topic
- [ ] **Code examples** (`<pre><code>`) — at least 1 runnable code block per module
- [ ] **Comparison tables** — detailed tradeoffs with 4+ columns and specific numbers
- [ ] **ASCII/SVG diagrams** — architecture, flow, or concept visualization
- [ ] **Tip boxes** — practical advice, best practices
- [ ] **Warn boxes** — pitfalls, common mistakes
- [ ] **Exercise boxes** — hands-on practice or interview simulation
- [ ] **Deep boxes** — historical context, "why it had to be this way"

## Depth audit command
```bash
cd DIR && for f in *.html; do
  chars=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  fm=$(grep -c 'class="formula"' "$f")
  cd=$(grep -c '<pre><code>' "$f")
  t=$(grep -c 'class="tip"' "$f")
  w=$(grep -c 'class="warn"' "$f")
  e=$(grep -c 'class="exercise"' "$f")
  d=$(grep -c 'class="deep"' "$f")
  printf "%-35s %5d字 formula:%d code:%d tip:%d warn:%d ex:%d deep:%d\n" "$f" "$chars" "$fm" "$cd" "$t" "$w" "$e" "$d"
done
```

## "Book-level depth" enrichment order
When enriching a module, add content in this priority order:
1. **Mathematical foundations** — formulas with variable explanations (highest impact per byte)
2. **Implementation code** — complete, runnable examples (not pseudocode)
3. **Detailed comparison tables** — 4+ columns with specific numbers
4. **Historical context** — who invented it, when, why, what problem it solved
5. **Common pitfalls** — real-world failure modes with solutions

## Signals that content is too shallow
- Module has 0 formulas AND covers a quantitative topic (RAG, attention, similarity)
- Module has 0 code examples AND covers a practical topic
- Module has 0 comparison tables AND covers multiple alternatives
- Per-section average < 1500 characters (sections are too thin)
- User keeps asking "还有没有可以补充的" after multiple rounds

## Multi-round audit workflow
1. **Round 1: Breadth** — Check topic coverage with grep for key terms
2. **Round 2: Depth** — Check formula/code/table counts per module
3. **Round 3: Quality** — Spot-read thin sections, verify accuracy
4. **Round 4: Cross-references** — Ensure modules link to related content
5. **Round 5: Consistency** — Check nav links, summary tables, formatting

## Pitfall: f-string curly braces
When generating HTML with Python f-strings, ALL literal curly braces in code examples must be doubled (`{{` / `}}`). Safer: use string concatenation instead of f-strings for HTML with code blocks.
