# Multi-Vendor Deep-Dive Guide Creation Workflow

## Overview
When creating technical deep-dive guides for multiple vendors (e.g., 5+ Chinese LLM providers), each with 12 files, the total is 60+ files. This requires a systematic approach.

## Validated Workflow (2026-06)

### Phase 1: Create Directory Structure
```bash
for vendor in Qwen Kimi GLM MiniMax ByteDance; do
    mkdir -p "/mnt/d/学习/.../$vendor/${vendor}系列深度学习"
done
```

### Phase 2: Create Index Files First
Create all index.html files first (fast, ~3 files/second via execute_code + write_file).
Each index.html includes: chapter list table, links to vendor overview and 2026全景.

### Phase 3: Create Chapters via Subagents
Use delegate_task with 3 concurrent subagents, each handling ONE vendor's full 11 chapters.
- Timeout: 600s per subagent
- Expected output: 4-8 files per subagent before timeout
- Remaining files: Create manually after subagent completes

### Phase 4: Fill Remaining Files
After subagents timeout (they will), check what was produced, then create remaining files via execute_code + write_file (3 files per batch).

### Phase 5: Add Cross-References
Add bidirectional links between:
- Vendor overview index ↔ Deep-dive index
- Deep-dive index ↔ 2026年中模型更新全景.html
- Related vendors (e.g., DeepSeek ↔ Qwen for MoE comparison)

### Phase 6: Verify
Count files per directory and check sizes.

## Subagent Timeout Handling
- Subagents timeout at 600s on mimo-v2.5-pro
- They typically produce 4-8 files before timeout
- Check produced files BEFORE retrying
- Don't retry the same subagent — fill remaining manually
- Manual creation: 3 files per execute_code batch, ~3 seconds per batch

## Content Quality per Chapter
- Target: 150-250 lines, 8-15KB
- Must include: ASCII diagram, comparison table, practical details
- Vendor-specific content (not generic)

## Validated Vendor List (2026-06)
| Vendor | Status | Files | Size |
|--------|--------|-------|------|
| DeepSeek | ✅ | 12 | 211KB |
| Qwen | ✅ | 12 | 110KB |
| Kimi | ✅ | 12 | 103KB |
| GLM | ✅ | 12 | 117KB |
| MiniMax | ✅ | 12 | ~100KB |
