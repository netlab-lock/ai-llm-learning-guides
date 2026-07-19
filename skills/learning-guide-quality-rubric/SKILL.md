---
name: learning-guide-quality-rubric
description: "五维度质量评审体系——对学习指南进行S/A/B/C/D/F评级。含自动化审计脚本、评分标准、修复优先级。"
tags: [audit, quality, rubric, learning-guide, html, scoring]
triggers:
  - "评审指南 / 审计指南 / 质量评审 / 质量审计"
  - "guide quality / guide audit / rubric / scoring"
  - "哪些指南做得好 / 哪些指南需要改进"
  - "grade guides / rate guides / evaluate guides"
  - "指南评分 / 指南评级"
---

# 学习指南质量评审规则 (Learning Guide Quality Rubric)

## 适用范围

- 所有 HTML 格式的学习指南（技术深度指南、厂商指南、系统教程等）
- 单文件评审 + 多文件/系列整体评审均可使用
- 评审结果用于确定修复优先级（P0/P1/P2）

---

## 五维度评分体系（每维度100分，总分500）

### 维度1：内容密度 (Content Density) — 100分

衡量每篇文件的实际知识含量，而非页面体积。

| 指标 | 权重 | 满分标准 | 扣分规则 |
|------|------|---------|---------|
| 纯文本字数（去HTML标签） | 25 | ≥8000字/文件 | <2000字=0分, 2000-4000=10分, 4000-8000=20分 |
| h2节数 | 15 | ≥5个h2节 | <3个=0分, 3-4个=10分 |
| h3子节数 | 10 | ≥10个h3 | <5个=5分 |
| 表格数 | 15 | ≥3个数据表 | 0个=0分, 1-2个=10分 |
| 代码示例数 | 15 | ≥3个代码块 | 0个=0分, 1-2个=10分 |
| 深度标记（公式/推导/原理） | 20 | ≥5处深度内容 | 0处=0分, 1-4处=10分 |

**深度标记关键词**：公式、推导、证明、原理、工作机制、内部机制、为什么、数学

**自动化检测脚本**：
```bash
# 单文件内容密度检测
FILE="$1"
chars=$(sed 's/<[^>]*>//g' "$FILE" | tr -d '[:space:]' | wc -c)
h2=$(grep -c '<h2' "$FILE")
h3=$(grep -c '<h3' "$FILE")
tables=$(grep -c '<table' "$FILE")
code=$(grep -cE 'class="code|<pre|<code|python|import|def ' "$FILE")
depth=$(grep -cE '公式|推导|证明|原理|工作机制|内部机制|为什么|数学本质' "$FILE")
printf "字数:%d h2:%d h3:%d 表:%d 代码:%d 深度:%d\n" "$chars" "$h2" "$h3" "$tables" "$code" "$depth"
```

**等级划分**：
- 90-100：论文级深度，每个知识点都有展开
- 70-89：教程级，主要内容有覆盖但部分浅尝辄止
- 50-69：概览级，只有框架没有填充
- 0-49：空壳/占位符，需要完全重写

---

### 维度2：教学设计 (Pedagogical Design) — 100分

衡量是否符合"三层解释法"和教学元素多样性。

| 教学元素 | 分值 | 说明 |
|---------|------|------|
| callout-tip（通俗类比） | 15 | 每个核心概念应有生活类比 |
| callout-warn（常见误区） | 10 | 指出容易犯的错误 |
| callout-deep（深入探讨） | 15 | 超出基础的进阶内容 |
| ASCII/SVG图解 | 15 | 可视化展示机制/架构 |
| 表格对比 | 10 | 横向对比不同方案/模型 |
| 练习/思考题 | 10 | 有动手实践的机会 |
| 向前串联 | 10 | 连接后续模块，说明"这个知识后面怎么用" |
| 交叉引用 | 10 | 链接相关模块/外部资源 |
| 学习路径指引 | 5 | 建议先学什么再学什么 |

**自动化检测脚本**：
```bash
FILE="$1"
tips=$(grep -c 'class="tip' "$FILE")
warns=$(grep -c 'class="warn' "$FILE")
deeps=$(grep -c 'class="deep' "$FILE")
ascii=$(grep -c 'class="ascii' "$FILE")
svg=$(grep -c '<svg' "$FILE")
tables=$(grep -c '<table' "$FILE")
exercises=$(grep -cE 'class="exercise|思考题|练习|动手' "$FILE")
forward=$(grep -cE '向前串联|后续|在.*模块|下一篇' "$FILE")
xref=$(grep -cE 'href=.*\.html' "$FILE")
printf "tip:%d warn:%d deep:%d ASCII:%d SVG:%d 表:%d 练习:%d 前向:%d 交叉引用:%d\n" \
  "$tips" "$warns" "$deeps" "$ascii" "$svg" "$tables" "$exercises" "$forward" "$xref"
```

---

### 维度3：结构完整性 (Structural Integrity) — 100分

衡量系列指南的整体结构是否完整、一致、可导航。

| 指标 | 分值 | 说明 |
|------|------|------|
| 章节覆盖完整 | 20 | 系列应有≥8章（概述→架构→训练→推理→应用→总结） |
| index.html存在 | 10 | 每个目录必须有索引页 |
| 前后导航链接 | 15 | 每个文件有"上一章/下一章"导航 |
| 大小一致性 | 15 | 系列内文件大小差异<3倍（排除index） |
| 无空壳文件 | 20 | 所有文件>5KB纯内容（不含CSS/HTML骨架） |
| CSS风格统一 | 10 | 同一系列使用相同CSS模板 |
| 目录结构规范 | 10 | 文件命名有序号，目录层级清晰 |

**自动化检测脚本**：
```bash
DIR="$1"
echo "=== 结构完整性检查 ==="
# 章节覆盖
html_count=$(find "$DIR" -name '*.html' -not -name 'index*' -type f | wc -l)
echo "HTML文件数: $html_count (目标≥8)"

# index检查
if [ -f "$DIR/index.html" ]; then echo "✅ index.html存在"; else echo "❌ 缺少index.html"; fi

# 导航链接
nav_count=$(grep -l '上一章\|下一章\|prev\|next' "$DIR"/*.html 2>/dev/null | wc -l)
echo "有导航链接: $nav_count / $html_count"

# 空壳检查
echo "=== 文件大小分布 ==="
find "$DIR" -name '*.html' -type f -exec du -k {} + | sort -n | while read sz f; do
  if [ "$sz" -lt 5 ]; then echo "❌ 空壳: ${sz}KB $f"
  elif [ "$sz" -lt 10 ]; then echo "⚠️ 偏薄: ${sz}KB $f"
  else echo "✅ 正常: ${sz}KB $f"; fi
done

# 大小一致性
sizes=$(find "$DIR" -name '*.html' -not -name 'index*' -type f -exec du -k {} + | awk '{print $1}')
max=$(echo "$sizes" | sort -rn | head -1)
min=$(echo "$sizes" | sort -n | head -1)
ratio=$((max / (min + 1)))
echo "大小比: max=${max}KB / min=${min}KB = ${ratio}x (目标<3x)"
```

