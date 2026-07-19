# KV Cache: Topic Map & Module Dependency Graph

## Module Dependency Chain

```
01 (基础原理) ──→ 02 (内存模型) ──→ 03 (PagedAttention)
    │                  │                    │
    │                  ▼                    ▼
    │           04 (GQA/MLA) ◄──── 05 (量化)
    │                  │                    │
    │                  ▼                    ▼
    │           06 (驱逐稀疏) ◄──── 07 (分布式)
    │                                      │
    ▼                                      ▼
08 (PD分离) ◄───────────────────── 09 (集群调度)
    │                                      │
    ▼                                      ▼
10 (集合通信) ──────→ 11 (Agent优化)
    │                                      │
    ▼                                      ▼
12 (框架对比) ◄──── 13 (工程调优) ──→ 14 (前沿)
```

## Key Technical Points Per Module

Module 01: Roofline analysis (Decode AI≈1 vs critical 295), Prefill=GEMM vs Decode=GEMV
Module 02: 2×L×2×H×d×S×dtype formula, LLaMA-70B 4K≈5GB KV Cache
Module 03: Block table mapping, CoW for beam search/parallel sampling
Module 04: DeepSeek MLA ~57× compression (34GB→0.5GB), GQA-H=MHA / GQA-1=MQA
Module 05: KIVI (INT2), KVQuant (per-channel), Gear (low-rank+residual)
Module 06: H2O/StreamingLLM/SnapKV — attention sink is key insight
Module 07: TP splits KV heads, PP splits layers (no KV comm needed), Ring Attention for SP
Module 08: Mooncake/Splitwise/DistServe — KV transfer is bottleneck (5GB for 70B@4K)
Module 09: Cache-aware routing, prefix-aware scheduling, swap vs recompute preemption
Module 10: AllReduce for attention output, AllGather for KV heads, NCCL overlap
Module 11: Prefix caching gives 2.96× speedup for Agent system prompts
Module 12: vLLM=PagedAttention, SGLang=RadixAttention, TRT-LLM=PagedKVCache
Module 13: gpu-memory-utilization, max-num-seqs, kv-cache-dtype, monitoring Grafana
Module 14: 20+ papers organized by category, HBM3/CXL hardware trends

## User Context (2026-06)

User works on: cluster scheduling, collective communication, Agent systems
Priority modules: 07, 08, 09, 10, 11 (distributed + scheduling + communication + agents)
Existing scattered KV Cache files in project: 6 files across 01-基础理论, 05-推理优化
New comprehensive guide replaces/supersedes those scattered files.