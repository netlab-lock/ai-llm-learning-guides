# LLM Inference Optimization Techniques — Knowledge Bank

Collected from web research (2026-05-21) and conversation context. For creating deep-dive learning guides on LLM inference hot technologies.

## Taxonomy (Full Landscape)

```
┌──────────────────────────────────────────────────────┐
│                  调度层 (Scheduling)                   │
│  ① 连续批处理 — 每步动态替换请求                         │
│  ② Chunked Prefill — 把长prompt切成块，避免阻塞解码       │
│  ③ Prefill-Decode 分离 — DistServe/Splitwise/POD-Attn  │
├──────────────────────────────────────────────────────┤
│                  内存层 (Memory)                       │
│  ④ PagedAttention — KV Cache 按页管理，消除内存碎片        │
│  ⑤ Prefix Caching — 相同前缀的请求共享 KV Cache           │
│  ⑥ KV Cache 压缩/量化 — TurboQuant, FP8, H2O, StreamingLLM│
├──────────────────────────────────────────────────────┤
│                  计算层 (Compute)                      │
│  ⑦ FlashAttention — IO-aware 注意力计算                  │
│  ⑧ 投机解码 — 小模型草稿 + 大模型验证                     │
│  ⑨ 量化 (FP8/INT4/MXFP) — 降低计算和内存开销              │
├──────────────────────────────────────────────────────┤
│                  并行层 (Parallelism)                  │
│  ⑩ Tensor Parallelism — 单层切分到多卡                   │
│  ⑪ Pipeline Parallelism — 层间切分到多卡                 │
│  ⑫ Context Parallelism — 序列维度切分到多卡               │
│  ⑬ Expert Parallelism — MoE 专家切分到多卡               │
└──────────────────────────────────────────────────────┘
```

## Key Disambiguation (容易混淆的概念对)

### Chunked Prefill vs Context Parallelism
| | Chunked Prefill | Context Parallelism |
|---|---|---|
| 层面 | 调度策略 | 并行策略 |
| 解决什么 | 长prompt阻塞decode | 序列太长单卡算不下 |
| 粒度 | 时间片交替 | 序列维度切分到多卡 |
| 需要多卡？ | 不需要 | 必须多卡 |
| 通信开销 | 无 | 有（卡间交换KV） |

### Prefill vs Decode 计算特征
```
Prefill (处理输入):  计算密集，算力瓶颈，GPU 利用率高
Decode  (生成输出):  访存密集，带宽瓶颈，GPU 利用率低
```
这两种阶段特征完全不同，混在一起互相干扰。DistServe/Splitwise 的核心洞察。

### Continuous Batching vs Static Batching
- Static: 攒满一批，等最慢的完成，才能下一批。木桶效应。
- Continuous: 每步(iteration-level)动态替换完成的请求。回转寿司。
- 效果: GPU利用率 30-60% → 80-95%, 吞吐量提升 2-5x

## Technique Details

### 1. Continuous Batching (连续批处理)
- 问题: 静态批处理的木桶效应 — 短请求被长请求拖累，完成后的槽位空闲
- 方案: 每个iteration做调度决策，完成的请求立刻让位给新请求
- 效果: GPU利用率 80-95%, 吞吐量 2-5x
- 场景: 所有在线推理服务（API、聊天、代码生成），不适用单用户独占
- 实现: vLLM, TensorRT-LLM, SGLang 全部内置

### 2. Chunked Prefill (分块预填充)
- 问题: 长prompt的prefill霸占GPU，decode请求被阻塞
- 方案: 把prompt切成chunk，和decode交替执行
- 关键: 不是并行，是时间片交替

### 3. Prefill-Decode 分离
- 问题: Prefill(计算密集)和Decode(访存密集)特征不同，混跑互相干扰
- 方案: 拆到不同GPU上
- 论文: DistServe (2024), Splitwise, POD-Attention (ASPLOS 2025), TetriInfer
- POD-Attention: 实现prefill和decode完全重叠

### 4. PagedAttention
- 问题: KV Cache内存碎片化，每个请求申请连续大块
- 方案: 类似OS虚拟内存，按页管理KV Cache
- 实现: vLLM核心创新

### 5. FlashAttention
- 版本: FA-1 (A100), FA-2 (2x faster), FA-3 (H100, FP8+异步)
- 核心: Tiling分块 + 在线softmax，O(n²)显存→O(n)
- 精确: 数学等价，非近似

### 6. 注意力变体 (GQA/MQA/MLA)
- MHA: 每个头独立KV (原始)
- MQA: 所有头共享KV (激进压缩，质量下降)
- GQA: 分组共享KV (平衡方案，LLaMA2+标准)
- MLA: 低秩投影压缩KV (DeepSeek-V2+, ~14x压缩)

### 7. Speculative Decoding (投机解码)
- Draft Model法: 小模型猜测 + 大模型验证
- Medusa: 在目标模型上加额外预测头
- EAGLE 1/2/3: 在特征空间预测(非token空间)，更快更准
- Self-Speculative: 用模型自身的部分层做草稿(Fractal-LLM)
- Tree Verification: 树状验证多个候选
- BeaGLE (2025): Cross-Attention投机解码

### 8. Quantization (量化)
- PTQ: GPTQ (需校准数据), AWQ (保护重要通道)
- 格式: GGUF (llama.cpp), FP8, MXFP (Microscaling)
- TurboQuant (Google, 2026.03): PolarQuant + QJL, ~3bit, 6x压缩, 近零精度损失
  - 旋转(Hadamard变换) → 标量量化 → 1bit残差校正
  - 适用于KV Cache压缩和向量搜索
  - llama.cpp讨论#20969: WHT + QJL + MSE 方案
  - 预计2026末/2027初集成

### 9. KV Cache 压缩
- H2O (Heavy-Hitter Oracle): 驱逐不重要的KV
- StreamingLLM: 只保留attention sink + 滑动窗口
- TurboQuant: 旋转+量化到~3bit
- MTLA (NeurIPS 2025): 沿时间维度动态合并相邻KV向量
- Google DeepSeek-KV: 量化压缩

### 10. Prefix Caching
- 问题: 相同system prompt的请求重复计算
- 方案: 缓存并复用相同前缀的KV Cache
- RadixAttention (SGLang): 用Radix Tree管理前缀缓存
- Prompt Cache / Semantic Cache: 更广义的缓存策略

## Sources (verified 2026-05-21)
- Spheron Blog: LLM Serving Optimization (continuous batching + PagedAttention benchmarks)
- RunPod: vLLM Explained guide
- POD-Attention: ASPLOS 2025 (apanwariisc.github.io)
- GeneralCompute: Medusa/EAGLE/Sequoia comparison (2026-03)
- HuggingFace Blog: MLA explanation
- Medium: MHA vs MQA vs GQA vs MLA comparison
- Google Research Blog: TurboQuant (2026-03-24)
- llama.cpp Discussion #20969: TurboQuant implementation
- InfoQ: TurboQuant news (2026-04-15)
- vLLM docs: Structured outputs with xgrammar/outlines
- arXiv: BeaGLE cross-attention speculative decoding (2505.24544)
- EMNLP 2025: FractalLLM self-speculative decoding
