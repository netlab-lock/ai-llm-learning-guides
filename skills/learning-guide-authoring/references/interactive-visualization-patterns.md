# Interactive HTML Visualization Patterns

Patterns for creating self-contained interactive HTML applications with Canvas animations, charts, and multi-mode interfaces. Distinct from static learning guides — these are interactive tools.

## When to Use

- User wants a "demo" or "visualization" or "interactive tool"
- Needs animations, charts, real-time updates
- Pure front-end, no server required
- Single HTML file with embedded CSS/JS

## Architecture

```
Single HTML file
├── <style> — All CSS (dark theme, responsive)
├── <div> — Tab navigation + content areas
├── <canvas> — For animations (racing, particle effects)
└── <script> — All JavaScript
    ├── Data definitions (tech tree, strategies, etc.)
    ├── Rendering functions (per mode)
    ├── Animation loop (requestAnimationFrame or setInterval)
    └── Event handlers (click, slider, checkbox)
```

## Multi-Mode Tab Interface

```html
<div class="navbar">
  <div class="tab active" onclick="switchTab('mode1',this)">Mode 1</div>
  <div class="tab" onclick="switchTab('mode2',this)">Mode 2</div>
</div>
<div id="mode1View">...</div>
<div id="mode2View" style="display:none">...</div>

<script>
function switchTab(tab, el) {
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  el.classList.add('active');
  ['mode1','mode2'].forEach(v => {
    document.getElementById(v+'View').style.display = v===tab ? 'block' : 'none';
  });
  // Re-render active tab
  if (tab==='mode2') renderMode2();
}
</script>
```

## Canvas Animation Pattern

```javascript
let running = false;
function startAnimation() {
  running = true;
  animate();
}
function animate() {
  if (!running) return;
  // Update state
  // Render frame
  requestAnimationFrame(animate);
  // Or: setTimeout(animate, 50) for slower updates
}
```

## Racing/Progress Bar Pattern

```html
<div class="race-lane">
  <div class="label">Strategy Name</div>
  <div class="bar-container">
    <div class="bar" style="width:0%; background:#58a6ff"></div>
  </div>
  <div class="time">100ms</div>
</div>
```

```javascript
// Animate progress bars
strategies.forEach((s, i) => {
  progress[i] = Math.min(100, progress[i] + speedupFactor * speed);
  barElements[i].style.width = progress[i] + '%';
});
```

## Control Panel Pattern

```html
<div class="controls">
  <div class="control-row">
    <label>Parameter</label>
    <input type="range" id="param" min="1" max="32" value="8" oninput="update()">
    <span class="value" id="paramVal">8</span>
  </div>
</div>
<script>
function update() {
  document.getElementById('paramVal').textContent = document.getElementById('param').value;
  renderAll(); // Re-render all views with new params
}
</script>
```

## Dark Theme CSS Variables

```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --border: #30363d;
  --text: #c9d1d9;
  --text-dim: #8b949e;
  --primary: #58a6ff;
  --success: #3fb950;
  --warning: #d29922;
  --error: #f85149;
}
```

## Pitfalls

1. **Single file size** — Keep under 50KB. If larger, split into multiple HTML files with shared CSS.
2. **Animation performance** — Use `requestAnimationFrame` for smooth 60fps. Use `setTimeout` for slower updates (50-100ms intervals).
3. **Mobile responsiveness** — Use `flex-wrap` and `min-width` for control panels. Test on narrow viewports.
4. **No external dependencies** — Self-contained means no CDN links. Embed Chart.js or vis.js if needed (or use pure Canvas).
5. **Chinese text encoding** — Always use `<meta charset="UTF-8">` and ensure file is saved as UTF-8.

## Example: LLM Inference Racing Visualization

See `D:\学习\llm-inference-racing\index.html` for a complete example with:
- 4 tab modes (tech tree, racing, pipeline, dashboard)
- Canvas-based racing animation
- Interactive sliders and checkboxes
- Real-time performance calculations
- Dark theme with consistent styling
