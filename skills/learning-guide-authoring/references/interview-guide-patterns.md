# Interview-Focused Learning Guide Patterns

When creating guides for interview preparation, add these specialized modules:

## Module Structure for Interview Guides

After the core theory modules (01-N), add interview-specific modules:

### Pattern: RAG Deep Dive (必考)
- Full pipeline: Query→Doc→Chunk→Embed→Retrieve→Rerank→Generate
- Vector search: Embedding models comparison, ANN algorithms (HNSW/IVF/PQ)
- Hybrid search: Dense + Sparse + RRF fusion
- Rerank: Bi-encoder vs Cross-encoder
- GraphRAG: Multi-hop reasoning, community detection
- Agentic RAG: Agent decides when/how to retrieve
- Hallucination prevention: 4-layer defense
- Evaluation: Faithfulness, Context Relevance, Recall@K

### Pattern: Model Fine-tuning (高频)
- Training pipeline: Pre-training → Post-training → Domain fine-tuning
- SFT: Instruction tuning, LoRA/QLoRA
- RLHF: 3-step process (SFT→Reward Model→PPO)
- DPO: Simplified alternative, no Reward Model needed
- Decision tree: Prompt vs RAG vs SFT vs DPO
- 2026 shift: Fine-tuning value changed from "capability" to "domain knowledge + preference"

### Pattern: Harness Engineering (2026新概念)
- Evolution: Prompt Engineering → Context Engineering → Harness Engineering
- 7 components: Context mgmt, Tool orchestration, Budget control, Termination, Trajectory eval, Error recovery, Safety
- Loop Engineering: 5 types of governance (context/state/budget/tool/termination)
- Multi-Agent Harness: Communication, budget allocation, error isolation

### Pattern: Interview Q&A Module
- Use `.qa` CSS class for Q&A cards
- Structure: Question → Answer points → Follow-up direction
- Cover: Architecture, RAG, FC/MCP, Memory, Multi-agent, Safety, Fine-tuning, Production
- Include preparation checklist with priority and time estimates

## CSS for Q&A Cards
```css
.qa{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.2rem;margin:1rem 0}
.qa .q{color:var(--yellow);font-weight:700;font-size:1.05em;margin-bottom:.5rem}
.qa .a{color:var(--text)}
.qa .key{color:var(--green);font-weight:600}
```

## Iterative Audit Methodology
When user asks to "检查/审计" a guide repeatedly:
1. Round 1: Element counting (tip/warn/exercise/deep/ascii/table per file)
2. Round 2: Topic coverage (grep for key terms per module)
3. Round 3: Cross-references between modules + globally missing topics
4. Round 4: Per-module subtopic audit + section density analysis
5. Round 5: HTML correctness + duplicate detection
6. Declare complete after 5 rounds unless user specifies new direction

## Content Density Targets
- Ideal: 1500-2500 chars per h2 section
- If any module < 1200 chars/section, it needs enrichment
- If ratio of max/min > 2.0, balance with more content in thin modules
