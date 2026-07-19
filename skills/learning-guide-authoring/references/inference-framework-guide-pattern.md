# Inference Framework / Tool Deep-Dive Guide Pattern

When creating a deep-dive guide for a specific inference framework (Dynamo, vLLM, SGLang, TensorRT-LLM, Triton, etc.), follow this validated pattern.

## Structure (flat, 10-12 files)

```
D:\学习\<Framework>-深度解读\
├── index.html              ← Overview, stats cards, roadmap, resource links
├── 01-概述与定位.html       ← What/why/where in the stack
├── 02-核心架构.html         ← Components, data flow, ASCII diagrams
├── 03-核心特性1.html        ← Deepest technical topic (e.g., disaggregated serving)
├── 04-核心特性2.html        ← Second key feature (e.g., KV cache management)
├── 05-核心特性3.html        ← Third key feature (e.g., smart routing)
├── 06-核心特性4.html        ← Fourth key feature (e.g., transfer library)
├── 07-性能基准.html         ← Benchmarks, comparisons with alternatives
├── 08-硬件协同.html         ← How it leverages specific hardware (optional)
├── 09-部署实战.html         ← Docker/K8s/cloud, config, monitoring, troubleshooting
└── 10-生态与未来.html       ← Version history, ecosystem map, trends
```

Use **flat layout** (not subdirectories) for single-framework guides. Subdirectory layout is for broad multi-vendor surveys.

## Research Pattern (3 parallel subagents)

```python
delegate_task(tasks=[
    {"goal": "Search for '<framework> architecture components 2025' via ddgs CLI", "toolsets": ["terminal"]},
    {"goal": "Search for '<framework> github official documentation' via ddgs CLI", "toolsets": ["terminal"]},
    {"goal": "Search for '<framework> benchmark performance vs alternatives' via ddgs CLI", "toolsets": ["terminal"]},
])
```

Then fetch 3 key pages for deep detail:
1. **Official blog post** — announcement, key innovations, performance numbers
2. **GitHub README** — architecture overview, features list, deployment info
3. **Official docs** — design docs, API reference, configuration

## Content Checklist per Chapter

Each chapter MUST have:
- [ ] 通俗类比 (callout-tip) — everyday analogy for the core concept
- [ ] ≥2 ASCII diagrams — architecture, data flow, or comparison
- [ ] ≥1 comparison table — with concrete numbers
- [ ] 代码块 (if applicable) — config snippets, API examples
- [ ] 关键洞察 (highlight box) — 3 non-obvious insights
- [ ] 常见误区 (callout-warn) — 2-3 misconceptions
- [ ] 深度思考题 — L1/L2/L3 questions

## Index Page Must Include

1. **Stats grid** — 4 key performance numbers (e.g., "30x", "7x")
2. **"What is X?"** section — 2-3 sentence definition with callout-tip analogy
3. **Core capabilities table** — feature/说明/effect columns
4. **Learning roadmap** — card grid with all chapters
5. **Reference resources** — GitHub, official blog, docs links

## Depth Levels: Standalone Deep-Dive vs Chapter-in-Project

**Standalone deep-dive** (e.g., D:\学习\NVIDIA-Dynamo深度解读\): 10-12 files, each 200-400 lines. Total 2000-4000 lines.

**Framework chapter within a broader project** (e.g., 08-主流框架/01-vLLM.html): SINGLE file, but must be 400-500 lines / 20-30KB. This is the user's expectation — they rejected 185-line files as "泛泛而谈" (shallow). Each chapter must contain:
- 8+ H2 sections, 15+ H3 subsections
- 8+ code blocks (real config/API examples, not pseudocode)
- 8+ architecture diagrams (SVG preferred, see below)
- Internal mechanism deep-dives (math formulas, algorithm pseudocode, data structures)
- Production tuning parameter tables (with defaults, effects, recommendations)
- Pitfall/troubleshooting tables
- 4-5 interview Q&A (class=box purple)
- Decision framework for "when to use this vs that"

**Rule of thumb**: If the file is <300 lines or <15KB, it's too shallow for a framework chapter.

## Diagram Standard: SVG-First (2026-06)

User explicitly requested SVG over ASCII. Use inline SVG with dark theme for all architecture diagrams in learning guides.

