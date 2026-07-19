# Knowledge Gap Audit → Prompts → Sequential Generation

End-to-end workflow for systematically filling a knowledge base. Used when the user has an existing learning library and wants to identify gaps and fill them methodically.

## Phase 1: Knowledge Gap Audit

1. **Inventory** — `find /path/ -name '*.html' | cut -d'/' -f1-2 | sort | uniq -c` to get file counts per section
2. **Sample quality** — Pick 3-5 representative files, check `wc -c` (target 14-21KB), count `<h[1-3]` sections
3. **Identify structural gaps** — Empty shell directories (only index.html), missing prerequisites, imbalance patterns ("重推理轻训练")
4. **Search for frontier topics** — Use `ddgs` to check what's current in the field that's not covered
5. **Write gap checklist** — Markdown file at the learning directory root with:
   - Current coverage assessment (table)
   - Identified problems
   - Gaps organized by priority (P0/P1/P2/P3)
   - Each gap: topic name, output path, specific sub-topics, references
   - Progress tracking table with checkboxes

**Output**: `学习缺口清单.md` at the learning directory root

## Phase 2: Prompt Writing

For each gap direction, write a self-contained prompt that specifies:
1. Role + context
2. Output format (HTML, dark theme, Chinese, file path)
3. 8-dimension framework reminder (背景→原理→技术细节→对比→...)
4. Module structure (numbered files, each with specific chapter titles)
5. Topic-specific sub-topics (detailed, not vague — "数据清洗与质量过滤" not "数据处理")
6. Must-include concepts, formulas, comparison tables
7. Reference sources

**Key user preference**: User explicitly said "担心批量生成会影响质量" — prefer one-by-one generation over batch. Each prompt should be self-contained for maximum depth.

**Output**: `学习提示词-P0.md` through `学习提示词-P3.md` (one per priority level)

## Phase 3: Sequential Multi-Direction Generation

For each direction:
1. Search for latest info (`ddgs text -q '...' -m 3`)
2. Create output directory (`mkdir -p`)
3. Write Python script(s) to `/tmp/gen_<topic>_p<N>.py` (2-3 files per script)
4. Execute via `terminal("python3 /tmp/gen_<topic>_p<N>.py")`
5. Verify file count and sizes
6. Update todo list
7. Move to next direction

**Batch size per script**: 2-3 files is reliable on mimo-v2.5-pro. 4+ files risks content truncation.

**CSS reuse**: Always extract CSS from an existing file in the same guide for consistency.

**Progress tracking**: Use todo list with per-direction status (pending/in_progress/completed) and file count + size.

## Phase 4: Enrichment Pass (Post-Generation)

After all directions are generated, the user may request "补强" (enrichment) for more diagrams, foundations, and latest tech. Validated workflow (2026-05-27, 6 directions × 7-8 files):

1. **Audit thin files** — `execute_code` loop checking `wc -c` for all non-index files, flagging those < 10KB
2. **Search latest tech** — `ddgs text -q 'topic latest 2025 2026' -m 3` for trending developments
3. **Write enrichment scripts** — Python scripts that overwrite ONLY the thinnest files with expanded content
   - Add ASCII architecture diagrams (chip layouts, data flows, comparison visualizations)
   - Add "名字由来" (name origin) sections for deeper context
   - Add latest/trending technology sections with search-verified data
   - Add foundation/prerequisite knowledge sections
   - Target: each enriched file grows from 5-7KB to 10-14KB
4. **Fix triple-quote nesting** — If enrichment scripts contain HTML `<pre><code>` blocks with Python triple-quoted strings, write a fix script that replaces `"""` with `&quot;&quot;&quot;` inside `<span class="string">` tags
5. **Re-audit** — Verify thin files grew; remaining 8-9KB files are acceptable

**Batch size**: Enrich 3-4 files per script. Focus on core technical modules (02-04) first, then overview/summary if time permits.

## Phase 5: Completion Verification & Framework Gap Analysis

After all gap items are generated (and optionally enriched), verify completeness before declaring done. This phase transforms the gap checklist from a TODO list into a project completion report.

### Step 1: Gap List Compliance Check

