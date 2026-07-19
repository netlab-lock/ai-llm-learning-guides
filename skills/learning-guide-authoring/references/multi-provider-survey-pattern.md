# Multi-Provider Domain Survey Pattern

When the user asks to "调研所有X厂商" or "survey all providers in domain X", use this pattern. Common domains: Chinese LLMs, cloud providers, inference frameworks, etc.

## Template Structure

Each provider entry should cover:
1. **公司背景** — founding, key people, headquarters
2. **模型发布时间线** — chronological list with dates, model names, parameter counts
3. **最新模型** — flagship model name, params (total/active), context length, architecture
4. **关键技术** — 3-5 key innovations with brief explanations (MLA, MoE, RL training, etc.)
5. **开源状态** — fully open / partially open / closed, license type
6. **生态与应用** — products, API availability, pricing strategy

## Output Format

Create a single comprehensive HTML file (not multiple files per provider) with:
- Hero section: title, provider count, date range
- Quick comparison table: one row per provider (name, latest model, params, key tech, open-source status)
- Per-provider detailed sections: h2 per provider with timeline, tech details, comparison
- ASCII timeline: horizontal timeline showing all providers' model releases
- Innovation map: card grid of cross-cutting technical innovations (who pioneered what)
- Learning roadmap: recommended reading order

## Research Strategy

1. **Check existing files first** — user may already have partial content in the target directory
2. **Parallel subagent search (preferred)** — Use `delegate_task` with `toolsets=["terminal"]` + `ddgs text -q '...' -m 3`. Max 3 per batch. ddgs CLI is pre-installed at `~/.local/bin/ddgs`.
3. **Platform docs over web search** — Chinese AI platform developer docs are more reliable than search engines (see `chinese-ai-platform-docs.md`)
4. **Mark uncertain data** — use "推测" for unverified parameter counts, "截至YYYY-MM" for knowledge cutoff dates
5. **Don't delegate large HTML generation to subagents** — they timeout at 600s. Write large files via parent agent's `execute_code` instead.

## Chinese LLM Providers (17 as of 2026-05)

Tier 1 (global impact): DeepSeek, Qwen/阿里云, GLM/智谱AI (Z.ai)
Tier 2 (strong domestic): 月之暗面/Kimi, MiniMax, 字节跳动/豆包Doubao, 百度/文心ERNIE
Tier 3 (notable niche): 阶跃星辰/StepFun, 科大讯飞/星火Spark, 商汤/SenseTime + InternLM, 小米/MiMo, 百川智能/Baichuan, 零一万物/01.AI, 腾讯/混元Hunyuan, 昆仑万维/天工Skywork, 面壁智能/ModelBest MiniCPM, 阿里巴巴通义Tongyi

## Pitfalls

- Don't create one HTML file per provider — that's the sub-directory layout for learning guides. Provider surveys work better as a single scrollable page.
- Parameter counts are often unverified — always note the source or mark as estimated.
- Model names change frequently (e.g., Doubao → Seed, ERNIE versioning). Use the latest known name.
- Some providers (ByteDance, Baidu) deliberately obscure parameter counts.