**Color semantics** (adapt from architecture-diagram skill):
- cyan (#22d3ee) = API/Server/Frontend layer
- emerald (#34d399) = Core engine/backend components
- violet (#a78bfa) = Memory/Cache/Database components
- amber (#fbbf24) = GPU/Hardware/Cloud layer
- rose (#fb7185) = Highlights/Warnings/Security
- slate (#94a3b8) = Secondary text, borders

**SVG component style**:
- Rounded rectangles (rx=6), semi-transparent rgba fills, 1.5px stroke
- viewBox="0 0 900 N" (width 900, height N per content)
- Font: 'Courier New', monospace (inline in SVG)
- Arrow markers via SVG defs
- Wrap in `<div class="diagram" style="padding:0;overflow:hidden">` for container styling

**Subagent pattern for SVG conversion** (validated 2026-06):
```
delegate_task(tasks=[
    {"goal": "Read <file>, replace all class=diagram ASCII blocks with inline SVG. Write back.", "toolsets": ["file", "terminal"]},
    ...  # up to 3 files in parallel
])
```
Pass the color semantics and component style in the context. Each subagent reads the file, generates SVGs via Python script, writes back. 3 parallel subagents can convert ~30 diagrams in ~5-10 minutes.

## Pitfalls

- **Don't just copy training data** — frameworks evolve fast. Always web search for latest version, release notes, and benchmarks. Training data may be 6-12 months stale.
- **Position correctly** — clarify whether the tool is an engine, orchestrator, library, or platform. Many users confuse Dynamo (orchestrator) with vLLM (engine).
- **Include decision tree** — users need "when to use X vs Y", not just feature lists. Add a decision tree in the benchmarks chapter.
- **Benchmark honesty** — always note what contributes to performance numbers (hardware vs software vs combination). A "50x" number may include 10x from hardware, 2x from disaggregation, 1.5x from routing, etc.
- **Shallow framework chapters** — a 185-line / 9KB file is NOT a "deep guide". User will reject it as "泛泛而谈". Target 400+ lines / 20KB+ per framework chapter.
- **ASCII diagrams when SVG is expected** — user considers ASCII "简陋" (crude). Always use SVG for architecture diagrams in learning guides.

## Auditing & Updating Existing Inference Framework Guides

When asked to "检查推理框架部分" or "评判做得怎么样", follow this workflow:

### Step 1: Locate existing content
```bash
search_files(path=base_dir, pattern="*推理*", target="files")
search_files(path=base_dir, pattern="*infer*", target="files")
search_files(path=base_dir, pattern="*vLLM*", target="files")
search_files(path=base_dir, pattern="*部署*", target="files")
```

### Step 2: Read key files and evaluate
Read the framework overview (00-框架总览), comparison table (06-框架对比选型), and individual framework files. Evaluate:
- File timestamps (how stale?)
- Stars/version numbers (outdated?)
- Framework status changes (deprecated? maintenance mode?)
- Missing new frameworks that emerged since creation

### Step 3: Web research for current state
```bash
ddgs text -k "LLM inference framework 2026 comparison" -m 10
ddgs text -k "<framework> 2026 latest version features" -m 6
```

### Step 4: Gap analysis matrix
Build a table: | Gap | Priority | Action |
- P0: Status changes (deprecated frameworks still recommended), missing major frameworks
- P1: Version/Stars updates, new features for existing frameworks
- P2: New frameworks, expanded comparisons

### Step 5: Execute updates
- **New files**: write_file for entirely new framework pages
- **Status updates**: patch the framework description (e.g., "⚠️ 维护模式")
- **Version updates**: patch the info box with latest version/stars
- **New features**: patch to add a new section (e.g., "2026年重大更新")
- **Comparison tables**: patch to add rows for new frameworks
- **Decision trees**: patch to add new options and remove deprecated ones

### Step 6: Fix navigation links (CRITICAL PITFALL)
When inserting a new numbered file (e.g., 07-NVIDIA-Dynamo.html) into an existing sequence:

```
BEFORE: ... → 06-框架对比选型 → 返回首页
AFTER:  ... → 06-框架对比选型 → 07-NVIDIA-Dynamo → 返回首页
```

Required changes:
1. Previous file (06): patch `nav-bottom` right link to point to new file
2. New file (07): left link = previous file, right link = 返回首页
3. Check README.html and 00-总览 for card grids that need new entries

**Pitfall**: Don't accidentally make a file's nav link point to itself. After patching, verify old_string didn't create a self-reference.

### 2026-06 Inference Framework Landscape (verified via web search)

| Framework | Status | Version | Stars | Key 2026 Development |
|-----------|--------|---------|-------|---------------------|
| vLLM | Active | v0.19.1 | 45k+ | Mature, production standard |
| SGLang | Active (most活跃) | v0.5.13 | 16k+ | DFlash, GB300 25x, JAX TPU, Diffusion |
| TensorRT-LLM | Active | - | 10k+ | NVIDIA GPU deep optimization |
| llama.cpp | Active | - | 75k+ | Local/edge/CPU standard |
| NVIDIA Dynamo | **NEW** (2026.03 GA) | 1.0 | 15k+ | Datacenter orchestration, PD disaggregation |
| TGI | **⚠️ Maintenance mode** | - | 9k+ | HF recommends migrating to vLLM/SGLang/llama.cpp |
| Ollama | Active | - | 100k+ | Local dev standard |
| Mooncake | **NEW** (2026.02 OSS) | - | 5k+ | Distributed KV Cache (Moonshot AI/Kimi) |
| MLX | **NEW** | - | 20k+ | Apple Silicon deep optimization |
| LMDeploy | Active | - | 6k+ | Chinese model optimization |

**Key architectural trend**: Disaggregated Prefill/Decode (PD分离) is the dominant 2026 pattern. Dynamo orchestrates it across nodes; Mooncake provides the KV transfer layer; SGLang/vLLM implement it at the engine level.