For each item in the gap checklist:
1. Confirm output directory exists
2. Count HTML files: `find "$dir" -name "*.html" | wc -l`
3. Check total size: `find "$dir" -name "*.html" -exec du -cb {} + | tail -1`
4. Spot-check 2-3 files for line count (`wc -l`) — flag any < 100 lines as suspicious
5. Compare against the gap list's "覆盖内容" bullets — verify each sub-topic has a corresponding file

**Minimum thresholds**: 7+ files per direction, 59KB+ total, each file 150+ lines.

### Step 2: Empty Shell Detection

Previously-created directories may contain only an index.html with broken references (the "空壳" pattern — seen with 经典模型 directory). Detection:

```bash
for d in /path/to/*/; do
  html_count=$(find "$d" -maxdepth 1 -name "*.html" ! -name "index.html" | wc -l)
  if [ "$html_count" -eq 0 ]; then
    echo "EMPTY SHELL: $(basename $d)"
  fi
done
```

Also check that index.html links don't point to nonexistent files.

### Step 3: Knowledge Framework Pillar Analysis

After gap compliance is verified, zoom out to the full knowledge base. Organize ALL content (gap items + existing guides + systematic guide) into **knowledge pillars** (6-12 broad categories covering the entire field):

| Pillar | Sources to include |
|--------|-------------------|
| Foundation | Classical models guide + systematic guide chapters 1-3 |
| Data | 训练数据工程 + Tokenizer深度 + systematic guide §2 |
| Architecture | MoE + 注意力前沿 + 长上下文 + systematic guide §9 |
| Training | 训练基础设施 + systematic guide §3, §7 |
| Alignment | 安全与对齐 + RLEF + systematic guide §4 |
| Optimization | 知识蒸馏 + 模型融合 + systematic guide §6 |
| Inference | 推理框架 + 编译优化 + 推理服务架构 + systematic guide §12 |
| Deployment | ContextCaching + StructuredOutput |
| Applications | RAG + Agent + 代码生成 + 多模态 + systematic guide §10 |
| Hardware | GPU架构 + 非NVIDIA + 集合通信 |
| Providers | 国产LLM系列 + 联邦学习 |
| Theory | Scaling Law + systematic guide §11 |

For each pillar, assess: ★★★★★ (deep) → ★☆☆☆☆ (missing). Identify pillars with only shallow coverage (★★★ or below) — these become **optional deepening directions** to suggest.

### Step 4: Update Gap List as Living Document

Transform the gap checklist into a **completion report**:
- All `[ ]` checkboxes → `[x]` with "✅ 已完成" status
- Add file count + total size to each completed item
- Add "七、整体知识框架完整性分析" section with pillar coverage table
- Add "可能的补充方向" section listing optional deepenings (with rationale: what's already covered in systematic guide, what would benefit from standalone deep-dive)
- Add "八、知识库统计" section with totals (files, size, directions)
- Update the progress tracking table with actual dates and file counts

**File**: Update `学习缺口清单.md` in-place at the same path.

### Pitfalls

- Don't just check directory existence — verify actual content (files, sizes, line counts)
- Empty shells are a known pattern — always check, especially for directories created in early sessions
- The gap list should be self-contained after completion — a reader should understand the full project status without external context
- "Optional deepening directions" should reference what's already covered in the systematic guide, not suggest completely missing topics
- Cross-reference pillar analysis with the systematic guide's chapter structure to avoid recommending topics that already have adequate coverage

---

## Pitfalls (General)

- **"写进文档" ≠ "生成指南"**: When user says "将提示词写进文档" or "写进文档", they mean SAVE THE PROMPT TEXT into a .md file for later use — NOT immediately execute the prompt to generate HTML guides. Always confirm intent before bulk-generating. (Session correction 2026-05-27: user said "我说的是把要做的几个方向的提示词写到md文档中，我们后面再生成指南，而不是让你直接生成指南")
- Don't generate all directions simultaneously — sequential gives better quality control
- Don't skip the search step — fresh data matters for fast-moving fields (LLM, AI)
- File sizes of 6-9KB per module are acceptable for bulk generation; deepen in second pass if needed
- Always generate index.html last (it references all other files)
- Update the gap checklist's progress table after completing each direction
- Enrichment scripts that contain HTML with triple-quoted Python prompt examples cause SyntaxError — use fix_quotes.py approach (see main skill pitfall #33)
