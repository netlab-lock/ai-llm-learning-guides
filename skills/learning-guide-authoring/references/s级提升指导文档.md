# 学习指南S级质量提升 — 统一指导文档

## 任务目标

将HTML学习指南的质量从B级(300-379分)提升到S级(≥450分)或A+级(尽可能高分)。

## 评分标准 (五维度，每维度100分，总分500)

### 维度1: 内容密度 (100分)
| 指标 | 分值 | 满分标准 | 当前常见问题 |
|------|------|---------|-------------|
| 纯文字数 | 25 | ≥8000字 | 大部分4000-6000字 |
| h2节数 | 15 | ≥5个 | 基本达标 |
| h3子节数 | 10 | ≥10个 | 大部分3-6个 |
| 表格数 | 15 | ≥3个 | 大部分1-2个 |
| 代码块数 | 15 | ≥3个 | 大部分0-1个 |
| 深度关键词 | 20 | ≥5处(公式/推导/证明/原理/工作机制) | 大部分2-3处 |

**升级方法**:
- 每个h2节增加h3子节（2-3个），补充深入分析
- 每个文件至少3个代码块（Python/bash/伪代码）
- 每个文件至少3个对比表格
- 增加"公式/推导/原理/为什么/数学本质"等深度标记

### 维度2: 教学设计 (100分)
| 元素 | 分值 | 满分标准 | 当前常见问题 |
|------|------|---------|-------------|
| tip(通俗类比) | 15 | ≥3个，每个h2节独特 | 通用模板复制 |
| warn(常见误区) | 10 | ≥2个 | 通用模板复制 |
| deep(深入探讨) | 15 | ≥2个 | 缺具体数字/公式 |
| ASCII/SVG图 | 15 | ≥3个 | 大部分1-2个 |
| 表格对比 | 10 | ≥2个 | 大部分1个 |
| 练习/思考题 | 10 | 有 | 几乎全部缺失 |
| 向前串联 | 10 | 有 | 几乎全部缺失 |
| 交叉引用 | 10 | 有 | 大部分缺失 |
| 学习路径 | 5 | 有 | 缺失 |

**关键: 每个h2节的教学元素必须是该节主题独有的，不能复制通用模板！**

### 维度3: 结构完整性 (100分) — ✅ 已满分100分
- 章节覆盖完整: 20分 ✅
- index.html存在: 10分 ✅
- 前后导航链接: 15分 ✅
- 大小一致性: 15分 ✅
- 无空壳文件: 20分 ✅
- CSS风格统一: 10分 ✅
- 目录结构规范: 10分 ✅

### 维度4: 知识准确性 (100分) — 固定75分(需人工确认)
- 模型版本/参数准确: 25分
- 基准测试数据有出处: 20分
- 无过时信息: 20分
- 技术描述准确: 20分
- 限制性说明: 15分

### 维度5: 可读性 (100分) — 固定85分(已有暗色主题)
- CSS暗色主题正确: 15分 ✅
- 段落长度适中: 15分 ✅
- 标题层级清晰: 15分 ✅
- 移动端适配: 10分 ✅
- 代码块有语法高亮: 10分
- 表格可读: 10分 ✅
- 无死链: 15分
- 无孤立页面: 10分

**因此最高可达: 100+100+100+75+85 = 460分 (S级)**

## 等级划分
| 总分 | 等级 | 含义 |
|------|------|------|
| 450-500 | S | 标杆级 |
| 380-449 | A | 优秀 |
| 300-379 | B | 合格 |
| 200-299 | C | 薄弱 |
| <200 | D/F | 空壳 |

## 提升策略

### S级目标文件 (当前≥380分，差距≤80分)
精确补充缺失项:
- 字数不足 → 在现有h2节下新增h3子节，补充深入分析
- 表格不足 → 新增对比数据表
- 图解不足 → 新增ASCII架构图
- tip/warn/deep不足/重复 → 为每个h2节补充独特教学元素

### A+级目标文件 (当前<380分)
尽量提分:
- 所有h2节都应有独特tip+warn+deep
- 每个文件至少3个对比表格
- 每个文件至少2个ASCII图
- 每个文件至少3个代码块
- 字数尽量充实(≥6000字)

## 教学元素写法规范

