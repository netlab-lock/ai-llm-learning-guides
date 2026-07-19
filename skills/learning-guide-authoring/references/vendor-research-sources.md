# Vendor-Specific Research Sources for Chinese LLM Guides

Search patterns for finding technical details when enhancing learning guide files.

## Tencent Hunyuan

- arXiv:2411.02265 — Hunyuan-Large (389B/52B MoE, Scaling Laws, Recycle Routing)
- arXiv:2505.15431 — Hunyuan-TurboS (Mamba2-Transformer hybrid, Adaptive CoT, Two-stage GRPO)
- GitHub: `Tencent-Hunyuan/Hunyuan-A13B` (80B/13B, Technical Report PDF)
- GitHub: `Tencent-Hunyuan/Hunyuan-TurboS`
- GitHub: `Tencent/Tencent-Hunyuan-Large`
- Search: `ddgs text -q 'Hunyuan MoE architecture technical details' -m 5`

## Baidu ERNIE

- arXiv:1904.09223 — ERNIE 1.0 (knowledge masking)
- arXiv:1907.12412 — ERNIE 2.0 (continual pre-training)
- arXiv:2107.02137 — ERNIE 3.0
- arXiv:2602.04705 — ERNIE 5.0 (trillion-param omni-modal)
- Technical Report: `ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf`
- HuggingFace: `huggingface.co/baidu/ERNIE-4.5-300B-A47B-PT`
- Key innovation: Heterogeneous MoE (cross-modal parameter sharing)
- Search: `ddgs text -q 'ERNIE 4.5 heterogeneous MoE architecture' -m 5`

## Xiaomi MiMo

- arXiv:2505.07608 — MiMo-7B (25T tokens, rule-based RL, test-difficulty-driven code reward)
- arXiv:2506.03569 — MiMo-VL
- arXiv:2511.16518 — MiMo-Embodied
- HuggingFace config.json has exact specs: hidden=4096, layers=36, heads=32, KV=8, RoPE theta=640000
- Key innovation: No reward model, pure rule-based accuracy rewards for RL
- Search: `ddgs text -q 'Xiaomi MiMo 7B architecture training details' -m 5`

## StepFun

- Step-3: 321B/38B MoE, MFA (Multi-Matrix Factorization Attention), AFD
- MFA reduces query matrix 7168→2048 via low-rank factorization
- KV-cache: 22% of DeepSeek V3's per-token cost
- 48 experts per layer, 3+1 routing (3 routed + 1 shared)
- Search: `ddgs text -q 'StepFun Step-3 MFA architecture technical' -m 5`

## 01AI (Yi)

- Yi-Lightning: MoE with fine-grained experts, hybrid attention (3 sliding window + 1 full)
- Cross-layer KV cache sharing (halves memory)
- RoPE theta=5,000,000 (very high, for long context)
- Search: `ddgs text -q '01AI Yi Lightning MoE architecture' -m 5`

## Baichuan

- Baichuan2: SwiGLU activation, 8/3 * hidden_size FFN, NormHead
- Baichuan v1: ALiBi position encoding; Baichuan2: RoPE (7B) / ALiBi (13B)
- Vocab: 125,696 (expanded from 64K in v1)
- 2.6T training tokens for Baichuan2
- Search: `ddgs text -q 'Baichuan2 architecture SwiGLU NormHead' -m 5`

## General Search Patterns

```bash
# English search for architecture details
ddgs text -q 'VendorName ModelName architecture technical details parameters layers heads' -m 5

# Chinese search for training/innovation details
ddgs text -q '厂商名 模型名 技术细节 架构 论文' -m 5

# HuggingFace model config (get exact specs)
curl -sL "https://huggingface.co/api/models/OrgName/ModelName" | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(f'Tags: {d.get(\"tags\",[])}')
print(f'Pipeline: {d.get(\"pipeline_tag\",\"?\")}')
"

# GitHub README (extract technical details)
curl -sL "https://github.com/OrgName/RepoName" 2>/dev/null | sed 's/<[^>]*>//g' | sed '/^$/d' | grep -i "architect\|layer\|head\|param\|train\|benchmark" | head -30

# DeepWiki (often has structured technical overviews)
ddgs text -q 'site:deepwiki.com VendorName ModelName' -m 3
```

## Pitfalls

- Chinese vendor docs often don't publish exact architecture specs (layer count, head count). Check HuggingFace model repos for `config.json` which has exact values.
- Some vendors (e.g., ERNIE 5.0) claim to beat GPT-5 without publishing detailed benchmarks. Mark claims as "厂商宣称" (vendor claim) in guides.
- Model parameter counts may be estimated. Use "推测" (estimated) when not officially confirmed.
