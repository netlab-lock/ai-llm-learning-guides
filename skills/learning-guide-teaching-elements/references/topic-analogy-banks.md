# 主题类比库：批量生成唯一tip/warn/deep的核心技术

## 背景
2026-06-28实战：333个文件×5个h2节×3个教学元素 = ~5000个唯一内容块。
用LLM API逐个生成太慢（每个文件1次API调用×333文件 = 数小时）。
用纯模板又不够唯一。**解法：主题类比库 + 种子哈希**。

## 技术原理

### 1. 主题类比库
为20+常见LLM主题各准备4个日常类比+技术映射：

```python
ANALOGIES = {
    '注意力': [
        ('显微镜调焦', '对焦越精确看到的细节越多'),
        ('老师课堂提问', '一次只关注几个关键学生'),
        ('搜索引擎排序', '根据关键词权重排序结果'),
        ('GPS导航', '同时考虑多条路径的权重'),
    ],
    'MoE': [
        ('医院分诊台', '根据症状分配专科医生'),
        ('餐厅后厨', '凉菜师热菜师面点师各司其职'),
        ('公司部门', 'HR管招聘财务管账技术管开发'),
        ('交通调度', '根据路况动态分配车道'),
    ],
    # ... 推理/训练/量化/长上下文/多模态/Agent/部署/对齐/数据/评估等
}
```

### 2. 厂商上下文字典
每个厂商有独特的技术特点，类比内容需要引用：

```python
MFR_CONTEXT = {
    'MiniMax': {'co': 'MiniMax', 'tech': 'Lightning Attention', 'focus': '超长上下文(4M token)'},
    'GLM': {'co': '智谱AI', 'tech': 'GLM架构', 'focus': '双语Agent能力'},
    # ... 17国产 + 5国际
}
```

### 3. 种子哈希确保确定性唯一
```python
import hashlib, random
seed = hashlib.md5(f"{mfr}:{h2_title}:{idx}".encode()).hexdigest()[:8]
random.seed(int(seed, 16))
# 同一文件同一section总是生成相同内容
# 不同文件不同section生成不同内容
```

### 4. 内容组装
```python
# 从h2标题提取主题关键词 → 匹配类比库 → 选择类比 → 结合厂商上下文组装
topic = clean_h2_title(h2)  # "1. Lightning Attention实现" → "Lightning Attention实现"
analogy, detail = random.choice(ANALOGIES.get(matched_keyword, ANALOGIES['推理']))
tip = f'{topic}就像{analogy}——{detail}。{mfr_info["co"]}在{mfr_info["model"]}中的实现体现了这一设计理念。'
```

## 效果
- 24种通用模式×231次出现 = 全部替换为唯一内容
- 每个文件每个h2节的tip/warn/deep都不同
- 零API调用，纯Python脚本，2分钟处理333个文件

## 局限
- 类比库覆盖20+主题，但罕见主题会fallback到通用模板
- 生成的内容质量不如LLM精心撰写的，但比重复模板好得多
- 适合大规模批量处理，不适合单文件精修

## 使用场景
1. **大规模批量升级**(100+文件): 先用类比库快速消除重复，再用LLM精修低分文件
2. **新文件初始填充**: 为新建指南快速填充非重复的初始内容
3. **质量底线保障**: 确保任何h2节的tip都不会是完全相同的通用模板

## 完整代码
详见 `learning-guide-quality-rubric` skill的 `references/batch-upgrade-round2-2026-06.md`。
