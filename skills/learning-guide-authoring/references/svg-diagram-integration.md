# SVG Diagram Integration for HTML Learning Guides

## When to use SVG vs ASCII
- **SVG**: Multi-layer architectures, complex flowcharts (5+ steps with branching), diagrams needing color semantics
- **ASCII**: Small comparison tables (3-5 rows), simple 3-step flows, code-like structures

## SVG Design System (from architecture-diagram skill)
Semantic colors for component types:
| Component Type | Fill (rgba) | Stroke (Hex) |
|:---|:---|:---|
| Frontend/Input | `rgba(8, 51, 68, 0.4)` | `#22d3ee` (cyan) |
| Backend/Process | `rgba(6, 78, 59, 0.4)` | `#34d399` (emerald) |
| Database/Storage | `rgba(76, 29, 149, 0.4)` | `#a78bfa` (violet) |
| Cloud/External | `rgba(120, 53, 15, 0.3)` | `#fbbf24` (amber) |
| Security/Risk | `rgba(136, 19, 55, 0.4)` | `#fb7185` (rose) |
| Message/Bus | `rgba(251, 146, 60, 0.3)` | `#fb923c` (orange) |

## SVG Template
```html
<div class="diagram">
<div class="diagram-title">Title</div>
<svg width="100%" viewBox="0 0 W H" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#475569"/>
    </marker>
  </defs>
  <rect width="W" height="H" fill="#020617" rx="8"/>
  <rect width="W" height="H" fill="url(#grid)" rx="8"/>
  <!-- Components: rounded rects with semantic fills -->
  <!-- Arrows: lines with marker-end="url(#arrow)" -->
</svg>
</div>
```

## Required CSS
```css
.diagram{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin:1.5rem 0;overflow-x:auto}
.diagram-title{color:var(--blue);font-weight:700;font-size:1.05em;margin-bottom:1rem;text-align:center}
```

## Best Practice
Convert only the top 8-12 most complex diagrams per guide. Leave simple comparison tables and 3-step flows as ASCII.
