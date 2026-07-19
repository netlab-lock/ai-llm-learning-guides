# SVG Diagrams & Interview Preparation Patterns

## SVG Diagrams > ASCII Art (2026-06 learned)

User explicitly asked: "你很喜欢画ASCII架构图，但html下不是有办法画出更好看，更直观的图吗？"

**Prefer SVG/CSS diagrams over ASCII art in HTML guides.** ASCII art is limited and looks crude in HTML.

### Design System (from architecture-diagram skill)

Use the `architecture-diagram` skill's design system for professional dark-themed SVG diagrams:

```html
<div class="diagram">
  <div class="diagram-title">Title</div>
  <div class="stack">
    <div class="stack-layer l1">
      <div class="label">应用层</div>
      <div class="content">内容</div>
    </div>
    <!-- more layers -->
  </div>
</div>
```

CSS classes for diagram components:
- `.diagram` — container with dark card background
- `.flow` / `.flow-box` / `.flow-arrow` — horizontal flow diagrams
- `.stack` / `.stack-layer.l1-l5` — vertical stack diagrams
- `.grid-2` / `.grid-3` / `.grid-box` — grid layouts
- `.compare` / `.compare-side.good/.bad` — side-by-side comparison

Color mapping:
- `.l1` (blue/cyan) = Application/Frontend
- `.l2` (green/emerald) = Orchestration/Backend
- `.l3` (yellow/violet) = Capabilities/Logic
- `.l4` (purple) = Models/Data
- `.l5` (red/rose) = Infrastructure/Security

SVG should use:
- Semantic color fills with rgba transparency
- Grid pattern background (#020617 + #1e293b grid)
- Rounded rectangles (rx="6")
- Arrow markers for connections
- JetBrains Mono font

### When to use ASCII vs SVG

- **Use SVG**: Architecture diagrams, flow charts, layered stacks, comparisons
- **Keep ASCII**: Quick inline diagrams, terminal output examples, code comments
- **Rule of thumb**: If it's a standalone diagram that users will study, use SVG. If it's a quick illustration inside a paragraph, ASCII is fine.

## Interview Preparation Guide Pattern

User wanted "面试高频问题+参考答案". Pattern learned:

### Structure per Q&A
```html
<div class="qa">
  <div class="q">Q: Question text</div>
  <div class="a">
    <p><span class="key">回答要点：</span></p>
    <ul>...</ul>
    <p><span class="key">追问方向：</span>What interviewers will ask next</p>
  </div>
</div>
```

### CSS for Q&A blocks
```css
.qa{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.2rem;margin:1rem 0}
.qa .q{color:var(--yellow);font-weight:700;font-size:1.05em;margin-bottom:.5rem}
.qa .a{color:var(--text)}
.qa .key{color:var(--green);font-weight:600}
```

### Interview module must-haves
- 20+ Q&A pairs covering all major topics
- Each Q&A has: 回答要点 + 追问方向
- STAR template for project experience questions
- Preparation checklist with priority ranking (⭐⭐⭐⭐⭐ = must-know)
- 12-15 day study plan

## Breadth + Depth Audit Methodology

When user says "尽量详尽、全面、深入", do a systematic audit:

### Breadth check
```bash
# Check if key topics exist across the guide
for topic in "Topic1" "Topic2"; do
  count=$(grep -cirl "$topic" *.html | wc -l)
  echo "$topic: $count files"
done
```

### Depth check
```bash
# Check formula/code/element density per module
for f in *.html; do
  formulas=$(grep -c 'class="formula"' "$f")
  code=$(grep -c '<pre><code>' "$f")
  echo "$f: formulas=$formulas code=$code"
done
```

### Density check
```bash
# Check per-section density (chars per h2)
for f in *.html; do
  total=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  h2=$(grep -c '<h2' "$f")
  avg=$((total / h2))
  echo "$f: ${avg}字/节"
done
```

Target: ratio of largest/smallest module < 2.0

## f-string Escaping Pitfall

When generating HTML with Python f-strings, curly braces in code blocks MUST be escaped:
```python
# WRONG — Python interprets {content} as f-string variable
f'<pre><code>messages=[{{"role": "user", "content": "{query}"}}]</code></pre>'

# CORRECT — double braces escape
f'<pre><code>messages=[{{{{"role": "user", "content": "{query}"}}}}]</code></pre>'
```

Better approach: Use `write_file` directly with string concatenation instead of f-strings:
```python
content = '''<!DOCTYPE html>...'''
# No f-string, no escaping needed
```

## Multi-Module Guide Checklist

When creating a multi-module guide (10+ files):

1. **Create index page first** — hub with navigation cards, roadmap, stats
2. **Generate modules in batches** — 2-3 modules per script
3. **Audit after generation** — check sizes, elements, coverage
4. **Enrich weak modules** — bring all to minimum density
5. **Add cross-references** — link related modules
6. **Fix navigation** — prev/next links, consistent sidebar
7. **Final verification** — broken links, duplicate sections, HTML balance
