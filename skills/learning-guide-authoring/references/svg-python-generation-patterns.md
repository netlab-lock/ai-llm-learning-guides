# SVG Python Generation Patterns for HTML Learning Guides

## Reusable Helper Functions

These helpers generate SVG primitives for dark-themed architecture diagrams. Use string concatenation (NOT f-strings) to avoid nested-brace parsing errors.

### SVG Common Definitions (paste into every SVG)

```python
SVG_DEFS = '''
    <defs>
      <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
        <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
      </pattern>
      <marker id="arrow" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#475569"/>
      </marker>
      <marker id="arrow-cyan" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#22d3ee"/>
      </marker>
      <marker id="arrow-emerald" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#34d399"/>
      </marker>
      <marker id="arrow-amber" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#fbbf24"/>
      </marker>
      <marker id="arrow-rose" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#fb7185"/>
      </marker>
      <marker id="arrow-violet" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
        <polygon points="0 0, 10 3.5, 0 7" fill="#a78bfa"/>
      </marker>
    </defs>
'''
```

### Helper Functions (string concatenation, NOT f-strings)

```python
def box(x, y, w, h, fill, stroke, label, label2=None, fs=13):
    """Rounded rect with centered label(s)."""
    yoff = -2 if label2 else 5
    cx, cy = x+w//2, y+h//2+yoff
    t2 = '\n    <text x="'+str(cx)+'" y="'+str(y+h//2+16)+'" text-anchor="middle" fill="#94a3b8" font-size="11">'+label2+'</text>' if label2 else ''
    return '<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(w)+'" height="'+str(h)+'" rx="8" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.5"/>\n    <text x="'+str(cx)+'" y="'+str(cy)+'" text-anchor="middle" fill="'+stroke+'" font-size="'+str(fs)+'" font-weight="600">'+label+'</text>'+t2

def arrow(x1, y1, x2, y2, color="#475569"):
    """Line with arrowhead marker."""
    cmap = {"#22d3ee":"arrow-cyan","#34d399":"arrow-emerald","#fbbf24":"arrow-amber","#fb7185":"arrow-rose","#a78bfa":"arrow-violet","#475569":"arrow"}
    mk = cmap.get(color, "arrow")
    return '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" stroke="'+color+'" stroke-width="2" marker-end="url(#'+mk+')"/>'

def txt(x, y, text, color="#94a3b8", fs=11, anchor="middle"):
    """Simple text label."""
    return '<text x="'+str(x)+'" y="'+str(y)+'" text-anchor="'+anchor+'" fill="'+color+'" font-size="'+str(fs)+'">'+text+'</text>'
```

### Semantic Color Reference

| Component Type       | Fill (rgba)              | Stroke     | Use For                    |
|---------------------|--------------------------|------------|----------------------------|
| Frontend/Input       | rgba(8,51,68,0.4)       | #22d3ee    | API gateway, client, input |
| Backend/Process      | rgba(6,78,59,0.4)       | #34d399    | Engine, worker, compute    |
| Database/Storage     | rgba(76,29,149,0.4)     | #a78bfa    | Cache, storage, NIC        |
| Cloud/External       | rgba(120,53,15,0.3)     | #fbbf24    | Orchestration, KV transfer |
| Security/Risk        | rgba(136,19,55,0.4)     | #fb7185    | Hardware, GPU, limitations |
| Message/Bus          | rgba(251,146,60,0.3)    | #fb923c    | Planning, scheduling       |

### SVG Container Template

```python
svg = '''<div class="diagram">
<div class="diagram-title">Title Here</div>
<svg width="100%" viewBox="0 0 720 400" xmlns="http://www.w3.org/2000/svg">
  ''' + SVG_DEFS + '''
  <rect width="720" height="400" fill="#020617" rx="8"/>
  <rect width="720" height="400" fill="url(#grid)" rx="8"/>
  <!-- components here -->
</svg>
</div>'''
```

### Required CSS (add to all files with SVG)

```css
.diagram{background:#0d1117;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin:1.5rem 0;overflow-x:auto}
.diagram-title{color:#58a6ff;font-weight:700;font-size:1.05em;margin-bottom:1rem;text-align:center}
```

## Batch Upgrade Workflow

1. Count ASCII diagrams per file: `grep -c 'class="ascii"' *.html`
2. Identify top 1-2 most impactful diagrams per file (architecture > flow > comparison)
3. Write Python script to `/tmp/svg_upgrade_pN.py` (2-3 files per script)
4. Pattern: read HTML → `split('<div class="ascii">')` → replace first match → write back
5. Add `.diagram` CSS if missing
6. Verify SVG/DIV tag balance: `grep -c '<svg\|</svg>\|<div\|</div>' file.html`

## Pitfall: f-string Nested Braces

`{5 if not label2 else -2}` inside an f-string is parsed as set literal → `TypeError`.
**Always** compute values in separate variables before string interpolation.
Use string concatenation (`'a'+str(b)+'c'`) for HTML content, NOT f-strings.
