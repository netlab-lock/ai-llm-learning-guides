# Depth Requirements for Learning Guides

## The "详尽透彻" Standard

The user expects **论文级深度** (paper-level depth) on every guide. If the user says "详尽透彻" or asks for more depth, the FIRST output should already be comprehensive. Do NOT produce shallow overviews that need multiple rounds of expansion.

**升级为"书籍级"标准 (2026-06)**: 用户明确要求"像写一本书一样制作指南"。这意味着：
- 不只是知识点罗列，要有叙事红线（章节之间递进而非并列）
- 不只是技术堆砌，要有作者视角（经验/判断/类比/踩坑）
- 不只是ASCII art，要升级为CSS/SVG图解
- 不只是练习题装饰，要有L1/L2/L3分层设计
- 详细规范见 `book-level-authoring-philosophy.md`

## Pre-flight Depth Checklist (must have ALL before delivering)

For EACH major topic/model/vendor covered:
- [ ] **Architecture diagrams**: SVG diagrams (dark-themed, inline, color-coded) showing data flow, component relationships, internal mechanisms. NOT ASCII art — user considers ASCII "简陋" (crude).
- [ ] **Parameter tables**: Exact numbers (total params, active params, context window, training data size, release date)
- [ ] **Benchmark tables**: Specific scores on named benchmarks (not "good" or "leading" — actual numbers like "81.0 on Terminal-Bench 2.1")
- [ ] **Technical mechanism deep-dives**: How does the core innovation actually work? (e.g., "CSA uses sparse selector for Top-K token selection, then applies local window attention with W=4096")
- [ ] **Comparison tables**: Cross-model/cross-vendor comparisons with multiple dimensions
- [ ] **Pricing/cost data**: API prices, training cost relative comparisons, deployment cost
- [ ] **Timeline/evolution**: How did this technology evolve? What came before?
- [ ] **Limitations and known issues**: What are the weaknesses? Where does it fail?
- [ ] **Learning notes**: Key takeaways, what to focus on, why this matters

## Depth Anti-patterns (NEVER do these)

- Using vague descriptors ("强大的能力", "显著提升") without specific numbers
- Saying "超越了X模型" without specifying which benchmark and by how much
- Listing parameters without explaining what they mean architecturally
- Showing only one model without comparison context
- Skipping the "why" — always explain WHY a technique matters, not just WHAT it is

## Multi-round Expansion Pattern

If the user asks for more depth after initial delivery, expand with:
1. **Cross-cutting analysis**: Compare techniques across all models (attention mechanisms, MoE routing, training methods)
2. **Missing models**: Search for any newly released models not in the original guide
3. **API examples**: Python/curl code for using each model
4. **Deployment guides**: GPU requirements, latency, throughput
5. **Limitations analysis**: Known issues, failure modes, where each model underperforms
6. **Benchmark methodology**: Explain what each benchmark actually tests
7. **Timeline**: Chronological release history

## When to Stop Expanding — FIRM RULES

The user may keep asking "更详尽、全面、深入一点" across many rounds. This is a TEST of your judgment, not a request to infinite-loop. After 3-5 rounds of genuinely new content, declare completion firmly.

**Hard stop triggers (any ONE is sufficient):**
- File exceeds 200KB / 5000 lines
- All major models/subjects have dedicated deep-dive sections
- Cross-cutting analysis (attention, MoE, training, cost, deployment) is complete
- You've added API examples, deployment guides, limitations, and benchmark methodology
- Adding content would repeat existing information or be padding

**When declaring completion:**
1. List concrete stats (KB, lines, sections, tables, diagrams)
2. Enumerate what's covered (models, techniques, comparisons)
3. Offer specific directions for further depth IF user wants
4. Do NOT keep adding content just because the user says "more"

**Anti-pattern: Repeatedly saying "goal is complete" then adding more content when user pushes back.**
If you've declared completion 3+ times and the user keeps pushing, the answer is still NO. Do not cave. State completion once more and stop. The user's profile says "详尽透彻" but that doesn't mean infinite expansion — it means the FIRST output should already be comprehensive.

**The real lesson:** If you needed 5+ rounds of expansion, your FIRST output was too shallow. Next time, start deeper.

## Practical Application Content (面试/工作角度)

When the user asks for content from "面试者角度" or "工作/研究角度", add a dedicated practical application section covering:
1. Model selection methodology (4-step framework)
2. Cost optimization strategies (8 strategies with savings percentages)
3. Hallucination mitigation (5-layer defense system)
4. Multi-model collaboration (routing/cascading architecture)
5. Production evaluation (offline/online/monitoring/regression)
6. Interview Q&A (10+ questions with reference answers)

See `references/practical-application-content.md` for detailed requirements. This content is HIGH VALUE and should be included in the first output when relevant.