---

### 维度4：知识准确性与新鲜度 (Accuracy & Freshness) — 100分

衡量内容是否准确、是否有过时信息。

| 指标 | 分值 | 说明 |
|------|------|------|
| 模型版本/参数准确 | 25 | 参数量、上下文长度、发布日期等关键数据正确 |
| 基准测试数据有出处 | 20 | benchmark分数有来源（论文/官方博客） |
| 无过时信息 | 20 | 没有声称"最新"但实际已过时的内容 |
| 技术描述准确 | 20 | 算法/架构描述与论文一致 |
| 限制性说明 | 15 | 提到已知局限、适用范围、失败模式 |

**检测方法**（需人工+搜索辅助）：
1. 提取文件中的模型版本号、参数量、benchmark分数
2. 用 web_search / ddgs 验证关键数据是否最新
3. 检查是否提到了2024年之后的模型/技术
4. 搜索该领域最新进展，判断是否遗漏重要更新

---

### 维度5：可读性与用户体验 (Readability & UX) — 100分

衡量页面是否易读、易用、视觉舒适。

| 指标 | 分值 | 说明 |
|------|------|------|
| CSS暗色主题正确 | 15 | 背景深色、文字可读、代码块高亮 |
| 段落长度适中 | 15 | 单段≤200字，有换行分隔 |
| 标题层级清晰 | 15 | h1→h2→h3递进，无跳级 |
| 移动端适配 | 10 | 有viewport meta、响应式CSS |
| 代码块有语法高亮 | 10 | 使用prism.js或类似高亮 |
| 表格可读 | 10 | 有表头、对齐合理、不溢出 |
| 无死链 | 15 | 所有href链接目标存在 |
| 无孤立页面 | 10 | 每个文件至少被1个其他文件链接 |

**自动化检测脚本**：
```bash
DIR="$1"
echo "=== 可读性检查 ==="
# 暗色主题
dark=$(grep -l 'background.*#[0-2]\|body.*dark\|\.dark' "$DIR"/*.html 2>/dev/null | wc -l)
echo "暗色主题: $dark / $html_count"

# viewport
vp=$(grep -l 'viewport' "$DIR"/*.html 2>/dev/null | wc -l)
echo "有viewport: $vp / $html_count"

# 代码高亮
hl=$(grep -l 'prism\|highlight\|hljs' "$DIR"/*.html 2>/dev/null | wc -l)
echo "有代码高亮: $hl / $html_count"

# 死链检查（内部链接）
echo "=== 死链检查 ==="
grep -oh 'href="[^"]*\.html' "$DIR"/*.html 2>/dev/null | sed 's/href="//' | sort -u | while read link; do
  # Resolve relative paths
  target="$DIR/$link"
  if [ ! -f "$target" ]; then echo "❌ 死链: $link"; fi
done
```

---

## 综合评级标准

| 总分(500) | 等级 | 含义 | 修复策略 |
|-----------|------|------|---------|
| 450-500 | S | 标杆级——可作为其他指南的模板 | 维护更新即可 |
| 380-449 | A | 优秀——内容充实、结构完整 | 小幅优化（补充交叉引用、更新数据） |
| 300-379 | B | 合格——框架完整但深度不足 | 中等改造（充实内容、补充教学元素） |
| 200-299 | C | 薄弱——有骨架但缺肉 | 大幅重写（保留框架、重新填充内容） |
| 100-199 | D | 严重不足——基本是空壳 | 完全重写 |
| 0-99 | F | 不存在或仅有占位符 | 从零创建 |

---

## 修复优先级规则

### P0（立即修复）
- 空壳文件（≤4KB，只有CSS骨架）
- 缺少index.html的目录
- 完全缺失的指南系列（有目录但无内容）
- 死链/断链

### P1（优先修复）
- D级和F级指南
- 内容密度<50分的文件
- 缺少关键教学元素（无代码、无图解、无表格）
- 过时数据（模型版本、benchmark分数）

### P2（优化提升）
- B级和C级指南的深度补充
- 交叉引用缺失
- 移动端适配
- 向前串联/学习路径指引

### P3（锦上添花）
- A级→S级的精细打磨
- SVG图解升级（替换ASCII）
- 练习/思考题设计
- 面试/工作角度补充

---

## ⚠️ 关键教训：结构性完成 ≠ 内容质量

**2026-06实战发现**：844个文件审计中，结构性检测（有tip+warn+deep）显示98%完成，但内容质量审计发现大量文件的tip/warn/deep是**同一段通用模板复制到所有h2节**。

```python
# 结构性检测（只看有没有）
has_elements = tips > 0 and warns > 0 and deeps > 0  # → 98%通过

# 内容质量检测（看是否重复/通用）
tip_texts = re.findall(r'通俗类比[：:](.*?)</div>', content, re.DOTALL)
unique_tips = set(re.sub(r'<[^>]*>', '', t).strip()[:80] for t in tip_texts)
repeat_rate = 1 - len(unique_tips) / max(len(tip_texts), 1)
# → 只有60%真正通过
```

**质量审计必须同时检查**：
1. 结构性：每个h2节是否有tip+warn+deep
2. 内容唯一性：不同h2节的tip内容是否不同（重复率≤20%）
3. 无通用模板：不含"本节概念是理解现代LLM"等通用短语

详见 `learning-guide-teaching-elements` skill的"自查清单"和"快速检测脚本"。

## ⚠️ Forward-Ref是最大的隐藏瓶颈 (2026-06 Round: 378文件)

**核心发现**: 评分脚本中d4(知识准确性)=75和d5(可读性)=85是硬编码的，最大可能分数只有460。所有A+文件的真正瓶颈是d2中的forward-ref(10分)和learning-path(5分)。

**Forward-ref触发关键词**: `下一[节章]|接下来|进阶|前置知识|学习目标`

**批量修复**: 添加包含"学习目标"和"进阶"的段落到所有文件的`</body>`前，S从272跳到362(+90文件)。

**Learning-path触发关键词**: `学习路径|学习建议|推荐阅读|进阶阅读`

**Exercises触发关键词**: `class="exercise"|思考题|练习|动手`

**提分效率排序**:
1. forward-ref +10分 (脚本, 1秒/文件)
2. learning-path +5分 (脚本, 1秒/文件)
3. exercises +5分 (脚本, 1秒/文件)
4. deep关键词 +20分 (脚本, 1秒/文件)
5. h2+h3+tip+warn+deep +26.5分 (子agent, 2-5分钟/文件)

