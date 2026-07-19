# 思考与练习模板 — 按主题分类

按文件主题自动匹配练习题模板。检测文件名中的关键词确定主题。

## 主题检测逻辑

```python
def get_topic_category(fname):
    fname = fname.lower()
    if any(w in fname for w in ['架构', 'attention', '注意力', '位置编码', '核心架构']):
        return '架构'
    elif any(w in fname for w in ['预训练', '训练', '数据', '训练策略']):
        return '训练'
    elif any(w in fname for w in ['对齐', '后训练', 'rlhf']):
        return '对齐'
    elif any(w in fname for w in ['推理', '部署', '量化', '系统工程']):
        return '推理'
    elif any(w in fname for w in ['评估', '基准', '性能']):
        return '评估'
    elif any(w in fname for w in ['应用', '生态', '场景']):
        return '应用'
    elif any(w in fname for w in ['论文', '精读', '学习资源']):
        return '论文'
    else:
        return 'default'
```

## 模板

### 架构
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请用自己的话解释{mfr}架构设计的核心创新点，并说明它与传统Transformer架构的区别。</li>
<li><strong>技术分析：</strong>分析{mfr}架构中各组件的工作原理和相互关系，说明为什么这样设计。</li>
<li><strong>对比思考：</strong>将{mfr}的架构方案与同时期其他厂商的方案进行对比，分析各自的优劣势和适用场景。</li>
<li><strong>实践应用：</strong>如果你要基于{mfr}的模型构建一个应用，你会如何利用其架构特点来优化性能和成本？</li>
</ol>
```

### 训练
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请解释{mfr}在预训练阶段使用的核心算法和数据处理策略。</li>
<li><strong>技术分析：</strong>分析{mfr}训练过程中可能遇到的稳定性问题及其解决方案。</li>
<li><strong>数据工程：</strong>{mfr}的数据清洗和过滤流程包含哪些关键步骤？每一步的技术原理是什么？</li>
<li><strong>实践应用：</strong>假设你要从零开始训练一个类似{mfr}的模型，你会如何规划训练数据和计算资源？</li>
</ol>
```

### 对齐
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请解释{mfr}使用的对齐训练方法（如RLHF/DPO），并说明其数学原理。</li>
<li><strong>技术分析：</strong>对齐训练中"奖励黑客"问题是如何产生的？{mfr}采用了什么策略来缓解？</li>
<li><strong>安全分析：</strong>分析{mfr}模型的安全对齐机制，评估其在边缘场景下的表现。</li>
<li><strong>实践应用：</strong>如何设计一个有效的红队测试方案来评估{mfr}模型的安全性？</li>
</ol>
```

### 推理
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请解释{mfr}在推理优化方面使用的核心技术及其数学原理。</li>
<li><strong>性能分析：</strong>计算{mfr}模型在不同配置下的显存占用和吞吐量，分析瓶颈所在。</li>
<li><strong>优化方案：</strong>如果{mfr}模型的推理延迟过高，你会从哪些维度进行系统性优化？</li>
<li><strong>实践应用：</strong>设计一个{mfr}模型的生产部署方案，考虑成本、延迟和可靠性的平衡。</li>
</ol>
```

### 评估
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请解释{mfr}模型评估使用的主要基准和评估方法。</li>
<li><strong>统计分析：</strong>计算{mfr}模型在MMLU基准上的95%置信区间，分析分数差异的统计显著性。</li>
<li><strong>评估设计：</strong>设计一个针对{mfr}模型的综合评估方案，涵盖知识、推理、代码和安全四个维度。</li>
<li><strong>实践应用：</strong>如何在自己的应用场景中评估{mfr}模型的实际表现？</li>
</ol>
```

### 应用
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请分析{mfr}模型的主要应用场景和技术优势。</li>
<li><strong>方案设计：</strong>基于{mfr}的API设计一个完整的AI应用原型，包括前后端架构。</li>
<li><strong>成本分析：</strong>估算使用{mfr}的API服务处理每天100万token的成本，并与自建方案对比。</li>
<li><strong>实践应用：</strong>如何利用{mfr}的开源模型构建一个垂直领域的解决方案？</li>
</ol>
```

### 论文
```html
<h2>思考与练习</h2>
<ol>
<li><strong>论文精读：</strong>选择{mfr}的一篇核心论文，总结其主要贡献、方法论和实验结果。</li>
<li><strong>技术复现：</strong>基于论文中的方法描述，尝试复现关键实验结果，并分析可能的差异原因。</li>
<li><strong>批判性分析：</strong>论文中有哪些假设或实验设计可能存在问题？如何改进？</li>
<li><strong>延伸思考：</strong>论文中的方法可以应用到哪些其他领域或场景？需要做哪些技术调整？</li>
</ol>
```

### Default
```html
<h2>思考与练习</h2>
<ol>
<li><strong>概念理解：</strong>请用自己的话解释{topic}的核心原理，并说明它在{mfr}技术体系中的定位。</li>
<li><strong>技术分析：</strong>分析{mfr}在{topic}方面的技术特点和创新之处。</li>
<li><strong>对比思考：</strong>将{mfr}的方案与其他主流方案进行对比，分析各自的优劣势。</li>
<li><strong>实践应用：</strong>如何将{topic}的知识应用到实际的AI系统开发中？</li>
</ol>
```

## 插入位置

```python
# 优先插入到nav-links前
insert_pos = re.search(r'<div class="nav-links">', content)
if not insert_pos:
    # 没有nav-links就插到</body>前
    insert_pos = content.rfind('</body>')
```

## 效果实测

2026-06-29: 11个文件添加exercises后，每个+10分（从435→445）。这是ROI最高的单项修复。
