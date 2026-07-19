# Round 10: Generic Content Cleanup & Full-Project Scaling (2026-06-30)

## Session Summary
- **Scope**: 850 files across 16 directories
- **Initial state**: 232/850 S-grade (27%), 287 files with generic templates
- **Final state**: 792/850 S-grade (93%), 0 generic templates in new dirs

## New Generic Patterns (8 patterns, 100+ files each)

| Pattern | Count | Source |
|---------|-------|--------|
| `采用分层架构来管理复杂性` | 62 | final_fix.py |
| `性能瓶颈通常在于内存带宽` | 114 | enhance_batch.py |
| `算术强度转折点 = 312T/2T` | 114 | enhance_batch.py |
| `的技术要点 1/2/3/4/5` | 76 | add_h2.py |
| `与本系列其他章节密切相关` | 210 | enhance_batch.py |
| `很多人只看概念不动手实验` | 63 | fix_content_v2.py |
| `可以跳过基础直接上手` | 63 | fix_content_v2.py |
| `建议先在小规模环境验证` | 63 | fix_content_v2.py |

## Content Quality vs Score Tradeoff

Removing generic content and replacing with shorter topic-specific content drops scores.
Principle: "诚实的A+优于虚假的S"

Strategy:
1. Batch scripts for structural additions (exercise/forward/path/code/ASCII/xref)
2. Subagents for content replacement (generic → topic-specific, ≥100 chars/para)
3. Score recovery for files that dropped below S
4. Accept A+ with real content over S with fake content

## Full-Project Scaling (850+ files)

- 10 files per subagent batch, 3 parallel max
- 287 files ≈ 29 batches ≈ 2-3 hours
- Process by directory, not file list

## New Failure Modes

### `</p<` Broken HTML
Cause: Regex cleanup leaves broken tags. Fix: `re.sub(r'</p<', '</p><', c)`

### h2 Title Leakage
Cause: Script inserts h2 title "一、背景与动机" into templates.
Fix: `re.sub(r'学习[一二三四五六七八九十\d]+[、.][^建]*建议按', '建议按', c)`