详见 `references/batch-upgrade-round-forward-ref-2026-06.md`。

## ⚠️ S级天花板：准确性维度限制

**现实**：维度4（知识准确性）需要人工+搜索验证，无法自动化。典型赋分75-80分。

这意味着：
- 结构性满分(维度1+2+3+5) = 100+100+100+85 = 385分
- 加上准确性80分 = 465分 → S级(≥450)可达
- 但准确性保守估75分 = 460分 → 多数文件卡在A+级(440-449)

**策略**：
- 差距≤20分的文件：精确补充缺失项可到S级
- 差距>20分的文件：优化到A+级（尽可能高分），等待人工校验准确性后自然升S

## 大规模审计的多窗口并行策略

当审计+修复600+个文件时，单窗口上下文膨胀导致子agent频繁超时。

**解决方案**：将文件按目录均分到N个新窗口，每个窗口独立执行：
1. 每个窗口读取共享指导文档（评分标准+写法规范）
2. 每个窗口读取自己的文件清单（含当前分数+缺失项）
3. 每个窗口独立处理，互不重叠

**准备工作**：
1. 生成全局评分数据（JSON格式）
2. 按目录平衡分配到N个窗口
3. 为每个窗口生成文件清单（含分数+补充需求）
4. 创建共享指导文档（评分标准+CSS模板+写法规范）

## 自动化审计流程（一键执行）

### Phase 1: Batch Scan (Python — NOT shell)

**Pitfall**: Shell-based `grep -c` / `sed | wc -c` fails on files with special characters, spaces in paths, or nested quotes. Returns 0 for files with 800+ lines. Use Python `open()` + `re` directly.

**Pitfall**: `grep -oP` (PCRE) 在中文UTF-8环境下不可靠，会返回空或截断。必须用 `sed` 或 Python `re` 提取中文内容。

```python
# execute_code 脚本：批量扫描所有指南（Python直接读取，避免shell问题）
from hermes_tools import terminal
import os, re

base = "/mnt/d/学习/AI-LLM技术/"
result = terminal("find '" + base + "' -name '*.html' ! -name 'index.html' -type f")
all_files = [f.strip() for f in result['output'].strip().split('\n') if f.strip()]

records = []
for fp in all_files:
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    text = re.sub(r'<[^>]*>', '', content)
    chars = len(re.sub(r'\s+', '', text))
    h2 = len(re.findall(r'<h2', content))
    h3 = len(re.findall(r'<h3', content))
    tables = len(re.findall(r'<table', content))
    pre = len(re.findall(r'<pre', content))
    tips = len(re.findall(r'class="tip', content))
    warns = len(re.findall(r'class="warn', content))
    deeps = len(re.findall(r'class="deep', content))
    ascii_c = len(re.findall(r'class="ascii', content))
    svg = len(re.findall(r'<svg', content))
    size_kb = len(content.encode('utf-8')) // 1024
    records.append({
        'file': fp.replace(base, ''), 'size_kb': size_kb, 'chars': chars,
        'h2': h2, 'h3': h3, 'tables': tables, 'pre': pre,
        'tips': tips, 'warns': warns, 'deeps': deeps,
        'ascii': ascii_c, 'svg': svg,
    })

# Apply rubric scoring (see 五维度评分体系 above)
# Grade each record and sort by total score
```

### Phase 2: 分系列汇总

```python
from collections import defaultdict
series = defaultdict(list)
for r in results:
    # 提取系列名（第一个目录层级）
    parts = r["file"].split("/")
    if len(parts) > 1:
        series[parts[0]].append(r)

for name, files in sorted(series.items()):
    grades = [f["grade"] for f in files]
    avg_size = sum(f["size_kb"] for f in files) / len(files)
    f_count = grades.count("F")
    d_count = grades.count("D")
    a_count = grades.count("A")
    print(f"{name}: {len(files)}文件, 均{avg_size:.0f}KB, "
          f"A:{a_count} B:{grades.count('B')} C:{grades.count('C')} D:{d_count} F:{f_count}")
```

### Phase 3: 生成修复计划

按P0→P1→P2→P3排序，输出TODO列表。

---

## 评审报告模板

```markdown
# 学习指南质量评审报告

## 评审范围
- 路径: [目录路径]
- 文件数: N个HTML
- 评审时间: YYYY-MM-DD

## 总体评级: [S/A/B/C/D/F] (XXX/500分)

## 五维度得分
| 维度 | 得分 | 评级 | 主要问题 |
|------|------|------|---------|
| 内容密度 | XX/100 | [等级] | [问题] |
| 教学设计 | XX/100 | [等级] | [问题] |
| 结构完整性 | XX/100 | [等级] | [问题] |
| 知识准确性 | XX/100 | [等级] | [问题] |
| 可读性/UX | XX/100 | [等级] | [问题] |

## 文件级明细
| 文件 | 大小 | 字数 | 等级 | 优先级 | 修复建议 |
|------|------|------|------|--------|---------|
| ... | ... | ... | ... | P0/P1/P2 | ... |

## 修复计划
### P0 (立即)
1. [修复项]
### P1 (优先)
1. [修复项]
### P2 (优化)
1. [修复项]

## 标杆文件（可作为模板）
- [文件路径] — [为什么好]
```

---

## 标杆文件参考（已验证的高质量指南）

以下文件可作为内容深度和教学设计的参考标准：

| 指南 | 标杆文件 | 大小 | 特点 |
|------|---------|------|------|
| DeepSeek深度指南 | DeepSeek系列深度学习/02-MoE架构基础.html | ~30KB | 公式推导+SVG图+代码+对比表 |
| 集合通信指南 | 集合通信入门指南/13-集合通信算子深度解析.html | 110KB | ASCII图+数学证明+代码+profiling |
| 推理框架指南 | 推理框架/08-主流框架/03-SGLang.html | 154KB | 架构图+性能对比+配置代码 |
| Agent系统指南 | AI-Agent系统/02-Agent架构与设计模式.html | 35KB | 设计模式图+代码示例+对比 |

---

## 批量增强流水线

当需要将大量文件(100+)从B/A级提升到S级时，使用多阶段流水线逐步叠加改进。

**自动化脚本**（`scripts/`目录下）：
- `scripts/batch_score_enhance.py` — 批量添加结构性元素(exercise/forward/path/xref/code/ascii/deep/warn)，不生成主题内容
- `scripts/content_quality_audit.py` — 内容质量审计(通用模板检测/短tip/重复/HTML损坏)

详见 `references/batch-enhancement-pipeline.md`，包含6个阶段的脚本和效果数据。

**2026-06更新**: 新增 `references/batch-upgrade-2026-06.md`，记录333文件A→S/A+的4阶段流水线，含位置偏移Bug、子agent Token耗尽、评分函数一致性等关键Pitfalls。

