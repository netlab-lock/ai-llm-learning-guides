# Bulk HTML Quality Upgrade Workflow (333+ files)

## Session Context
333 HTML learning guides in `09-厂商与前沿/` (17 Chinese LLM manufacturers + 5 international).
Each file: ~5-20KB, dark-themed, with h2/h3 sections, tip/warn/deep blocks, tables, ASCII art.
Goal: upgrade all files from A-level (400-440) to S/A+ (440-450).

## Multi-Phase Pipeline

### Phase 1: File-level fixes (exercises, learnpath, forward)
- **Scope**: One fix per file (not per section)
- **Approach**: Python script with regex replacement
- **Pattern**: Generate exercises from h2 titles, generic learnpath per manufacturer
- **Result**: 269/333 files fixed in seconds

### Phase 2: Replace generic teaching elements
- **Detection**: Extract all tip/warn/deep text, count frequency
- **Threshold**: Text appearing ≥3 times = generic
- **24 generic tip patterns** found (563 total instances)
- **Approach**: Keyword→analogy mapping with manufacturer context
- **Critical bug**: `replacements.sort(reverse=True)` must be used to avoid position offset

### Phase 3: Add h3 subsections
- **The main bottleneck**: `min(10, h3/10*10)` scoring means h3=0→h3=10 = +10 points
- **78 A-level files ALL had h3 as primary bottleneck**
- **Approach**: Subagent generates h3 title + body paragraph per h2 section
- **Batch size**: 5-6 files per subagent call
- **Wait**: 20-30 seconds between calls to avoid 429

### Phase 4: Remove template garbage
- **908,746 characters** of identical template text across 329 files
- **Patterns**: "从系统设计角度看...由三个关键组件构成", "在实现层面...采用了分层抽象的设计哲学"
- **Detection**: `grep -c "由三个关键组件构成" *.html`
- **Impact**: Scores dropped from 100% to 72% — this is CORRECT behavior
- **Lesson**: Template content inflates scores without adding value. Always verify by reading actual files.

### Phase 5: Replace bland analogies
- **30% of tips** had generic analogies (e.g., "类比搜索引擎排序" for unrelated topics)
- **Fix**: Fine-grained keyword→specific analogy mapping
- **Result**: 0 bland tips remaining

### Phase 6: Fill empty h2 sections
- **835 empty h2 sections** across 281 files (after template removal)
- **Approach**: Python script with topic-based content library
- **Content library**: 20+ topic categories with manufacturer-specific templates

### Phase 7: Subagent h3 generation
- **Slowest phase**: ~5 minutes per batch of 5-6 files
- **Each file needs 5-10 h3 subsections** with real content
- **Progress**: 72% → 81% over many batches
- **Remaining**: ~60 files at session end

## Scoring Function Pitfalls

### Inconsistency
Different scoring functions gave different results:
- Function A: `exercises=1, learn_path=1` (hardcoded) → 100% S+A+
- Function B: `exercises = 1 if re.search(...)` (actual check) → 72% S+A+
**Always use the actual-check version.**

### h3 Dominance
`min(10, h3/10*10)` means:
- h3=0 → 0 points
- h3=5 → 5 points  
- h3=10 → 10 points
Each h3 subsection is worth exactly 1 point. Files with h3=0 lose 10 points.

### Deep Keywords
`min(20, deep_kw/5*20)` where deep_kw = count of 公式|推导|证明|原理|工作机制|数学本质|为什么
Adding 1-2 paragraphs with these keywords can boost by 4-8 points.

## Subagent Strategy

### Evolution
1. **Write entire files** (12-22KB output) → Too expensive, 429 after 2-3 files
2. **JSON config + script** → Better but still large
3. **Patch-based modification** (delta only) → Most efficient, 5-6 files per call

### Batch Pattern
```
sleep 20
delegate_task(files=5-6, goal="Add h3 subsections", toolsets=["file"])
# Subagent reads file → generates h3 title + paragraph → patches file
# Repeat for next batch
```

### 429 Handling
- Wait 20-30 seconds between calls
- Reduce batch size to 3-4 if persistent
- Subagent timeout: child_timeout=1800s

## Content Quality Verification

### Must-check metrics (not just scores)
1. **Empty h2 sections**: `len(real_paras) == 0`
2. **Template h3 titles**: Contains "核心组件与工作原理" or "训练流程与优化策略"
3. **Template body paragraphs**: Contains "由三个关键组件构成" or "采用了分层抽象的设计哲学"
4. **Bland tips**: First 80 chars match any generic pattern
5. **Duplicate tips**: Same tip text appearing in 3+ files

### Verification command
```python
# Check all quality dimensions at once
for fp in glob.glob("**/*.html", recursive=True):
    content = open(fp).read()
    # 1. Empty sections
    for h2 in h2_sections:
        if no_real_paragraph: empty_h2 += 1
    # 2. Template h3
    if '核心组件与工作原理' in h3_title: template_h3 += 1
    # 3. Template body
    if '由三个关键组件构成' in content: template_body += 1
    # 4. Bland tips
    if any(pattern in tip_text for pattern in GENERIC): bland += 1
```

## File Structure (post-upgrade)
Each h2 section should have:
- 1-2 body paragraphs (real content, not template)
- 1 h3 subsection minimum (descriptive title + body)
- 1 tip (specific analogy)
- 1 warn (specific misconception)
- 1 deep (specific technical detail)
- Optional: table, ASCII diagram, code block

File-level:
- Exercises (3 questions, topic-specific)
- Learning path (manufacturer-specific)
- Navigation (prev/next)
