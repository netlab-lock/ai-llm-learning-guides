# Content Quality Cascade Patterns (2026-06-29)

## Overview
This document captures the cascade patterns discovered during the 09-厂商与前沿 (333 files) quality upgrade session. The key insight: fixing one quality issue often creates new issues, requiring careful sequencing.

## The Quality-Score Tradeoff

Removing generic/template content IMPROVES quality but REDUCES scores. The cascade:

| Operation | S+A+ % | Quality |
|-----------|--------|---------|
| Initial (template-heavy) | 100% | Low |
| Remove template warns (1165) | 92.8% | Medium |
| Remove template tips (213) | 92.8% | Medium |
| Remove generic tables (927) | **64%** | High |
| Add topic tables (58) | 71.2% | High |
| Add h3/exercises/lp (96) | 100% | High |

**Lesson**: The drop from 100%→64% is from removing 927 generic tables. Each table = 5 points. Must prepare replacement tables BEFORE deleting.

## Template Pattern Detection Checklist

### Warn templates (6 patterns, 1165 instances)
```
的关键是算法创新          → 187 files
只需要关注技术实现就够了  → 196 files  
的技术选型是"非此即彼"的  → 200 files
的评估结果可以直接用于生产 → 197 files
只看论文不看代码          → 204 files
"技术完美主义"            → 181 files
```

### Tip templates (2 patterns, 213 instances)
```
需要精准的参数调优和系统设计 → 191 files
自动售货机/自动贩卖机       → 20 files
```

### Deep templates (1 pattern, 68 instances)
```
基准测试的局限性在于：测试集可能出现在训练数据中 → 68 files
```

### Format errors (1 pattern, 145 instances)
```
通俗类比：</strong></strong> → 145 files (double closing tag)
```

### H1 title contamination (394+1655 instances)
H1 titles containing emoji (🏥📋⚡🔍🧠⚙️🚀📊) embedded in warn/deep content.
Fix: Replace h1_title with manufacturer name (mfr).

## Warn Uniqueness Cascade

When replacing template warns with a small set of variants:

| Variant count | Files | Uniqueness | Max repeat |
|--------------|-------|------------|------------|
| 5 variants | 333 | 2% | 140 |
| 15 variants | 333 | 37% | 30 |
| 50+ variants (dynamic) | 333 | 85% | 30 |

**Key**: Use file's h2 titles to generate unique content, not fixed variant pool.

## Thin h2 Sections

Sections with h3/tip/warn/deep but no body paragraphs (<50 words).

**Detection**: Count words in h2 section body (excluding tip/warn/deep/table/pre).
**Found**: 25 thin sections in 2040 total (1.2%).
**Fix**: Insert 1 paragraph after h2 tag.

## Sequencing Rules

1. **Never delete generic tables before preparing replacements**
2. **Replace warns/deeps BEFORE tips** (warns have smaller score impact)
3. **After each cleanup pass, re-score immediately**
4. **Fix format errors FIRST** (they don't affect score but look bad)
5. **Fix h1 contamination BEFORE warn replacement** (contaminated warns won't match patterns)

## Cross-File Paragraph Duplication

4241 paragraphs extracted, 159 duplicated across 3+ files (3.7%).

Most duplicated templates:
- "从{mfr}的工程实践看..." → 34 files
- "从行业视角来看..." → 26 files
- "基准测试是评估模型能力的标准化工具..." → 14 files

**Fix**: Replace with content containing file-specific h2 title + manufacturer name.