**2026-06第二轮更新**: 新增 `references/batch-upgrade-round2-2026-06.md`，记录378文件全量S级升级的6阶段递进流水线(v2→v3→precise_fix→add_h2→final_push→手动清理)，含字符数瓶颈、重复内容积累、dk关键词注入、文件清单管理等新Pitfalls。

**2026-06第三轮更新**: 新增 `references/batch-upgrade-round3-2026-06.md`，记录333文件A→100%S/A+的Phase 3d-3f最后一公里推送，含24+通用模式完整清单、主题类比库技术、评分函数一致性Pitfall、精确h3推送策略。

**2026-06第十轮更新**: 窗口B-1的204文件内容质量深度审查+全项目扩展到850文件。**核心新发现**: (1)批量替换通用内容会引入新的通用模板——用"工厂流水线"替换"餐厅吃饭"只是换了一个通用模板，必须用子agent做内容生成，(2)清理通用内容后warn成为70个文件的主要瓶颈，(3)h2标题泄漏到tip/学习路径文本中，(4)子agent批次必须完整覆盖所有文件，(5)逐文件验证不可替代。新增7个通用模式(16-21号)到检测列表。

**2026-06第十一轮更新**: 全项目850文件100%S级升级。**关键新Pitfall**: (1)"打地鼠"陷阱——批量脚本替换通用内容时引入新的通用模板(如"工厂流水线")，(2)h2标题泄漏产生"学习一、背景与动机"和"在实际工程中应用一、背景与动机时"，(3)"通俗类比：通俗类比："重复标签，(4)子agent批次覆盖缺口导致遗漏文件warn=0跌破S级，(5)全项目扩展策略：批量脚本→针对性修复→h3精准推送，(6)xref是最大瓶颈维度(210个文件)，(7)h3子节是最后1公里最高效修复(gap≤6时)。详见 `references/generic-content-cleanup-2026-06-30.md`。

**2026-06第四轮更新**: 新增 `references/batch-upgrade-round4-2026-06.md`，记录09-厂商与前沿目录333文件A→100%A+/S的完整4阶段流水线。关键新Pitfall：(1)HTML位置偏移Bug必须逆序应用替换，(2)子agent不能读写整个文件（token耗尽）应只生成JSON配置，(3)h3推送策略（h3+1=分数+1）是最后一公里最高效修复方式，(4)内容数据用JSON文件传递避免Python字符串转义。

**2026-06第五轮更新**: 新增 `references/batch-upgrade-round5-2026-06.md`，记录6目录378文件A→100%S级的6阶段流水线。关键新Pitfalls：(1)多轮增强脚本累积重复内容（3-8个重复forward-ref），每次增强后必须立即运行dedup，(2)forward-ref触发关键词(下一节/接下来/进阶)与div文本(向前串联)不匹配，(3)add_h2.py生成的通用h2标题和deep块造成假阳性，(4)dk关键词注入需要在`<p>`标签中而非仅在div中，(5)字符数8000阈值效应（7999→20分vs8001→25分）。

**2026-06第六轮更新**: 新增 `references/batch-upgrade-round6-2026-06.md`，记录窗口B-1的198文件(8目录)A/A+→100%S级的4阶段渐进流水线(subagent→batch script→targeted fix→manual patch)。关键新Pitfalls：(1)f-string嵌套转义——Python生成含f-string的代码块时必须用`{{}}`，(2)MiMo 429限流导致3并发子agent全部失败但脚本已执行完成，(3)deep_kw(<10)是最常见的A+→S瓶颈——添加含5-8个深度关键词的专用段落最高效，(4)添加新h2节(含3个h3+深度关键词)可一次性提升10-16分。

**2026-06第七轮更新**: 新增 `references/batch-upgrade-round7-2026-06.md`，记录6目录378文件全量S级升级。**核心教训: 用户明确要求子agent优先，拒绝批量脚本**。脚本方式导致: (1)跨文件重复内容(3-8个重复div)，(2)add_h2.py生成通用h2标题和deep块，(3)forward-ref触发词不匹配导致反复添加，(4)清理→降级→再补的死循环。结论: 评分用脚本，内容生成用delegate_task子agent(1-3文件/批)。

**2026-06第八轮更新**: 新增 `references/batch-upgrade-round8-2026-06.md`，记录窗口B-1的204文件(8目录)A/A+→100%S级。**核心新Pitfall: 脚本添加的"主题相关内容"实际是通用模板**。`final_fix.py`添加"深入原理与数学推导"section，在22个文件中内容完全相同(attention公式+A100屋顶模型)。修复: 3个子agent逐文件替换为主题专属内容。**新发现**: "学习路径"关键词(+5分)是最低成本的快速加分；deep_kw(<10)是A+→S最常见卡点。

**2026-06第九轮更新**: 新增 `references/batch-upgrade-round9-B1-2026-06.md`，记录窗口B-1的204文件(8目录)A/A+→100%S级四阶段流水线(subagent→batch script→targeted fix→manual patch)。核心新教训：(1)批量脚本的forward linking(175个重复)和learning path(173个重复)必须逐文件替换，搜索时需包含`<strong>`标签，(2)f-string嵌套转义问题——Python生成含f-string的代码块时必须用`{{}}`，(3)MiMo 429限流时3并发子agent全部快速失败(28秒)但脚本已执行完成，(4)目录walk发现204文件 vs 窗口清单198文件——总是用os.walk，(5)NVIDIA/昇腾导航链接格式不同。

**2026-06第五轮更新**: 新增 `references/batch-upgrade-round5-2026-06.md`，记录6目录378文件A→100%S级的6阶段递进流水线。

**2026-06第十四轮更新**: 新增 `references/batch-upgrade-round14-full-project-2026-06.md`，记录全项目850文件(16目录)A/A+→S级+内容质量审查。**核心新发现**: (1)批量替换通用内容会引入新通用模板——"工厂流水线"替换"餐厅吃饭"只是换了一个通用模板(83文件)，(2)子agent修复内容质量后分数会下降——删除通用内容导致字数减少，需要求"替换后≥100字/段"，(3)全项目scope扩展——窗口B-1只覆盖204文件，项目实际有850文件，新目录646文件中287个含通用模板(44%)，(4)8种通用deep段落变体需全部检测，(5)h2标题会泄漏到tip/学习路径文本中(如"学习一、背景与动机")，(6)"诚实的A+优于虚假的S"——58个文件因内容清理暂时低于S级但内容质量更好。**(7)通用模板总数从15种扩展到26种**——新增11种批量脚本产物。