### tip (通俗类比) — 好例子
```html
<div class="tip"><strong>通俗类比：</strong>
KV Cache就像你做数学题时的草稿纸。每算一步，你把中间结果写在纸上，
后面步骤直接查就行，不用从头算。映射关系：草稿纸=显存中的KV Cache，
中间结果=K/V向量，翻找笔记=注意力计算，纸张大小=显存容量。
</div>
```

### warn (常见误区) — 好例子
```html
<div class="warn"><strong>常见误区：</strong>
很多人以为KV Cache只是"缓存"，删了也无所谓。实际上没有KV Cache，
每生成一个token都要重新计算所有之前token的K和V，时间复杂度从O(1)
退化到O(n²)，推理速度下降100倍以上。这不是优化，是必需品。
</div>
```

### deep (深入探讨) — 好例子
```html
<div class="deep"><strong>深入探讨：</strong>
KV Cache的显存公式为：2 × n_layers × n_heads × d_head × seq_len ×
batch_size × bytes_per_element。以LLaMA-70B为例(80层、64头、128维、FP16)，
单条4K序列的KV Cache约10.7GB。batch_size=32时需要342GB显存，
远超单卡容量——这就是为什么KV Cache量化和PagedAttention如此重要。
</div>
```

### ASCII图 — 好例子
```html
<div class="ascii">
KV Cache工作原理
Step 1: Prefill (处理 "我爱")
  Cache: K=[k_我, k_爱]  V=[v_我, v_爱]

Step 2: Decode (生成 "中国")
  K_cache = [k_我, k_爱, k_中]  ← 拼接，无需重新计算旧token
  Attention = softmax(Q × K_cache^T) × V_cache

Step 3: Decode (生成 "的")
  Cache追加: K=[..., k_的]  V=[..., v_的]
  ※ 旧token的K/V直接复用，节省大量计算
</div>
```

### ❌ 坏例子（通用模板，必须避免）
```html
❌ <div class="tip">本节概念是理解现代LLM系统的重要一环...</div>
❌ <div class="tip">LLM推理就像去餐厅吃饭...</div>  ← 每个节都用同一个
❌ <div class="warn">不要认为这只是理论知识...</div>
❌ <div class="deep">从更深层次来看，这个技术代表了AI领域的重要趋势。</div>
```

## CSS模板

### Style A (box格式 — 推荐)
```css
.box.tip{background:rgba(63,185,80,0.08);border-left:4px solid #3fb950;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}
.box.warn{background:rgba(210,153,34,0.08);border-left:4px solid #d29922;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}
.box.deep{background:rgba(188,140,255,0.08);border-left:4px solid #a371f7;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}
```

### Style B (暗色背景)
```css
.tip{background:#0d2818;border-left:4px solid #3fb950;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}
.warn{background:#2d1b00;border-left:4px solid #d29922;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}
.deep{background:#1a1024;border-left:4px solid #a371f7;padding:12px 16px;margin:15px 0;border-radius:0 8px 8px 0}
.ascii{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:16px;margin:15px 0;font-family:'Courier New',monospace;font-size:0.85em;line-height:1.4;white-space:pre;overflow-x:auto}
```

## 执行方法（逐文件升级清单）

对每个文件执行：
1. **读取文件**，理解每个h2节的主题
2. **统计当前指标**（字数/h2/h3/表格/代码/tip/warn/deep/ascii）
3. **计算当前分数**，识别缺失项
4. **为每个h2节**编写独特的tip/warn/deep（替换通用模板）
5. **增加h3子节**（每个h2下2-3个，补充深入分析）
6. **增加代码块**（至少3个，Python/bash/伪代码）
7. **增加对比表格**（至少3个，含具体数据）
8. **增加ASCII图**（至少2个，与内容相关）
9. **增加思考题**（文件末尾2-3道，带`class="exercise"`）
10. **增加向前串联**（说明"这个知识后面怎么用"）
11. **增加交叉引用**（`href`链接到相关模块）
12. **检查CSS**是否包含tip/warn/deep/ascii类定义
13. **检查导航**（上一章/下一章链接）
14. **写回文件**，验证分数提升

## 进度追踪

- 每处理完一个子目录，运行质量检查确认分数提升
- 每处理10个文件报告一次进度
- 优先处理低分文件(C/D级)，再处理B级
