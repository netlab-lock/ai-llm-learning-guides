# Batch B-Level Enhancement Workflow

将大量B级HTML文件（有CSS但缺教学元素）批量升级为A级。

## When to use

用户说"补充教学元素"、"增强B级文件"、"给h2节加tip/warn/deep"、"批量增强"时使用。

## 前提条件

- 已有质量审计结果（参见 `learning-guide-quality-rubric`），知道哪些文件是B级
- 文件使用暗色主题HTML，已有基本CSS和h2结构
- 每个h2节后需要插入5种教学元素

## 脚本位置

`scripts/enhance-b-level-files.py` — 完整可运行脚本，含42+主题模板库。

## 工作流

### Phase 1: 统计B级文件数量

```bash
# 统计各目录B级文件数（有CSS但无教学元素）
for dir in /path/to/guide/*/; do
  total=$(find "$dir" -name "*.html" | wc -l)
  has_tip=$(grep -rl 'class="tip"\|class="warn"\|class="deep"' "$dir" 2>/dev/null | wc -l)
  b=$((total - has_tip))
  echo "$dir: $total total, $has_tip A-level, $b B-level"
done
```

### Phase 2: Dry-run测试

```bash
# 先在一个文件上测试
python3 scripts/enhance-b-level-files.py /path/to/file.html --dry-run

# 再在一个目录上测试
python3 scripts/enhance-b-level-files.py /path/to/dir/ --dry-run
```

### Phase 3: 批量处理（delegate_task并行）

```python
# 3个并行子代理，每个处理不同目录
delegate_task(tasks=[
  {"goal": "Run: python3 /path/to/script.py '/path/to/dir1/'", "toolsets": ["terminal"]},
  {"goal": "Run: python3 /path/to/script.py '/path/to/dir2/'", "toolsets": ["terminal"]},
  {"goal": "Run: python3 /path/to/script.py '/path/to/dir3/'", "toolsets": ["terminal"]},
])
```

### Phase 4: 修复遗漏

```bash
# 检查仍有遗漏的文件
for dir in /path/to/guide/*/; do
  remaining=$(find "$dir" -name "*.html" -exec grep -L 'class="tip"\|class="warn"\|class="deep"' {} \; | wc -l)
  [ "$remaining" -gt 0 ] && echo "$dir: $remaining remaining"
done

# 常见遗漏原因：
# 1. 文件有CSS但无教学元素（检测逻辑太松）→ 重新运行脚本
# 2. index.html无h2标签 → 正常跳过，不需要增强
# 3. 文件名不在扫描路径中 → 扩大扫描范围
```

### Phase 5: 验证

```bash
# A级文件比例
total=$(find /path/ -name "*.html" | wc -l)
a_level=$(grep -rl 'class="tip"\|class="warn"\|class="deep"' /path/ 2>/dev/null | wc -l)
echo "A-level ratio: $((a_level * 100 / total))%"

# HTML结构平衡
for f in /path/to/sample/*.html; do
  opens=$(grep -c '<html\|<div\|<h2\|<table' "$f")
  closes=$(grep -c '</html>\|</div>\|</h2>\|</table>' "$f")
  [ "$opens" != "$closes" ] && echo "UNBALANCED: $f (opens=$opens, closes=$closes)"
done
```

## 关键Pitfalls

### 1. CSS子串匹配陷阱

**问题**: `.callout.tip {` 包含子串 `.tip {`，导致脚本误认为已有独立 `.tip` CSS。

**修复**: 使用负向后瞻regex `(?<![a-zA-Z0-9_-])\.tip\s*\{` 匹配独立类定义。

### 2. CSS-only文件检测

**问题**: 文件有CSS定义（`.tip {`）但没有教学元素（`class="tip"`），原逻辑跳过了这些文件。

**修复**: B级文件检测必须同时检查CSS定义和实际教学元素。只有两者都存在才算A级。

### 3. CSS注入不写入

**问题**: 当所有h2节已有教学元素时，脚本返回skip但不写入新注入的CSS。

**修复**: 即使无section插入，如果CSS被修改（`css_added=True`），也必须写入文件。

### 4. Index文件误处理

**问题**: `index.html`通常是目录页，无h2标签，不需要教学元素。

**修复**: 脚本自动跳过无h2文件。但如果index有h2且需要增强，脚本也会处理。

### 5. 插入位置偏移

**问题**: 从前往后插入教学元素会导致后续h2的end_pos偏移。

**修复**: 从后往前插入（按pos降序），避免位置偏移。

### 6. 教学内容上下文相关性

**问题**: 基于h2标题文本的关键词匹配可能不够精确（如"推理"可能匹配到多个类别）。

**修复**: 关键词匹配同时扫描h2文本和文件路径，优先匹配更具体的关键词。42+主题覆盖主要LLM/AI领域。

## 规模参考

| 目录 | 文件数 | h2节数 | 处理时间 |
|------|--------|--------|---------|
| 推理框架(11子目录) | 70 | 355 | ~16s |
| 国产LLM系列(17厂商) | 294 | 1669 | ~36s |
| 国际LLM(5厂商) | 45 | 221 | ~42s(含DeepSeek等) |
| 推理优化其他(5子目录) | 53 | 297 | ~42s |
| 模型架构+硬件+基础设施 | 49 | 269 | ~24s |
| 集合通信+经典优化+工具 | 32 | 257 | ~20s |

总计: 553文件, 3160个h2节, ~2分钟(3并行)

## 与quality-rubric的关系

本workflow是 `learning-guide-quality-rubric` 中"维度2: 教学设计"的自动化实现。
rubric定义评分标准，本workflow提供批量修复能力。