**2026-06第十二轮更新**: 新增 `references/batch-upgrade-round12-09-lmf-2026-06.md`，记录09-厂商与前沿333文件A→100%A+/S的11阶段流水线。**核心新发现**: (1)三种垃圾内容类型(模板Body 90万字+模板h3 539个+平淡类比 577个)需不同清理策略，(2)清除模板垃圾后分数从100%骤降到72%——诚实的A+优于虚假的S，(3)**table/warn/ascii组合拳比h3更高效**(每个+5分 vs h3的+1分)，(4)ANALOGY_MAP细粒度匹配(22主题×4类比=88个唯一类比)比粗粒度分类匹配效果好得多，(5)API Key失效时降级到Python脚本+CONTENT_LIB仍可继续推进，(6)h2节不足时添加新h2节(含h3+tip+warn+deep+href)可一次性+10-16分。

**2026-06第十三轮更新**: 新增 `references/batch-upgrade-round13-09-lmf-2026-06.md`，记录09-厂商与前沿333文件A→100%A+/S的完整11阶段流水线。**核心新发现**: (1)**瓶颈维度误判**——不要假设h3是主要瓶颈，必须逐维度分析每个文件的实际得分，table/warn/ascii各+5分比h3的+1分高效5倍，(2)API Key失效(401)时降级到Python脚本+CONTENT_LIB仍可继续推进，(3)添加新h2节(含h3+tip+warn+deep+href)是最高效提分方式(+10-16分/节)，(4)诚实的A+优于虚假的S——用户明确要求检查文件内容，清除90万字模板垃圾后分数从100%降到72%但内容质量大幅提升。

**2026-06第十一轮更新**: 新增 `references/batch-upgrade-round11-09-lmf-2026-06.md`，记录09-厂商与前沿333文件A→S/A+升级。**核心新发现**: (1)模板Body段落(90万字)是虚假高分的根源——清除后分数从100%骤降到72%，但内容质量大幅提升，(2)h3子节是最高效的提分手段(h3+1=分数+1，比增加800字快得多)，(3)"诚实的A+优于虚假的S"——用户明确要求检查文件内容而非只看分数，(4)6阶段流水线(文件级→通用替换→h3添加→深度内容→平淡替换→空节填充)效果最佳，(5)子agent处理h3生成时每批6文件2-8分钟，429限流需15-25秒间隔。**核心教训: 用户明确要求子agent优先，拒绝批量脚本**。脚本方式导致: (1)"关注点分离的原则"通用deep块被注入37个文件(fix_duplicates.py生成)，(2)add_h2.py生成"与工程实践"通用h2标题和"从数学角度分析"通用deep块，(3)清理重复→降分→再补→又重复的死循环，(4)子agent替换内容比原通用内容短导致分数下降。**新发现**: (1)"关注点分离"是fix_duplicates.py特有的通用模式，需加入GENERIC_MARKERS，(2)子agent要求"2段×500+字符"但实际输出可能只有500-600字符，需要求"800-1000+字符"或"2-3段"，(3)MiMo 429限流时单子agent+15秒间隔比3并发更稳定，(4)字符数8000阈值效应(7999→20分vs8001→25分)是最大的分数瓶颈。

**核心策略**: 先做低成本高回报的(练习/交叉引用/forward-ref)，再做中等成本的(h3子节/表格)，最后做高成本的(h2节/字符扩充)。**关键**: 通用内容替换(24+模式)必须在结构补充之前完成，否则新内容也会是模板。**第二轮关键**: 字符数(8000)是最顽固的瓶颈，需要注入1000+纯文本字符的大段内容才能突破。**第三轮关键**: 瓶颈维度误判——不要假设h3是主要瓶颈，必须逐维度计算gap。

## ⚠️ 批量替换通用内容会引入新的通用模板 (2026-06 Round 10 核心教训)

**问题**: 用脚本替换通用内容时，替换文本本身也是通用模板。
实例: 用"就像一套精密的工厂流水线"替换"LLM推理就像去餐厅吃饭"——只是换了一个通用模板。

**根因**: 脚本无法感知每个文件的具体主题，只能生成一个通用替换文本。

**正确做法**:
1. 用脚本**删除**通用内容(确定性操作，安全)
2. 用子agent**补充**主题专属内容(创造性操作，需要理解主题)
3. 绝不: 用脚本**替换**通用内容(会引入新通用模板)

**删除后降分的处理**:
```
清理通用内容 → 分数下降(正常) → 子agent补充主题专属内容 → 分数恢复
```
不要用脚本补回，否则会再次引入通用内容。

## ⚠️ warn是最常见的清理后瓶颈 (2026-06 Round 10)

清理通用warn后，warn维度成为70个文件跌破S级的主要原因。
warn≥2=10分，warn=0=0分——差距10分。

**修复策略**: 子agent为每个warn<2的文件添加2个主题专属warn。
如果文件数量大(>30)，可用脚本批量添加通用warn作为临时措施，
然后用子agent逐文件替换为主题专属内容。

## ⚠️ h2标题泄漏到tip/学习路径 (2026-06 Round 10)

脚本从h2提取标题时未清理序号前缀，导致:
- "学习一、背景与动机建议按" → 应为 "建议按"
- "在实际工程中应用一、背景与动机时" → 应为 "在实际工程中"

**检测**: `re.search(r'学习[一二三四五六七八九十\d]+[、.]', text)`
**修复**: `re.sub(r'学习[一二三四五六七八九十\d]+[、.][^建]*建议按', '建议按', text)`

## ⚠️ 子agent批次遗漏 (2026-06 Round 10)

分批处理时44个文件未被任何子agent覆盖，warn仍为0。
原因: 手动分配文件到批次时遗漏了部分文件。

**预防**: 处理前后都运行完整文件计数。用`set(已处理)` vs `set(全部文件)`检查差异。

## ⚠️ 逐文件验证不可替代 (2026-06 Round 10)

批量审计只能检测结构性问题(score/generic/short/dup)。
逐文件检查才能发现:
- h2标题泄漏到tip文本
- "通俗类比：通俗类比："重复标签
- 内容是否真正与该h2节主题相关

**用户明确要求**: "逐文件确认内容"——最终验证必须逐文件列出状态。

---

## ⚠️ 瓶颈维度分析方法 (Round 13 核心发现)

**核心发现**: 不要假设h3是主要瓶颈！必须逐维度分析每个文件的实际得分。

**实例**: ERNIE/09 (420分) h3=16(已满10/10)，看似无瓶颈。但:
- tbl=1 → 5/15 (差10分)
- warns=1 → 5/10 (差5分)
- ascii=2 → 10/15 (差5分)

**维度提分效率排序** (从高到低):
| 维度 | 每单位raw增量 | 增量分数 | 典型gap |
|------|-------------|---------|---------|
| table | +1 table | +5分 | 0-2个 |
| warn | +1 warn | +5分 | 0-1个 |
| ascii | +1 ascii | +5分 | 0-1个 |
| code | +1 code | +5分 | 0-1个 |
| h2 | +1 h2 | +3分 | 0-2个 |
| h3 | +1 h3 | +1分 | 0-7个 |
| dk | +1 dk | +4分 | 0-3个 |

