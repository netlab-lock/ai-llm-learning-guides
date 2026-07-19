# 大规模HTML内容清理与修复工作流

## 适用场景
当200+个HTML文件需要同时清理通用模板内容并恢复分数时使用。

## 工作流（7步）

### Step 1: 结构性评分审计
写Python脚本扫描所有文件，计算五维度分数，输出每个文件的具体缺口。
```python
# 关键: 不仅输出总分，还要输出每个维度的细分损失
# 例如: chars(-5), h3(-3), code(-5), xref(-10)
```

### Step 2: 批量结构性修复（子agent并行）
- 3个子agent并行，每个处理~60个文件
- 添加exercise/forward/path/nav等缺失元素
- 每个子agent处理3-4个文件后需冷却（429限流）

### Step 3: 通用内容检测
扫描所有文件，统计以下通用内容的出现次数：
- 通用h3后缀（13种变体）
- 通用模板句子（"应用场景广泛"等）
- 通用tip/warn/deep（"餐厅吃饭"等）
- 文件内重复块
- 损坏HTML标签

### Step 4: 一次性清理
**关键: 一次性完成所有清理，不要分轮次！**
1. 去除所有通用h3后缀
2. 删除通用模板段落
3. 替换通用tip/warn/deep
4. 去除文件内重复块
5. 修复损坏HTML

### Step 5: 分数恢复
清理后大量文件会跌破S级。一次性补充：
1. 代码块（优先，每缺1个-5分）
2. ASCII图（每缺1个-5分）
3. 交叉引用链接（缺-10分）
4. tips（每缺1个-5分）
5. h3子节（每缺1个-1分）
6. h2节（每缺1个-3分）
7. 深度关键词段落

### Step 6: 深度内容质量验证
- 自动化: 搜索通用文本、检查短元素、检查损坏HTML
- 人工抽查: 读取3-5个文件的实际内容，确认主题相关

### Step 7: 最终确认
运行全量审计脚本，确认所有检查项通过。

## 评分瓶颈分析技术

当文件分数接近但未达S级时，需要精确分析哪个评分组件是瓶颈：

```python
def analyze_bottleneck(filepath):
    """分析文件的具体评分瓶颈，返回按损失排序的组件列表"""
    # ... 计算所有指标 ...
    
    losses = []
    if cc < 8000: losses.append(('chars', 25 - d1_text))
    if h2 < 5: losses.append(('h2', 15 - min(15, h2*3)))
    if h3 < 10: losses.append(('h3', 10 - min(10, h3)))
    if tbl < 3: losses.append(('tables', 15 - min(15, tbl*5)))
    if pre < 3: losses.append(('code', 15 - min(15, pre*5)))
    if dk < 10: losses.append(('deep_kw', 20 - min(20, dk*2)))
    if tip < 3: losses.append(('tips', 15 - min(15, tip*5)))
    if warn < 2: losses.append(('warns', 10 - min(10, warn*5)))
    if deep < 2: losses.append(('deeps', 15 - min(15, deep*5)))
    if asc < 3: losses.append(('ascii', 15 - min(15, asc*5)))
    if ex == 0: losses.append(('exercise', 10))
    if fw == 0: losses.append(('forward', 10))
    if cr < 10: losses.append(('xref', 10 - min(10, cr)))
    if no_path: losses.append(('path', 5))
    
    losses.sort(key=lambda x: -x[1])
    return losses  # 按损失从大到小排序
```

**优先修复顺序**（按每分投入产出比）：
1. **交叉引用链接** — 加3个`<a href>`即可获得+10分，投入产出比最高
2. **学习路径/向前串联** — 各加一句话即可获得+5/+10分
3. **代码块** — 需要写真实代码，每缺1个-5分
4. **ASCII图** — 需要画图，每缺1个-5分
5. **tips/warns** — 需要写≥50字的内容，每缺1个-5分
6. **h3子节** — 需要写段落，每缺1个-1分
7. **h2节** — 需要写整个章节，每缺1个-3分

## 关键原则
1. **先清理后补充** — 不要在有通用内容的文件上继续添加
2. **一次性清理** — 不要"清理→检查→清理→检查"循环
3. **主题相关** — 所有新增内容必须与文件h2主题相关
4. **用户信号** — 用户反复确认"确定完成了吗"= 有未发现的质量问题
5. **死链检测** — 分数达标后必须检查交叉引用链接是否有效
