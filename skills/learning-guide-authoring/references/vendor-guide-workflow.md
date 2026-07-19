# Vendor Guide 8-Chapter Standard Structure

Standard chapter layout for international LLM vendor guides (OpenAI, Anthropic, Google, Meta, Mistral, etc.):

| # | Filename | Content |
|---|----------|---------|
| 01 | 概述与演进时间线.html | Company history, founding team, model evolution timeline, funding |
| 02 | 核心架构设计.html | Dense/MoE architecture, attention mechanism, tokenization, scaling strategy |
| 03 | 最新模型详解.html | Latest model series detailed specs, capabilities, benchmarks |
| 04 | 推理能力与Thinking.html | Reasoning model capabilities, thinking mode, test-time compute |
| 05 | 后训练与对齐.html | SFT/RLHF/DPO pipeline, safety training, red-teaming |
| 06 | 系统工程与部署.html | API design, pricing, developer tools, deployment options |
| 07 | 性能评估与对比.html | Benchmark results, LMSYS ranking, cross-vendor comparison |
| 08 | 生态与学习资源.html | Key papers, community, learning paths, ecosystem tools |

Each file includes:
- Fixed nav sidebar linking all 8 chapters (current page marked `class="active"`)
- Table of contents (`.toc`)
- Callout boxes (`.co .co-tip/.co-warn/.co-info`)
- Comparison tables
- SVG diagram (architecture, timeline, or decision tree)
- Exercise section (3-4 questions)
- Footer with page identification

Index page (`index.html`): Overview, chapter list with descriptions, knowledge map SVG, link to parent `../index.html`.

## CSS Template
Use `templates/vendor-guide-8ch.css` — single-line dark theme CSS. Copy into `<style>` block.

## Parallel Delegation Pattern
For batch-creating 8+ HTML files, use `delegate_task` with `role="leaf"` and `toolsets=["file"]`:
- Batch 2-3 providers per delegation (e.g., OpenAI + Anthropic simultaneously)
- Each delegation creates 9 files (8 content + 1 index)
- Pass the full CSS template inline in the delegation prompt
- Pass the nav sidebar HTML in full so each file gets consistent navigation
- Typical output: 9 files × ~8-10KB each per provider per delegation

## Pitfalls
1. **f-string curly braces**: NEVER use Python f-strings for HTML content containing `{r_1}`, `{t_i}`, CSS `{}  `. The curly braces get interpreted as Python variables. Use `write_file` tool directly instead of `execute_code` with f-strings for HTML with math notation.

2. **File size consistency**: Aim for 120-200 lines per file. The CSS is compressed (single line), so actual line count will be lower than expected. Content quality matters more than line count.

3. **Nav sidebar state**: Always mark the current file with `class="active"` in the nav. Don't forget this — it's the most visible UI bug if missed.

4. **Index update**: After creating a new topic directory, always update:
   - The parent directory's `index.html` (add a card/grid entry)
   - The root `index.html` (if it's a new top-level module)
