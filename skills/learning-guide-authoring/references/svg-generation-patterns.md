# SVG Diagram Generation Patterns

## Validated Box/Arrow Helper Functions

These functions were battle-tested across 14 SVG diagrams in the NVIDIA Dynamo guide. They avoid the nested-f-string pitfall by using string concatenation.

### box() — Rounded rect + centered label
```python
def box(x, y, w, h, fill, stroke, label, label2=None, fs=13):
    yoff = -2 if label2 else 5
    cx, cy = x+w//2, y+h//2+yoff
    t2 = '\n    <text x="'+str(cx)+'" y="'+str(y+h//2+16)+'" text-anchor="middle" fill="#94a3b8" font-size="11">'+label2+'</text>' if label2 else ''
    return '<rect x="'+str(x)+'" y="'+str(y)+'" width="'+str(w)+'" height="'+str(h)+'" rx="8" fill="'+fill+'" stroke="'+stroke+'" stroke-width="1.5"/>\n    <text x="'+str(cx)+'" y="'+str(cy)+'" text-anchor="middle" fill="'+stroke+'" font-size="'+str(fs)+'" font-weight="600">'+label+'</text>'+t2
```

### arrow() — Line with colored arrowhead marker
```python
def arrow(x1, y1, x2, y2, color="#475569"):
    cmap = {"#22d3ee":"arrow-cyan","#34d399":"arrow-emerald","#fbbf24":"arrow-amber","#fb7185":"arrow-rose","#a78bfa":"arrow-violet","#475569":"arrow"}
    mk = cmap.get(color, "arrow")
    return '<line x1="'+str(x1)+'" y1="'+str(y1)+'" x2="'+str(x2)+'" y2="'+str(y2)+'" stroke="'+color+'" stroke-width="2" marker-end="url(#'+mk+')"/>'
```

### txt() — Text label
```python
def txt(x, y, text, color="#94a3b8", fs=11, anchor="middle"):
    return '<text x="'+str(x)+'" y="'+str(y)+'" text-anchor="'+anchor+'" fill="'+color+'" font-size="'+str(fs)+'">'+text+'</text>'
```

## SVG_DEFS Template (paste once per SVG)

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

## Color Scheme (Semantic)

| Component Type | Fill | Stroke | Marker ID |
|:---|:---|:---|:---|
| Frontend/Input | `rgba(8,51,68,0.4)` | `#22d3ee` (cyan) | arrow-cyan |
| Backend/Process | `rgba(6,78,59,0.4)` | `#34d399` (emerald) | arrow-emerald |
| Database/Storage | `rgba(76,29,149,0.4)` | `#a78bfa` (violet) | arrow-violet |
| Cloud/External | `rgba(120,53,15,0.3)` | `#fbbf24` (amber) | arrow-amber |
| Security/Risk | `rgba(136,19,55,0.4)` | `#fb7185` (rose) | arrow-rose |
| Message/Bus | `rgba(251,146,60,0.3)` | `#fb923c` (orange) | arrow (default) |

## SVG Wrapper Template

```html
<div class="diagram">
<div class="diagram-title">图表标题</div>
<svg width="100%" viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg">
  ''' + SVG_DEFS + '''
  <rect width="W" height="H" fill="#020617" rx="8"/>
  <rect width="W" height="H" fill="url(#grid)" rx="8"/>
  <!-- components here -->
</svg>
</div>
```

## Required CSS (add to <style> if not present)

```css
.diagram{background:#0d1117;border:1px solid #30363d;border-radius:12px;padding:1.5rem;margin:1.5rem 0;overflow-x:auto}
.diagram-title{color:#58a6ff;font-weight:700;font-size:1.05em;margin-bottom:1rem;text-align:center}
```

## Workflow: Upgrading ASCII to SVG

1. Read the file, find all `<div class="ascii">...</div>` blocks
2. Pick the 1-2 most complex diagrams per file to upgrade (leave simple ones as ASCII)
3. Generate SVG using box/arrow/txt helpers in a Python script
4. Replace ASCII blocks via string matching
5. Add `.diagram` CSS if not present
6. Verify: `<svg` count == `</svg>` count, marker refs match marker defs
7. Browser-check with `browser_console` → `document.querySelectorAll('svg')` for render dimensions

## Pitfalls

- **Never use f-strings with nested curly braces** in box/arrow/txt helpers (see pitfalls section)
- **Never put single quotes inside triple-quoted SVG content** (e.g. Chinese text with `'超级GPU'` will break the outer triple-quote)
- **SVG viewBox vs width**: Use `viewBox="0 0 720 400"` with `width="100%"` for responsive scaling
- **Marker IDs must be unique per page**: If a page has 2 SVGs sharing SVG_DEFS, the marker IDs are shared (which is fine since they're identical). But if two SVGs define different markers with the same ID, only the first definition takes effect.