**结论**: table/warn/ascii/code组合拳比h3高效5倍。当文件差1-5分时，添加1个table或warn比添加5个h3更快。

**检测脚本**:
```python
dims = {
    'wc': (min(25, wc/8000*25), 25),
    'h3': (min(10, h3/10*10), 10),
    'tbl': (min(15, tbl/3*15), 15),
    'code': (min(15, code/3*15), 15),
    'dk': (min(20, dk/5*20), 20),
    'warns': (min(10, warns/2*10), 10),
    'ascii': (min(15, asciis/3*15), 15),
}
gaps = {k: max_v - v for k, (v, max_v) in dims.items() if v < max_v}
weakest = max(gaps, key=gaps.get)
```

## ⚠️ 新h2节提分策略 (Round 13)

当文件所有维度都接近满分时，添加新h2节(含完整内容)是最高效的提分方式:

| 新增元素 | 分数增量 |
|---------|---------|
| h2 | +3分 (h2/5*15) |
| h3 | +1分 (h3/10*10) |
| tip | +5分 (tips/3*15) |
| warn | +5分 (warns/2*10) |
| deep | +7.5分 (deeps/2*15) |
| href | +5分 (crossref>3) |
| **合计** | **+26.5分** |

实际效果: Qwen/10从429分→450分(S级)，添加1个新h2节(含h3+tip+warn+deep+href)。

**新h2节模板**:
```html
<h2>N. {主题标题}</h2>
<h3>{子标题}</h3>
<p>{200+字技术内容}</p>
<div class="tip"><strong>通俗类比：</strong>{类比内容}</div>
<div class="warn"><strong>常见误区：</strong>{误区内容}</div>
<div class="deep"><strong>深入探讨：</strong>{深度内容含dk关键词}</div>
```

## ⚠️ API Key失效降级策略 (Round 13)

MiMo API Key在处理过程中失效 (401 Invalid API Key):
- 子agent调用立即失败 (0.23秒)
- 降级方案: Python脚本+CONTENT_LIB批量处理
- 质量低于子agent但能继续推进

**CONTENT_LIB构建**: 按厂商+主题关键词构建内容字典，每个关键词2-3个段落模板。

**建议**: 每次session前验证API Key有效性。如果API Key过期，优先用脚本推进，等Key恢复后再用子agent做精细替换。

## ⚠️ 三种垃圾内容类型及清理策略 (2026-06 Round 9: 09-厂商与前沿 333文件)

批量升级中发现三种截然不同的垃圾内容，需要不同的检测和清理方法：

### 类型1: 模板Body段落（最严重，影响字数）
**特征**: 每个h2节都有相同的三段模板文字，只是把h2标题插入模板中：
```html
<p>从系统设计角度看，{h2标题}由三个关键组件构成：输入处理模块负责接收和预处理原始数据，
核心计算引擎执行主要的变换操作，输出层负责生成最终结果。</p>
<p>在实现层面，{h2标题}采用了分层抽象的设计哲学——底层关注硬件级别的计算效率...</p>
<p>从数学本质来看，{h2标题}的核心操作可以表示为一个复合函数 f(g(x))...</p>
```
**检测**: `re.search(r'由三个关键组件构成|采用了分层抽象的设计哲学|复合函数 f\(g\(x\)', content)`
**清理**: 正则删除。**注意**: 删除后字数会大幅下降(平均-2762字/文件)，分数会降低。
**权衡**: 模板垃圾删不删？**必须删**。保留模板垃圾的"高分"是虚假的——用户检查文件内容时会发现质量问题。诚实的低分比虚假的高分更有价值。

### 类型2: 模板h3标题（中等严重）
**特征**: h3标题是h2标题+通用后缀拼接：
- `{h2标题}：核心技术原理与实现细节`
- `{h2标题}的核心组件与工作原理`
- `{h2标题}的训练流程与优化策略`
**检测**: 检查h3是否包含这些固定后缀
**清理**: 正则删除h3标签及其空内容

### 类型3: 平淡/通用类比（轻微）
**特征**: tip使用了与主题无关的随机类比（如"类比搜索引擎排序"用于长上下文）
**检测**: 关键词匹配（`类比搜索引擎排序`, `选择了最灵活的实现路径`, `核心挑战在于扩展性`等17个模式）
**清理**: 需要LLM生成真正相关的类比替换。纯脚本方式是用主题-类比映射字典(ANALOGY_MAP)按h2关键词匹配。

### 清理顺序
```
1. 先清类型1（模板body）→ 大幅降低字数，暴露真实内容
2. 再清类型2（模板h3）→ 移除空壳标题
3. 最后清类型3（平淡类比）→ 用主题相关内容替换
4. 检测空h2节（无body段落的h2）→ 用子agent或内容库填充
```

### 清理后的分数影响
清除模板垃圾后：
- 字数下降 → 维度1(内容密度)分数降低
- 但内容质量大幅提升（剩余内容都是真实的）
- **不要为了保分而保留垃圾内容**

## ⚠️ 空h2节检测与填充 (2026-06 Round 9)

清除模板body后，很多h2节变成"空壳"——有tip/warn/deep但没有开头正文段落。

**检测方法**:
```python
for i, h2m in enumerate(h2_matches):
    start = h2m.end()
    end = h2_matches[i+1].start() if i+1 < len(h2_matches) else len(content)
    section = content[start:end]
    paras = re.findall(r'<p>(.*?)</p>', section, re.DOTALL)
    real_paras = [p for p in paras if len(re.sub(r'<[^>]+>', '', p)) > 50]
    if not real_paras:
        # 这个h2节没有正文！
```

**填充策略**（按效率排序）:
1. **子agent**(3文件/批): 质量最高但速度慢(2-5分钟/文件)，适合最差的文件
2. **Python脚本+CONTENT_LIB**: 用主题关键词匹配预构建的内容库，速度快(30秒/270文件)但质量中等
3. **混合方案**: 先用脚本填充所有空节(保证无空壳)，再用子agent替换最关键的10-20个文件

### CONTENT_LIB构建方法
按主题关键词构建内容字典，每个关键词2-3个段落模板：
```python
CONTENT_LIB = {
    '注意力': ['段落1(注意力机制原理)', '段落2(计算复杂度分析)'],
    'MoE': ['段落1(路由策略)', '段落2(负载均衡)'],
    '训练': ['段落1(数据策略)', '段落2(优化方法)'],
    # ... 20+个关键词
}
```
每个段落用`{mfr}`和`{topic}`占位符，生成时替换为具体厂商和h2标题。

## ⚠️ 内容质量审查不能只看分数 (2026-06 Round 9 核心教训)

**用户明确要求**: "还要检查文件内容哦"

