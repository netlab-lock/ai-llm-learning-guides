# Unified Chapter Template for LLM Provider Surveys

Standard 11-chapter structure for systematic learning guides covering multiple LLM providers.

## Chapter Structure

| # | Title | Content Scope | Key Topics |
|---|-------|--------------|------------|
| 01 | 公司背景与模型演进 | Company history, founding, timeline | Founders, funding, milestones, model generations |
| 02 | 核心架构设计 | Base Transformer variant | Dense/MoE, FFN design, model scales, config tables |
| 03 | 注意力机制创新 | Attention mechanism specifics | GQA/MLA/Linear Attention, KV cache, RoPE variants |
| 04 | 预训练策略与数据工程 | Pre-training pipeline | Data composition, quality filtering, multi-stage, scaling law |
| 05 | 后训练与对齐 | Post-training alignment | SFT, RLHF, DPO, GRPO, CISPO, Sequential RL, reward models |
| 06 | 推理能力与长上下文 | Reasoning & long context | Chain-of-thought, context extension (32K→1M), RoPE extrapolation |
| 07 | 多模态与跨模态 | Multimodal capabilities | Vision encoder, audio, video, early/late fusion strategies |
| 08 | 系统工程与部署优化 | Infrastructure & deployment | Distributed training, quantization, vLLM/SGLang, API architecture |
| 09 | 性能评估与基准测试 | Benchmarks & evaluation | MMLU, HumanEval, MATH, C-Eval, head-to-head comparison tables |
| 10 | 应用场景与生态系统 | Products & ecosystem | API platform, consumer products, open source, enterprise solutions |
| 11 | 论文精读与学习资源 | Papers & learning path | Core papers with summaries, reading order, practice projects |

## Per-Chapter Content Guidelines

### 01-公司背景与模型演进
- Company overview card (name, founded, founder, positioning)
- Timeline table (year → milestone)
- Key stats (total funding, employee count, open source contributions)

### 02-核心架构设计
- Model configuration table (params, layers, hidden dim, heads, context)
- MoE config if applicable (total params, active params, expert count)
- Architecture comparison vs baseline (GPT, Llama)
- ASCII architecture diagram

### 03-注意力机制创新
- Mathematical formulation of the attention variant
- Comparison table: MHA vs GQA vs MQA vs MLA vs Linear Attention
- KV cache size calculations
- Evolution across model generations

### 04-预训练策略与数据工程
- Data composition breakdown (web, code, math, books, multilingual)
- Quality filtering pipeline (dedup, scoring, filtering stages)
- Training hyperparameters (learning rate, batch size, warmup)
- Scaling law findings specific to this provider

### 05-后训练与对齐
- RL algorithm used (GRPO, CISPO, PPO, DPO, Sequential RL)
- Algorithm flow with formulas
- SFT data construction methodology
- Comparison table: this provider's method vs others
- Safety alignment and red-teaming approach

### 06-推理能力与长上下文
- Context extension technique (YaRN, NTK, RoPE extension)
- Reasoning model details (thinking mode, CoT)
- Long document benchmarks (RULER, Needle-in-a-Haystack)
- Comparison of context windows across providers

### 07-多模态与跨模态
- Vision encoder architecture (SigLIP, InternViT, custom)
- Fusion strategy (early, late, hybrid)
- Supported modalities (text, image, audio, video)
- Multimodal benchmark results

### 08-系统工程与部署优化
- Training infrastructure (GPU cluster, framework)
- Parallelism strategy (data, tensor, pipeline, expert)
- Inference optimization (quantization, speculative decoding, continuous batching)
- Local deployment guide (Ollama, vLLM, GGUF)

### 09-性能评估与基准测试
- Comprehensive benchmark table across all model sizes
- Head-to-head comparison with competitors
- Chinese-specific benchmarks (C-Eval, CMMLU)
- Evaluation methodology discussion

### 10-应用场景与生态系统
- API platform details (URL, pricing, rate limits)
- Consumer products
- Open source releases (HuggingFace, ModelScope)
- Developer tools and frameworks

### 11-论文精读与学习资源
- Core papers with 2-3 sentence summaries
- Recommended reading order
- External resources (GitHub, blog, documentation)
- Self-assessment checklist
- Practice project suggestions

## CSS Standard (Dark Theme)

All chapters use identical CSS variables:
```css
:root {
  --bg: #0d1117;
  --surface: #161b22;
  --surface2: #1c2128;
  --border: #30363d;
  --text: #c9d1d9;
  --text2: #8b949e;
  --accent: #58a6ff;
  --green: #3fb950;
  --orange: #d29922;
  --red: #f85149;
  --purple: #bc8cff;
}
```

## Navigation Pattern

Each chapter has:
- Top nav bar (sticky): `← prev | chapter title | next →`
- Bottom nav: prev/next links + link to brand index.html
- Brand index.html: chapter-list with all chapters listed

## Batch Expansion Results (May 2026)

Expanded 16 Chinese LLM providers from 1-5 chapters to 11-13 chapters each.
Total: 221 HTML files across 16 vendor directories.
Method: 3 concurrent delegate_task subagents, each handling one vendor.
Most vendors completed in 1 batch (3 vendors per round, ~200-600s each).
Some vendors needed 2 rounds due to timeouts.
