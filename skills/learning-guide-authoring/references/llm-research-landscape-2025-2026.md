# LLM Research Landscape 2025-2026

Knowledge map for creating LLM learning guides. Verified via web search on 2026-05-15.

## Layer 1: Foundations

### Tokenization
- BPE (Byte Pair Encoding): GPT series. Merge frequent char pairs.
- WordPiece: BERT, uses likelihood instead of frequency.
- SentencePiece: No pre-tokenization needed, byte-level BPE, handles any language/emoji.
- Impact: affects multilingual ability, vocab size, inference cost.

### Embedding
- Token → high-dimensional vector (768 to 12288 dims)
- Semantically similar tokens cluster in vector space.

## Layer 2: Transformer Architecture

### Self-Attention
- `Attention(Q, K, V) = softmax(QK^T / √d_k) · V`
- Q=Query ("what am I looking for?"), K=Key ("what do I offer?"), V=Value ("what I actually provide")

### Multi-Head Attention
- Multiple parallel Q/K/V groups (e.g., 96 heads), each captures different relationships (syntax, semantics, position).

### Positional Encoding
- Original: sinusoidal/cosine fixed encoding.
- Modern LLM: **RoPE** (Rotary Position Embedding) — encodes position as rotation angles.
- Variants for long context: YaRN, NTK-aware.

### FFN (Feed-Forward Network)
- 2/3 of total parameters live here.
- Activation evolution: ReLU → GELU → **SwiGLU** (modern standard).

### Layer Normalization
- Pre-Norm (modern): normalize before Attention/FFN.
- **RMSNorm**: simplified LayerNorm, faster (no mean centering).

### Transformer Block (modern)
```
Input → RMSNorm → Multi-Head Attention → Residual
      → RMSNorm → FFN (SwiGLU) → Residual → Output
```

### Decoder-Only
- All modern LLMs use decoder-only with causal mask.
- Encoder-Decoder (T5) and Encoder-Only (BERT) not mainstream for generation.

## Layer 3: Pretraining

### Objectives
- **CLM** (Causal Language Modeling): autoregressive next-token prediction. All modern LLMs.
- **MLM** (Masked Language Modeling): BERT-style, not used in modern LLMs.

### Training Data
- Sources: Common Crawl, books, code, academic papers, Wikipedia, GitHub.
- Scale: trillions of tokens (DeepSeek-V3: 14.8T tokens).
- Quality >> Quantity (Phi series proved curated small data works).
- Pipeline: crawl → clean → dedup → filter → mix ratios.
- Tools: NVIDIA NeMo Curator (GPU-accelerated curation).
- "Garbage In, Hallucination Out" — data quality directly determines model quality.

### Optimizer & Training
- **AdamW**: standard optimizer (Adam + weight decay).
- LR schedule: **Warmup + Cosine Decay** (linear warmup then cosine curve).
- Gradient clipping: prevents gradient explosion.
- FLOPs: ≈ 6 × params × training_tokens.
- New research (2025): "Beyond Cosine Decay", "Simplifying Adam: Bias Correction Debunked".

## Layer 4: Post-Training (Alignment)

### Evolution (2026 verified via search)
```
SFT → RLHF(PPO) → DPO → ORPO/SimPO → GRPO → RLVR
```

### SFT (Supervised Fine-Tuning)
- Train on (instruction, response) pairs.
- Teaches model to follow instructions vs. just continue text.

### RLHF (Reinforcement Learning from Human Feedback)
- Step 1: SFT → Step 2: Train Reward Model (RM) → Step 3: PPO with RM signal.
- Problems: needs RM + Value Model, expensive, unstable.
- **Status (2026): Being replaced** — "The Death of RLHF" (Towards AI, 2025).

### DPO (Direct Preference Optimization, 2023)
- Skip RM training, directly optimize on preference data.
- Mathematically equivalent to RLHF, much simpler.
- Variants: ORPO, SimPO.

### GRPO (Group Relative Policy Optimization)
- DeepSeek proposal, **new standard in 2025-2026**.
- No critic/value model needed, uses group-relative ranking.
- Simpler, more stable, cheaper than PPO.
- Unsloth has complete GRPO training tutorials.

