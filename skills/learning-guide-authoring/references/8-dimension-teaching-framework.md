# 8-Dimension Teaching Framework for Technical Knowledge Points

When user requests "深入" content or references this framework, apply these 8 dimensions to EVERY knowledge point in the guide. Each dimension should be a separate h2/h3 section with substantial content (not one-liners).

## The 8 Dimensions

### 1. 背景与动机 (Background & Motivation)
- Why does this technology exist? What problem does it solve?
- Quantify the problem: real numbers, not vague statements
- Example: "PCIe 5.0 x16 = 126 GB/s, but HBM3 = 3,350 GB/s → 27x gap → PCIe is the bottleneck"

### 2. 名字由来 (Name Origin & Etymology)
- Where does the name come from? Break down the English/technical terms
- Historical context: who coined it, when, why
- Example: "InfiniBand = Infinite + Bandwidth, coined in 2000 by Intel/Microsoft/Sun consortium"

### 3. 核心原理 (Core Principles)
- How does it fundamentally work? The "aha" explanation
- ASCII diagrams showing the mechanism
- Life analogies for intuition

### 4. 技术细节 (Technical Details)
- Real specifications, formulas, parameters
- Version history tables with actual numbers
- Architecture diagrams with labeled components
- Comparison tables (before/after, with/without)

### 5. 使用场景 (Use Cases)
- Where is it used in practice?
- Map to specific parallelism strategies (DDP, TP, PP, EP)
- Map to cluster scales (8 GPU → 100K GPU)

### 6. 相似技术对比 (Comparison with Similar Technologies)
- Horizontal comparison table with 3-5 alternatives
- Clear tradeoffs (not just "better/worse")
- Example: InfiniBand vs RoCE vs iWARP — latency, cost, complexity, scale

### 7. 关联技术 (Related Technologies)
- What depends on this? What does this depend on?
- Connection to the overall communication stack
- Example: "NCCL uses GPUDirect RDMA, which requires InfiniBand/RoCE NICs"

### 8. 实际效果 (Real-World Performance)
- Concrete performance numbers (latency, bandwidth, speedup)
- Before/after comparisons
- Training time impact calculations

## Depth Expectations

- Each dimension: 1-3 paragraphs + 1 table or diagram minimum
- Per knowledge point: 15-25KB (not 5-8KB)
- Use `.deep` CSS class for historical/background sections
- Use `.tip` for practical advice
- Use `.warn` for pitfalls
- Use `.exercise` for practice problems

## Quality Checklist

After writing a knowledge point, verify:
- [ ] Background quantifies the problem with real numbers
- [ ] Name origin explains the English term breakdown
- [ ] Core principle has at least one ASCII diagram
- [ ] Technical details include at least one spec table
- [ ] Use cases map to specific scenarios (parallelism strategies, cluster sizes)
- [ ] Comparison table has 3+ alternatives with clear tradeoffs
- [ ] Related technologies section shows dependency chain
- [ ] Performance section has concrete numbers (not "significantly faster")

## Actual Depth Achieved (集合通信 guide, 2026-05-25)

Target per module: 15-25KB. Actual results:
- Deepest: 21KB (01-芯片基础) — had 7 tables, 3 ASCII diagrams, detailed CoWoS/TSV specs
- Good: 16-19KB (02, 06, 08, 09, 10, 11) — had 4-8 tables, 2-4 ASCII diagrams
- Adequate: 13-14KB (03, 04, 05, 07) — had 5-8 tables, 1-2 ASCII diagrams

Key lesson: the "技术细节" and "核心原理" sections are the most impactful for depth. Adding real parameters (e.g., "NVLink 4.0 = 900 GB/s, 18 links × 25 GB/s × 2") and formulas (e.g., "Ring AllReduce time = 2D/B") makes content feel substantially deeper without adding fluff.

CSS class usage:
- `.tip` (blue): practical advice, key insights
- `.warn` (yellow): pitfalls, common mistakes
- `.exercise` (green): practice problems
- `.deep` (purple): historical background, deep technical details, "why it had to be this way"
