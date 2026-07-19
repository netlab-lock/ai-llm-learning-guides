# Technical Guide Audit Workflow (查缺补漏)

When user asks to audit/evaluate existing technical guides against current state, follow this workflow.

## Step 1: Inventory Existing Content

Use `search_files` with MULTIPLE search patterns (Chinese + English) to find all related files:
- Chinese terms: *推理*, *部署*, *训练*, *量化* etc.
- English terms: *infer*, *serv*, *vLLM*, *deploy* etc.
- File patterns: *.html in target directory

Check BOTH the main topic directory AND related directories. Example:
- Main: `05-推理优化/推理框架/` (50+ files)
- Related: `05-推理优化/推理服务架构/` (7 files)
- Scattered: Each `国产LLM系列/` subdirectory has copies (推理能力/部署优化)

Read the overview and comparison files first — they reveal the structure.

Use `ls -la` to check file timestamps — content freshness matters.

## Step 2: Web Research Current State

Use `ddgs` CLI DIRECTLY — do NOT delegate to subagents (they timeout on rate-limited search APIs).

```bash
ddgs text -k "LLM inference framework 2025 2026 vLLM SGLang comparison" -m 10
ddgs text -k "SGLang 2026 latest features update" -m 8
ddgs text -k "new framework name 2026" -m 6
```

Focus on:
- New frameworks/tools that didn't exist when content was created
- Tools that entered maintenance/deprecated status
- Major version changes (e.g., vLLM v0.19 vs v0.8)
- Paradigm shifts (e.g., Disaggregated Serving becoming mainstream)

## Step 3: Gap Analysis Report

Produce a structured report:

```
## 一、现有内容概览
- Location, file count, directory structure
- Coverage summary

## 二、质量评审（优点）
- What's done well (be specific)

## 三、重大缺失（需要更新）
For each gap:
- What it is (1-2 sentences)
- Why it matters (impact)
- Suggested action + file location
- ⭐ Priority indicator

## 四、更新优先级
P0（必做）: Must-fix, outdated/wrong info
P1（重要）: Missing important content
P2（锦上添花）: Nice-to-have additions
```

## Pitfalls

- **Subagents timeout on web search** — rate limits + slow APIs = 600s timeout. Do it directly with `ddgs`.
- **Don't audit every copy** — when 15+ vendor directories each have "推理能力" files, note the duplication but evaluate the canonical version only.
- **File timestamps reveal staleness** — a 2025-05 creation date on a fast-moving field = likely outdated.
- **Check if "recommended" tools are still active** — TGI entering maintenance mode is the kind of change users need to know.