### RLVR (Reinforcement Learning with Verifiable Rewards)
- Uses auto-verifiable tasks as reward signal (math correctness, code test cases).
- No human annotation needed, fully automated.
- Core technique for training reasoning models (DeepSeek-R1).

### Alignment Pretraining (new direction)
- Inject alignment data during pretraining, not just post-training.
- May solve "inner alignment" problem.
- arxiv 2601.10160: alignment priors persist through post-training.

## Layer 5: Inference & Usage

### KV Cache
- Cache computed K/V to avoid recomputation during autoregressive generation.
- Problem: huge VRAM for long sequences.
- Optimization: FP8/INT8 KV Cache quantization (2x savings, minimal quality loss).
- **PagedAttention** (vLLM): virtual memory management for KV Cache.

### Prompt Engineering
- **Zero-shot**: no examples, direct question.
- **Few-shot**: provide examples before question (In-Context Learning).
- **Chain-of-Thought (CoT)**: "Let's think step by step..." to guide reasoning.
- **System Prompt**: set model role and behavior rules.

### RAG (Retrieval-Augmented Generation)
- Pipeline: Chunk documents → Embed → Store in vector DB → Retrieve relevant chunks → Feed to LLM with query.
- Vector DBs: FAISS, Pinecone, Chroma.
- **2026 debate**: With 10M token context (Llama 4), is RAG still needed?
- **Consensus**: Yes — cost, real-time updates, data freshness.
- RAG is "default architecture for private-data QA" in 2026.

### Hallucination
- Definition: model generates plausible but factually incorrect content.
- Detection: uncertainty quantification, external knowledge verification, self-consistency.
- Mitigation: RAG, RLHF/RLVR alignment, chain-of-thought reasoning.

## Layer 6: Efficiency Optimization

### PEFT (Parameter-Efficient Fine-Tuning)
- **LoRA**: add low-rank matrix ΔW = A·B alongside original weights, train only A and B (~1000x fewer params).
- **QLoRA**: LoRA + 4-bit quantized base model (fine-tune 65B on single consumer GPU).
- **Spectrum**: newer HuggingFace PEFT method.
- HuggingFace PEFT library: unified interface.

### Quantization
- **GPTQ**: post-training quantization, needs calibration data.
- **AWQ**: protects important weight channels, better accuracy than GPTQ.
- **GGUF**: llama.cpp format, CPU/GPU hybrid inference.
- Levels: FP16 → INT8 → INT4.

### FlashAttention
- Solves O(n²) memory/computation bottleneck of attention.
- Core: tiling (chunked computation), avoids materializing full n×n matrix.
- Effect: memory O(n²) → O(n), speed 2-4x.

### Inference Engines
- **vLLM**: PagedAttention + continuous batching. v0.19.1 (2026.04), 45k+ stars. Production standard.
- **SGLang**: RadixAttention + structured generation. v0.5.13 (2026.06), 16k+ stars. Most actively updated framework in 2026 (DFlash speculative decoding, GB300 NVL72 25x, JAX/TPU support, Diffusion generation).
- **TensorRT-LLM**: NVIDIA official optimization. Best raw performance on NVIDIA GPUs.
- **NVIDIA Dynamo** (NEW 2026.03 GA): Datacenter-scale distributed inference orchestrator. NOT a replacement for vLLM/SGLang — sits ABOVE them. Core: disaggregated prefill/decode, KV-cache-aware routing, multi-tier caching, autoscaling. 30x throughput on Blackwell, 7x on H100. Successor to Triton for LLM serving.
- **TGI** (⚠️ Maintenance mode 2026): HuggingFace officially recommends migrating to vLLM/SGLang/llama.cpp.
- **Mooncake** (NEW 2026.02 OSS): Moonshot AI (Kimi) distributed KV Cache platform. Transfer Engine + Mooncake Store. Integrated into SGLang and vLLM-Omni.
- **MLX** (NEW): Apple Silicon deep optimization. Unified memory architecture. Often faster than llama.cpp on Mac M4 Pro/Max.
- **Speculative Decoding**: small model drafts, large model verifies. SGLang's DFlash + Spec V2 is 2026 state-of-the-art.
- **Continuous Batching**: new requests join at any time.
- **Key 2026 trend**: Disaggregated Prefill/Decode (PD分离) — separate compute-intensive prefill from memory-intensive decode onto different GPU pools. Dynamo orchestrates across nodes.

