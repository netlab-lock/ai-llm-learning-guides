# Guide Enhancement Workflow (Audit → Enhance → Verify)

## When to use
User says "查缺补漏", "更加详尽", "补充内容", or asks to audit/improve an existing guide.

## Step 1: Audit existing content
```python
# Extract structure from all files
for f in files:
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content)
    h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', content)
    ascii_count = len(re.findall(r'class="ascii"', content))
    table_count = len(re.findall(r'<table', content))
    tip_count = len(re.findall(r'class="tip"', content))
```

## Step 2: Keyword coverage check
```bash
# Check which important topics are missing
for kw in 'keyword1' 'keyword2' ...; do
  grep -rl "$kw" $base/*.html | wc -l
done
```

## Step 3: Gap identification matrix
| Module | Lines | ASCII | Tables | Tips | Missing Topics |
Create a table like above to identify weak modules.

## Step 4: Parallel enhancement via delegate_task
- Max 3 concurrent subagents (system limit)
- Use `toolsets=["file"]` for file operations
- Rate limiting is common (HTTP 429) — have fallback plan
- Subagents can read + patch files successfully
- Give specific insertion anchors (e.g., "before section X.9 术语速查表")

## Step 5: Verify
```bash
wc -l -c $base/*.html | sort -n  # Size check
grep -rl 'keyword' $base/*.html  # Coverage check
```

## Multi-dimensional coverage pattern
When user asks for "面试、工作、研究、学习" angles, create a 知识全景图 that includes:
1. 面试速查 (interview quick reference) — TOP 20 questions with difficulty levels
2. 工作实战 (work practical) — tuning checklists, environment variables, fault diagnosis
3. 研究前沿 (research frontier) — papers, trends, technology roadmap
4. 学习路径 (learning path) — day-by-day plan with checkpoints
5. 一页速查表 (one-page cheatsheet) — formulas, comparison tables
6. 相关领域 (related fields) — adjacent knowledge areas

## Deep algorithm content pattern
When user asks for "原理、技术细节", create a dedicated deep-dive module with:
1. Theory foundation (mathematical models like LogP/LogGP)
2. Step-by-step walkthroughs with ASCII diagrams showing data movement at each step
3. Mathematical proofs of communication complexity lower bounds
4. Algorithm families (multiple algorithms for the same operation, with comparison)
5. Implementation details (how the library actually implements it — channels, protocols)
6. Decision framework (which algorithm to choose when)

## Pitfall: iterative depth requests
User profile: will keep pushing for more depth even after you declare completion.
First output should be at "论文级深度" — don't save depth for round 2.
If you've declared completion 3+ times and user still pushes, firmly decline.
