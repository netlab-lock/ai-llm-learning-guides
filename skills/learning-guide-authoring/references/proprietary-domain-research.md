# Proprietary Domain Research & Three-Layer Explanation

## Three-Layer Explanation Methodology (三层解释法)

Every technical concept in a learning guide MUST have three layers:

### Layer 1: 通俗类比 (Analogy)
Build intuition with everyday comparisons. Examples from the Ascend guide:

| Technical Concept | Analogy | Why it works |
|---|---|---|
| AI Core (Cube/Vector/Scalar) | Factory (machine shop / auxiliary / dispatcher) | Separates "main production" from "support" from "coordination" |
| Memory hierarchy (HBM→L0) | Warehouse → workshop → workbench | Distance = latency, size = capacity tradeoff |
| Software scratchpad vs hardware cache | Manual restocking vs automatic restocking | Explains WHY software-managed is more predictable |
| Tiling | Cutting a cake into slices | Can't fit whole matrix in L0, must slice |
| Jetty (connectionless transport) | Sending packages to a pickup locker vs making phone calls | Eliminates N² connection overhead |
| C-AQM congestion control | GPS navigation with per-request route hints vs "congestion ahead" sign | Request-precise vs flow-level feedback |
| Weak transaction ordering (RO/NO/SO) | Cafeteria queue: can cut / no queue / must queue | Different operations need different ordering |
| Ring AllReduce | Circle telephone game with file passing | Phase 1: pass + merge, Phase 2: broadcast |
| RHD algorithm | Tournament bracket (halving/doubling) | log₂N rounds vs N-1 rounds |
| Hierarchical communication | Village → township → county postal system | Small circles + fast local links = huge speedup |
| α-β model | Delivery fee = base price + weight fee | Small data: dominated by base price (latency). Large data: dominated by weight (bandwidth) |
| Bandwidth optimality | Learning songs: must learn N-1 + teach N-1 | Mathematical lower bound, Ring achieves it |
| MoE AllToAll | Hospital triage: patients routed to specialists | Dispatch = triage, Combine = pick up results |
| CANN compilation | Recipe → head chef → line chef → dish | Python → graph compiler → operator compiler → NPU |

### Layer 2: 技术原理 (Technical Principle)
- ASCII architecture diagrams
- Step-by-step execution flow
- Comparison tables with concrete parameters
- Protocol stack diagrams

### Layer 3: 数学/本质 (Mathematical Essence)
- Formal proofs (e.g., Ring AllReduce bandwidth optimality via proof by contradiction)
- Complexity analysis (O(N) vs O(log N) with concrete numbers)
- Quantitative comparisons (e.g., hierarchical: 0.45M vs single-layer: 2M)

### Anti-pattern: Surface-level "analogies"
BAD: "Ring is like a circle" — this is just restating the name, not building intuition.
GOOD: "Ring is like a circle telephone game where each person passes a file to the right while merging files from the left" — this explains the MECHANISM through the analogy.

## Proprietary Domain Source Hierarchy

For topics like Huawei Ascend, NVIDIA internals, specific hardware platforms:

### Source 1: Official Documentation
- Usually the most authoritative but often JS-rendered
- Chinese: hiascend.com, huaweicloud.com, mindspore.cn
- Workaround for JS sites: use browser_navigate + browser_snapshot

### Source 2: Source Code Repos (with GitHub API Deep Reading)
- Gitee (gitee.com) for Chinese companies (Huawei, Alibaba, etc.)
- GitHub for international projects
- Look for `docs/` directory and README.md — often contain algorithm descriptions
- Example: `gitee.com/ascend/cann-hccl/blob/master/docs/Ring.md`

**Deep source code reading via GitHub API** (validated 2026-06):
```bash
# Browse repo structure
curl -s "https://api.github.com/repos/OWNER/REPO/contents/src" | python3 -c "import json,sys; [print(f['name']) for f in json.load(sys.stdin)]"
# Read specific files
curl -sL "https://raw.githubusercontent.com/OWNER/REPO/master/src/file.h" | head -200
```
Key files: `include/*.h` (data structures, enums), `device/*.h` (kernel impls), `graph/*.cc` (topology/tuning).
See `github-api-source-reading.md` for full technique.

### Source 3: Academic Papers
- arXiv for official technical papers
- Search: `ddgs text -q 'company name topic arxiv paper' -m 5`
- Papers contain: architecture details, benchmark numbers, design rationale
- Example: arXiv:2506.12708 (CloudMatrix384) had production-grade benchmarks

### Source 4: Developer Personal Blogs
- Often the DEEPEST source — engineers sharing design thinking
- Example: Bojie Li (01.me) — Huawei distributed systems lab, wrote the best UB protocol analysis
- These contain "why" that official docs don't cover

### Source 5: Community Technical Blogs
- CSDN (blog.csdn.net) — usually accessible via curl
- Zhihu (zhuanlan.zhihu.com) — requires browser (JS-rendered)
- Huawei Cloud BBS (bbs.huaweicloud.cn) — mix of accessible and JS-rendered
- Medium/Substack — some paywalled

### Source 6: Industry Analysis
- SemiAnalysis, TechInsights (die photos, packaging analysis)
- China Research Collective (Substack) — detailed teardowns
- Convergedity (Substack) — chip roadmap analysis

## Search Strategy for Specialized Domains

Run 3 parallel delegate_task searches:
1. **Chinese queries**: `site:gitee.com`, `site:csdn.net`, `site:huaweicloud.com`
2. **English queries**: `site:arxiv.org`, `site:github.com`, general web
3. **Technical term queries**: Protocol names, algorithm names, product names

Each subagent uses `ddgs text -q '...' -m 5` via terminal toolset.
Collect ALL URLs with descriptions — even tangentially relevant ones.
Expect 30-80+ URLs from a comprehensive search.

## JS-Rendered Documentation Site Patterns

Many Chinese tech company doc sites use heavy JavaScript (Vue/React SSR):
- hiascend.com (Huawei Ascend docs)
- mindspore.cn (MindSpore docs)
- platform.moonshot.cn (Kimi docs)
- open.bigmodel.cn (Zhipu docs)

Workaround hierarchy:
1. `browser_navigate` + `browser_snapshot` — may work but slow
2. Search for the specific doc title to find mirrors/cross-posts
3. Look for the source repo (many doc sites are open-source MkDocs/Docusaurus)
4. Use `curl` with different User-Agent headers
5. Search for cached versions: `ddgs text -q '"exact page title"' -m 3`

## Synthesis Methodology

After gathering sources, synthesize content following this order:
1. **Architecture overview** — from official docs + papers
2. **Design rationale** — from developer blogs + papers (the "why")
3. **Technical details** — from source code + docs (the "how")
4. **Benchmark data** — from papers + blog posts (the "numbers")
5. **Community insights** — from CSDN/Zhihu (practical tips, common issues)
6. **Cross-validation** — compare claims across sources, note discrepancies