### Distributed Training
- **Data Parallel (DP)**: each GPU has full model, different data. FSDP/ZeRO shard optimizer states.
- **Tensor Parallel (TP)**: split individual matrix ops across GPUs. Best for single-node multi-GPU (NVLink).
- **Pipeline Parallel (PP)**: different layers on different GPUs. Best for cross-node.
- **3D Parallel**: DP + TP + PP combined.
- Frameworks: DeepSpeed, Megatron-LM, FSDP.

## Layer 7: Frontiers (2024-2026, search-verified)

### 7.1 Reasoning Models (biggest paradigm shift)
- OpenAI o1 (2024.09), o3-mini (2025.01)
- DeepSeek-R1 (2025.01): pure RL (GRPO) trained reasoning, open-sourced
- Paper: "Scaling LLM Test-Time Compute Optimally" (Snell 2024)
- PRM (Process Reward Model) vs ORM (Outcome Reward Model)
- System-1 (fast) vs System-2 (slow) thinking

### 7.2 MoE (Mixture of Experts)
- DeepSeek-V4-Pro (2026.04): 1.6T total, 49B active, MIT license, 1M context
- Core: routing network selects few experts per token
- Challenge: load balancing, expert collapse

### 7.3 Long Context
- Llama 4: 10M tokens; DeepSeek-V4: 1M tokens
- Tech: RoPE extrapolation, YaRN, Ring Attention
- Debate: long context vs RAG

### 7.4 Multimodal
- GPT-4o replaced GPT-4 (2025.04)
- Gemini 3, Kimi K2.5, InternVL
- Trend: native multimodal pretraining (not post-hoc vision encoder)

### 7.5 Agents
- MCP (Model Context Protocol): Agent ↔ Tool standard (Anthropic)
- A2A (Agent-to-Agent): Agent ↔ Agent protocol (Google)
- Evolution: 2024 action → 2025 systems → 2026 specialization
- Kimi K2.6: Agent Swarm (multi-agent collaboration)

### 7.6 Scaling Laws (new directions)
- NeurIPS 2025: "Gemstones" (multi-faceted scaling), "Power Lines" (weight decay/batch size scaling)
- Training scaling + inference scaling dual track
- Training cost entering $1B+ range (2025)

## Latest Model Landscape (as of 2026-05)

| Model | Org | Params | Active | Context | Key Feature |
|-------|-----|--------|--------|---------|-------------|
| DeepSeek-V4-Pro | DeepSeek | 1.6T MoE | 49B | 1M | MIT open-source, 81% SWE-bench |
| GPT-5.4 | OpenAI | - | - | - | Closed |
| Claude 4.5 | Anthropic | - | - | - | Closed |
| Gemini 3 | Google | - | - | - | Multimodal |
| Qwen3 | Alibaba | 235B | - | - | Multilingual |
| Llama 4 | Meta | - | - | 10M | Longest context |
| Kimi K2.6 | Moonshot | - | - | 256K | Agent Swarm |

## Conference Highlights (2024-2025)

- NeurIPS 2024: VAR, Rho-1, Mamba-Llama distillation
- NeurIPS 2025: "Gemstones" scaling laws, Oxford benchmark review (only 16% of 445 LLM benchmarks do statistical testing)
- EMNLP 2024 Best Demo: MarkLLM (LLM watermarking)
- ACL 2025: MT, narrative understanding, coreference, LLMs

## Sources

All information verified via DuckDuckGo web search on 2026-05-15.
Key sources:
- HuggingFace (DeepSeek-R1, model cards)
- TechCrunch (o3-mini launch)
- Towards AI ("Death of RLHF")
- NxCode, Twin AI, NVIDIA NIM (DeepSeek-V4)
- Google DeepMind (Gemini 3)
- Aitude ("Modern AI Agents In 2026")
- MCP official docs
- arxiv (alignment pretraining, scaling laws)
- Unsloth (GRPO tutorials)