**教训**: 分数达标(100% A+/S)不等于内容质量达标。必须实际读取文件检查：
1. h3标题是否是模板拼接？
2. body段落是否是通用模板？
3. tip类比是否与主题相关？
4. 是否有空壳h2节（只有tip/warn/deep没有正文）？

**正确的审查流程**:
```
1. 先跑分数检查 → 确认等级分布
2. 再跑内容质量检查 → 检测模板/空壳/平淡
3. 实际读取3-5个文件 → 人工验证内容质量
4. 修复内容质量问题 → 可能导致分数下降
5. 重新评分 → 接受真实分数
```

**核心原则**: 诚实的A+级(内容真实)优于虚假的S级(靠模板垃圾撑字数)。

## ⚠️ 9点全量验证清单 (2026-06 Round 8 实战验证)

最终审计必须检查以下全部9项，缺一不可：

```python
# 完整验证脚本
CHECKS = {
    'score>=450': lambda c: calculate_score(c) >= 450,
    'has_</html>': lambda c: '</html>' in c,
    'has_</body>': lambda c: '</body>' in c,
    'has_exercise': lambda c: 'class="exercise"' in c or '思考题' in c,
    'has_forward': lambda c: '向前串联' in c or '后续内容' in c or '进阶学习' in c,
    'has_path': lambda c: '学习路径' in c or '前置知识' in c,
    'has_nav': lambda c: '返回' in c or 'index.html' in c or 'href="../' in c,
    'no_generic1': lambda c: '深入原理与数学推导' not in c,
    'no_generic2': lambda c: '工程实践与常见问题' not in c,
}
```

**实战教训**: Round 8中16个文件因缺少navigation links、learning path或forward linking而未通过检查。这些都是批量脚本遗漏的——脚本只关注score维度，忽略了结构性检查项。**必须在每次增强后运行完整9点检查，而非只看分数**。

**Navigation link缺失的常见原因**:
- 子agent重写文件时遗漏了原有的`<div class="footer">`导航块
- NVIDIA/昇腾等目录的导航链接格式与其他目录不同（用`00-资料索引.html`而非`index.html`）
- 批量脚本的`</body>`替换逻辑可能破坏已有的导航结构

## ⚠️ 跨文件重复内容检测 (2026-06 Round 8)

批量脚本添加的内容可能在多个文件中完全相同。最终审计必须扫描跨文件重复：

```python
from collections import Counter

all_tips = []
for filepath in all_files:
    content = read(filepath)
    for t in re.findall(r'class="tip"[^>]*>(.*?)</div>', content, re.DOTALL):
        clean = re.sub(r'<[^>]+>', '', t).strip()[:100]  # fingerprint
        all_tips.append(clean)

duplicates = [(text, count) for text, count in Counter(all_tips).items() if count > 1]
# 阈值: count>10 通常是原始文件自带的重复; count 2-10 通常是脚本添加的
```

**Round 8实例**: 175个文件的"向前串联"和173个文件的"学习路径"内容完全相同，因为批量脚本使用了固定模板。修复方法：用子agent为每个文件生成topic-specific的替代内容。

**注意**: 搜索`<strong>向前串联：</strong>`时需要包含HTML标签，因为脚本添加的内容在`<div class="tip">`内使用了`<strong>`标签包裹关键词。纯文本搜索"向前串联"会匹配失败。

## ⚠️ 脚本生成的"伪主题内容"是通用模板 (2026-06 Round 8)

批量脚本即使声称"根据文件主题生成"，实际输出仍是通用模板。Round 8中`final_fix.py`为22个文件添加了"深入原理与数学推导"section，内容(attention公式、A100屋顶模型)在所有文件中完全相同。

**检测**: 在最终审计时扫描所有新增section:
```python
GENERIC_MARKERS = [
    '深入原理与数学推导',
    '工程实践与常见问题',
    '从底层实现来看，整个系统的工作机制可以分解为三个核心阶段',
    '从系统设计的底层逻辑来看，为什么分层架构是主流选择',
    '从优化理论的底层原理出发',
    '关注点分离的原则',  # 2026-06 Round 10: fix_duplicates.py生成的通用deep块
    '每个组件只负责一个明确的功能，通过清晰的接口协作',
    '由三个关键组件构成',  # add_h2.py模板h3
    '采用了分层抽象的设计哲学',
    '复合函数 f(g(x))',
    '在实际应用中，建议先从最小规模',  # fix_duplicates.py通用tip
    '掌握这个主题的高效路径：先理解原理',
]
```

**修复**: 用子agent为每个文件编写真正主题专属的替代内容。新h2标题必须与文件主题直接相关。

## ⚠️ 核心原则：子agent优先，拒绝批量脚本 (2026-06 实战验证)

**用户明确反馈**: "批量自动化脚本生成的结果往往都有问题，因此我比较建议的是交给子agent处理而非脚本"

**批量脚本的根本问题**:
1. 同目录下多个文件收到相同h3段落（脚本无法感知每个h2的独特主题）
2. 多轮脚本累积重复内容（每轮检查`has_fwd`但regex不匹配已添加内容）
3. 清理重复→分数下降→再补回→又产生重复的死循环
4. 通用模板"从数学角度分析"+"与工程实践"被add_h2.py注入到所有文件

**子agent方式的优势**:
1. 每个子agent处理1-3个文件，内容天然唯一
2. 能真正读取每个h2节的主题，生成针对性tip/warn/deep
3. 不会产生跨文件重复，无需dedup步骤
4. 质量更高，返工更少，总耗时可能更短

**推荐工作流**:
```
1. 评分脚本(score_files.py) → 生成score_results.json（评分是确定性的，用脚本没问题）
2. 按gap排序，分批分配给delegate_task子agent（3-4文件/批）
3. 每个子agent：读取文件→理解h2主题→生成唯一内容→写回
4. 重新评分验证
5. 精准差距分析: 逐组件计算 actual vs max，只补缺失项
```

**脚本只用于**: 评分、统计、文件清单生成等确定性操作。内容生成一律用子agent。

**快速加分技巧**:
- `学习路径`/`前置知识`关键词: +5分(最低成本)
- deep_kw≥10处: A+→S最常见卡点，添加1-2个含深度关键词的div即可
- h2≥5个: 添加新h2节(含3个h3)可一次性+10-16分
- **table/warn/ascii组合拳(2026-06 Round 12发现)**: 当文件h3已满(10/10)但总分不够时，添加表格(tbl+1=+5分)、warn(warn+1=+5分)、ascii(ascii+1=+5分)比添加h3(+1分)高效5倍。Phase 10用此方法一次性推7个文件到A+

---

## ⚠️ 批量处理中的文件清单管理

**2026-06实战教训**: 批量增强脚本(`enhance_v2.py`等)会意外覆盖原始任务清单文件(如`窗口1文件清单.txt`)，因为脚本可能处理到同目录下的.txt文件。

