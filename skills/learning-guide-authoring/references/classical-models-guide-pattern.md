# Classical Model / Historical Guide Pattern

Reusable pattern for creating learning guides that trace the evolution of a technology through its classic models/inventions.

## Scope & Structure

**Flat layout** (recommended for 20-30 models):
```
topic-name/
├── index.html              ← Timeline + learning path + model cards
├── 01-ModelName.html       ← One file per model
├── 02-ModelName.html
├── ...
└── NN-ModelName.html
```

**Organized by phases** (use phase badges in index.html):
- Phase 1: Foundations (oldest, must learn first)
- Phase 2: Breakthroughs (key innovations)
- Phase 3: Maturation (refinements)
- Phase 4: Revolution (paradigm shift)
- Phase 5: Modern era (current state)

## Index Page Design

Include:
1. Hero section with model count, phase count, time span
2. Stats bar (total models, phases, dimensions, year range)
3. Phase sections with color-coded badges
4. Model cards with: year badge, title, description, tags
5. Learning dependency graph (which models must be learned before others)
6. Info box with recommended reading order

## Per-Model File Structure (8-Dimension Framework)

Every model MUST cover all 8 dimensions:
1. **背景与动机** — Why did this model exist? What problem did it solve? Real numbers.
2. **名字由来** — Etymology. English word breakdown. Historical naming.
3. **核心原理** — How it works. ASCII architecture diagrams. Analogies.
4. **技术细节** — Formulas, parameter tables, training details, hyperparameters.
5. **使用场景** — Where is it used? Map to specific products/systems.
6. **相似技术对比** — Comparison table with alternatives.
7. **关联技术** — Links to other models in the guide (cross-references).
8. **实际效果** — Real benchmark numbers. Quantified impact.

**Target file size**: 8-14KB per model. Below 8KB is too shallow.

## Batch Generation Workflow

For 20+ model files:
1. Create index.html first (write_file, ~15-20KB)
2. Write Python scripts to `/tmp/gen_XX.py` — each script generates 2-3 models
3. Each script: extract CSS from existing file → define `hp()` template → call `w()` for each model
4. Run scripts via `terminal("python3 /tmp/gen_XX.py")`
5. After all scripts: audit depth consistency, deepen thin files

**Script template pattern:**
```python
#!/usr/bin/env python3
import os
BASE = "/mnt/d/学习/topic-name"
CSS = open(os.path.join(BASE, "01-ExistingFile.html")).read().split("<style>")[1].split("</style>")[0]

def hp(title, prev, nxt, nav, body):
    # Generate complete HTML with nav, container, footer
    ...
def w(path, content):
    with open(os.path.join(BASE, path), "w") as f: f.write(content)
    print(f"  {path} ({os.path.getsize(...):,}B)")

# Model content as raw strings (r"""...""")
w("01-Model.html", hp("Title", None, "02.html", "Nav", r"""...body..."""))
w("02-Model.html", hp("Title", "01.html", "03.html", "Nav", r"""...body..."""))
```

## Depth Consistency Pitfall

**CRITICAL**: First 2-3 models tend to be significantly deeper (13-14KB) than later ones (6-7KB) because:
- The agent gets more "efficient" (shorter content generation)
- Content generation fatigue sets in
- Later models may share context with earlier detailed ones

**After creating all models, ALWAYS audit depth:**
```bash
cd "/mnt/d/学习/topic-name/"
for f in *.html; do sz=$(wc -c < "$f"); printf "%s: %dKB\n" "$f" "$((sz/1024))"; done
```

**If min/max ratio > 0.5**: deepen the thinnest 3-5 files with a dedicated script.
Target: all models within 60-100% of the deepest model's size.

## Navigation & Cross-References

Every model file must have:
- Top nav bar: ← Previous | Current Title | Next →
- Footer: link back to index.html
- Cross-references to related models within the "关联技术" section

## CSS Consistency

Extract CSS from the first created file to ensure all files match:
```python
CSS = open("existing.html").read().split("<style>")[1].split("</style>")[0]
```

Use dark theme (#0d1117 background, #58a6ff headings, #c9d1d9 text).
Standard classes: `.tip`, `.warn`, `.exercise`, `.deep`, `.ascii`, `.formula`
