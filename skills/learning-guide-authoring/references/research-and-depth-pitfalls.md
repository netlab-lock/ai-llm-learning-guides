# Research & Depth Pitfalls for Learning Guide Authoring

## Research Pitfalls for Fast-Moving Fields

### ddgs Language Issues
- **ddgs Chinese queries often fail** (DDGSException "No results found"). Use English queries as fallback — they return more results and better quality. For Chinese-specific content, try both languages in separate ddgs calls.
- When searching for Chinese LLM releases, use both: `"Kimi K2.7 月之暗面 2026"` AND `"Kimi K2.7 Moonshot 2026 release"`

### 3-Phase Search Strategy for Rapidly Evolving Topics
1. **Phase 1 — Broad sweep**: Search each major vendor + "latest 2026" in English
2. **Phase 2 — Gap check**: For vendors with no Phase 1 results, try Chinese queries AND check official sites
3. **Phase 3 — Cross-validate**: Search "X vs Y 2026" or "X benchmark 2026" to find comparative analyses that reveal missed releases

### Don't Assume Completeness
- After initial search, do a second pass searching for "<vendor> latest release" and check dates
- User will notice missing models (real example: K2.7 Code released June 12, GLM-5.2 released June 13 — missed on first pass)
- Note the **exact search date** in guides on weekly-changing fields and warn user content may be outdated

## Depth Requirements ("详尽透彻")

When user explicitly asks for more depth ("再详尽一点", "深入", "全面"), each model/topic section MUST include ALL of:

- [ ] Parameter table (total params, active params, architecture, context length)
- [ ] ASCII architecture diagram (not just a table — a visual diagram)
- [ ] Core innovation explanation (WHY it works, not just WHAT it is)
- [ ] Benchmark comparison table with exact scores (not just "strong")
- [ ] API pricing (if available)
- [ ] Open-source status and license
- [ ] Cross-vendor comparison tables
- [ ] Decision tree / selection guide
- [ ] Training methodology details (RL algorithm, data pipeline, optimizer)
- [ ] Limitations and known issues

### Don't Just List — Compare
User wants cross-vendor comparison tables, not isolated per-model descriptions. Include:
- Attention mechanism comparisons (CSA+HCA vs MLA vs Lightning vs GQA)
- MoE routing comparisons (expert count, activation ratio, load balancing)
- Training efficiency comparisons (relative cost, optimizer, precision)
- Agent capability comparisons (Terminal-Bench, SWE-bench, continuous runtime, parallel agents)

## Update Guide Strategy

When updating a series with many existing files (e.g., 221 HTML pages across 17 vendors):
- **Create a standalone "update panorama" file** rather than modifying every existing file
- More maintainable and user can review all updates in one place
- Use `patch` tool to add a prominent link in the main index.html
- The standalone file should be self-contained (own CSS, own navigation)

## Patch Tool for Large Insertions

When inserting large content blocks via `patch`:
- Use `mode=replace` with old_string being the footer/closing tags to preserve at end
- old_string must **exactly match** (including whitespace and quote style)
- If file has smart quotes or special characters, match may fail
- **Read the exact bytes around insertion point first** using `read_file` with specific offset/limit
- For very large insertions (>500 lines), consider writing to a temp file and concatenating via terminal

## Real-World Example: 2026 Chinese LLM Update Guide

Session: 2026-06-24
- Created 172KB guide covering 12+ models across 7 vendors
- 3,652 lines, 14 sections, 31 tables, 20 ASCII diagrams
- Key models covered: DeepSeek V4-Pro/Flash/R2, Qwen3/3.5/3.6/3.7, Kimi K2.6/K2.7, GLM-5/5.1/5.2, MiMo V2.5, MiniMax M1/M3, ERNIE 5.1, 豆包 Seed 2.0
- User pushed back twice: (1) missed recent models, (2) needed more depth
- Solution: Added "深度补充" section with 9 subsections covering attention mechanisms, MoE architecture, Qwen3 dual-mode reasoning, GLM architecture evolution, Lightning Attention, training efficiency, Agent capabilities, open-source ecosystem, and decision tree