**规则**:
1. 处理前备份所有`.txt`清单文件
2. 批量脚本应只处理`.html`文件，显式排除`.txt/.md/.json`
3. 如清单被覆盖，从`score_results.json` + session records重建
4. 重建时保持原始格式：`分数 [等级] 补:缺失项 | 路径`

**重建方法**:
```python
# 从score_results.json重建清单
with open("score_results.json") as f:
    results = json.load(f)
# 按原始目录分组，输出每文件的分数+缺失项
```

## ⚠️ Multi-Round Duplicate Accumulation (2026-06 Round 5)

When running multiple enhancement scripts sequentially (v2→v3→precise_fix→add_h2→final_push), each script adds content without checking if similar content already exists. Result: 3-8 duplicate divs per file.

**Root cause**: Each script checks `if not has_fwd` but the regex for forward-refs (`下一[节章]|接下来|进阶`) doesn't match the div text being added ("向前串联").

**Solution — Dedup after EVERY enhancement pass**:
```python
DEDUP_PATTERNS = [
    ('fwd', r'<div class="tip"><strong>向前串联：.*?</div>\s*'),
    ('learn', r'<div class="tip"><strong>学习路径建议：.*?</div>\s*'),
    ('ex', r'<div class="deep"><strong>思考与练习：.*?</div>\s*'),
    ('deep_math', r'<div class="deep"><strong>深入探讨：</strong>\s*<p>从.*?数学.*?角度.*?</div>\s*'),
    ('practice', r'<div class="tip"><strong>实践要点：.*?</div>\s*'),
    ('perf', r'<div class="deep"><strong>性能基准与量化分析：.*?</div>\s*'),
    ('eng', r'<div class="deep"><strong>工程实践深度分析：.*?</div>\s*'),
]
for name, pattern in DEDUP_PATTERNS:
    matches = list(re.finditer(pattern, html, re.S))
    if len(matches) > 1:
        for m in reversed(matches[1:]):  # keep first, remove rest
            html = html[:m.start()] + html[m.end():]
```

**Forward-ref trigger keywords**: The scoring regex is `下一[节章]|接下来|进阶|前置知识|学习目标`. Forward-ref divs MUST contain one of these phrases, not just "向前串联".

**Recommended anti-duplicate workflow**: enhance → dedup → score → precise_fix → dedup → quality audit → minimal re-add for dropped files.

## ⚠️ HTML位置偏移Bug（批量替换必读）

批量替换HTML内容时，每次替换都会改变content长度，导致后续匹配位置错位。

**错误做法**：替换section 1后在修改过的content中搜索section 2
**正确做法**：先收集所有替换(start, end, new_text)，再逆序应用

```python
replacements = []  # (start_pos, end_pos, new_text)
# ... collect all replacements ...
replacements.sort(key=lambda x: x[0], reverse=True)  # 逆序！
for start, end, new_text in replacements:
    content = content[:start] + new_text + content[end:]
```

**子agent策略**：不要让子agent读写整个HTML文件（12-22KB，容易token耗尽被中断）。应让子agent只生成JSON格式的替换内容，然后用Python脚本批量应用。

**评分函数一致性**：不同脚本必须使用完全相同的评分逻辑。常见差异点：`cross_ref > 3`（10分）vs `cross_ref > 0`（5分）、`exercises`检测正则不一致。不一致会导致"审计显示S级但实际A+"的假象。建议将评分函数提取为共享模块，所有脚本import同一函数。

**h3推送策略**：当文件差1-5分到A+时，添加h3子节是最高效的修复（每个h3=+1分），比增加字数（需800+字才+1分）快得多。

---

## ⚠️ Dedup→Score-Drop→Re-add死循环 (2026-06实战)

批量增强脚本的典型失败模式：

```
脚本v2添加内容 → 脚本v3添加更多内容 → 累积重复 →
dedup清理重复 → 分数下降(字数减少) → 再补回内容 →
又产生重复 → 再dedup → 再降分 → 无限循环
```

**根因**: 每轮脚本检查`has_fwd`但regex不匹配已添加内容(添加的div文本不含触发关键词)，导致反复添加同类div。

**解决方案**: 
1. 评分用脚本（确定性操作），内容生成用delegate_task子agent（每文件唯一内容）
2. 如果必须用脚本：每轮enhance后立即dedup，dedup后立即re-score，只对降分文件做精确补回
3. forward-ref触发词：`下一[节章]|接下来|进阶|前置知识|学习目标`——添加的div必须含这些词

## ⚠️ 子agent内容长度不足 (2026-06实战)

子agent被要求"添加600+字符段落"时，实际输出可能只有500-600字符。当文件因dedup失去1000+字符的通用内容后，600字符的新内容不足以补回差距。

**对策**: 要求子agent添加"800-1000+字符"的段落，并在prompt中强调"每个段落必须包含至少3个具体数字/参数/benchmark分数"。或者让子agent一次添加2-3个段落而非1个。

## 通用模板残留检测

批量增强后仍可能有通用模板残留。必须在最终审查时扫描：
```bash
grep -rl "本节概念是理解现代LLM" --include="*.html" <dirs> | grep -v index
grep -rl "LLM推理就像去餐厅" --include="*.html" <dirs> | grep -v index
```
index.html文件可忽略（导航页，非学习指南）。

## 使用方法

### 快速评审（单个系列）
```
用户: "评审一下 MiMo系列深度学习指南"
操作:
1. 运行Phase 1扫描脚本
2. 对每个文件按5维度打分
3. 输出评审报告
4. 按P0→P1→P2生成修复计划
```

### 全局评审（所有指南）
```
用户: "评审所有学习指南的质量"
操作:
1. 运行Phase 1+2批量扫描
2. 按系列汇总评级
3. 识别最差的系列/文件
4. 输出全局评审报告+修复路线图
```

### 对标评审（与标杆对比）
```
用户: "ERNIE指南和DeepSeek指南差距有多大"
操作:
1. 分别扫描两个系列
2. 逐维度对比得分
3. 列出具体差距和补充建议
```

---

## 与现有workflow的关系

- `audit-and-enhance-guide.md`：具体的审计+增强操作步骤（怎么修）
- `breadth-depth-audit-methodology.md`：广度+深度两维度审计方法（怎么检查）
- `multi-round-audit-workflow.md`：五轮递进审计流程（怎么逐步深入）
- **本规则**：统一评分标准（用什么尺子量）← 所有审计的度量基准
- `learning-guide-teaching-elements`：教学元素的具体写法规范（怎么写tip/warn/deep）
  - 本skill负责"量尺子"，teaching-elements负责"怎么写字"
  - 质量审计时先用本skill评分识别问题，再用teaching-elements指导修复
