# Scaling Law 学习指南 — 研究资料 (2026-05)

Research bank compiled from web searches (ddgs) during guide creation.

## Core Papers

| Paper | Authors/Inst | Year | Key Contribution |
|-------|-------------|------|------------------|
| Scaling Laws for Neural Language Models | Kaplan et al. / OpenAI | 2020 | Three independent power laws for N, D, C |
| Training Compute-Optimal LLMs | Hoffmann et al. / DeepMind | 2022 | N≈D balanced scaling, ~20 tokens/param |
| Emergent Abilities of LLMs | Wei et al. / Google | 2022 | Defined emergent abilities, BIG-Bench |
| Beyond Chinchilla-Optimal | MosaicML | 2024 | Include inference cost in scaling |
| Scaling LLM Test-Time Compute | Snell et al. / UC Berkeley | 2024 | Test-time compute scaling (foundational) |
| Inference Scaling Laws | Multi-institution | 2024 | Power-law for inference-time compute |
| Joint MoE Scaling Laws | ICML 2025 | 2025 | MoE independent scaling law |
| Towards Comprehensive MoE Scaling | arXiv 2509.23678 | 2025 | Shared experts, granularity |
| Towards Greater Leverage | arXiv 2507.17702 | 2025 | 300+ models, activation ratio power law |
| Scaling Laws for Downstream Tasks | EMNLP 2025 | 2025 | Downstream scaling unreliable |
| Data Mixing Laws | ICLR 2025 | 2025 | Loss = f(mixture_weights, N, D) |

## Kaplan Formulas (2020)

- L(N) = (Nc / N)^α_N, α_N ≈ 0.076, Nc ≈ 8.8 × 10^13
- L(D) = (Dc / D)^α_D, α_D ≈ 0.095, Dc ≈ 5.4 × 10^13
- L(C) = (Cc / C)^α_C, α_C ≈ 0.050, Cc ≈ 3.1 × 10^8
- Combined: L(N,D) ≈ (Nc/N)^0.076 + (Dc/D)^0.095 + E
- Strategy: Parameter-first, large model + early stopping

## Chinchilla Formulas (2022)

- L(N,D) = A/N^α + B/D^β + E
- A=406.4, α=0.34; B=410.7, β=0.28; E=1.69
- Optimal: D ≈ 20 × N (20 tokens per parameter)
- Compute: C ≈ 6ND → N_opt ≈ sqrt(C/120)

## Test-Time Compute Scaling (2024)

- Performance ∝ (Inference Compute)^γ
- γ ≈ 0.1-0.2 (math), 0.05-0.1 (code), 0.02-0.05 (general QA)
- Methods: Best-of-N, CoT search, self-verification, tree search (MCTS)
- o1 (Sept 2024): AIME ~83%, inference tokens 1K-50K
- DeepSeek-R1 (Jan 2025): pure RL (GRPO), matches o1

## MoE Scaling (2025)

- L(N_total, D, E) = A/N_active^α + B/D^β + C·g(E) + E_irr
- N_active (not N_total) determines loss
- More experts → better, with diminishing returns
- Leverage: DeepSeek-V3 671B/37B = 18x; Qwen3-235B/22B = 10.7x

## Data Scaling

- Beyond Chinchilla: smaller model + overtrained for high-inference scenarios
- LLaMA-3 8B: 15T tokens (1875 tokens/param), far beyond Chinchilla 20:1
- Data quality > quantity: Phi-1 (1.3B) matches 10B+ with curated data
- Data wall: ~15-25T high-quality English tokens, may exhaust by 2026-2028
- Code data boosts reasoning ability beyond programming

## Three Eras Summary

| Era | Year | Core Strategy | Representative |
|-----|------|---------------|----------------|
| 1st (Kaplan) | 2020 | N >> D, parameter-first | GPT-3 (175B) |
| 2nd (Chinchilla) | 2022 | N ≈ D, balanced | Chinchilla (70B), LLaMA |
| 3rd (Test-time) | 2024-2025 | N + D + C_infer, multi-axis | o1, R1, V4 |

## Sources

- https://arxiv.org/abs/2001.08361
- https://arxiv.org/abs/2203.15556
- https://arxiv.org/abs/2206.07682
- https://arxiv.org/abs/2401.00448
- https://arxiv.org/abs/2408.03314
- https://arxiv.org/abs/2408.00724
- https://arxiv.org/abs/2502.05172
- https://arxiv.org/abs/2509.23678
- https://arxiv.org/abs/2507.17702
- https://www.emergentmind.com/topics/scaling-laws
- SemiAnalysis Newsletter
