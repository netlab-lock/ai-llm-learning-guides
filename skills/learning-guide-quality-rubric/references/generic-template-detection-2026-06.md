# 通用模板检测清单 (2026-06)

批量脚本/子agent最常生成的通用模板内容。在最终质量审计时必须检测并清理。

## 通用段落模式 (Body Templates)

```python
GENERIC_BODY_PATTERNS = [
    '由三个关键组件构成',
    '采用了分层抽象的设计哲学',
    '复合函数 f(g(x))',
    '深入原理与数学推导',
    '工程实践与常见问题',
    '从底层实现来看，整个系统的工作机制可以分解为三个核心阶段',
    '从系统设计的底层逻辑来看，为什么分层架构是主流选择',
    '从优化理论的底层原理出发',
    '关注点分离的原则',
    '每个组件只负责一个明确的功能，通过清晰的接口协作',
    '掌握这个主题的高效路径：先理解原理',
    '在实际应用中，建议先从最小规模',
    '从数学角度分析，本节涉及的核心算法具有明确的公式表示和推导过程',
    '从数学角度看，训练目标函数通常为交叉熵损失加上正则化项',
    '训练优化的关键技术包括：混合精度训练(FP16/BF16)减少显存占用约50%',
    '性能评估需要关注两个核心指标：Time To First Token',
    '优化策略可以从四个维度入手：(1)算法优化',
    '常用的评估基准包括：MMLU(知识广度，14K题目覆盖57个学科)',
    '需要注意的评估陷阱包括：数据污染(训练集包含测试题)',
    '工程实践中最常用的优化手段包括：算子融合(Operator Fusion)',
    '优化效果的量化评估需要关注两个核心指标：Time To First Token',
]
```

## 重复教学元素模式 (Duplicate Teaching Elements)

```python
# 学习路径建议 (最常见重复tip)
DUPLICATE_TIP_PATTERNS = [
    '学习路径建议：\n然后按照章节顺序逐步深入',
    '学习路径建议：\n建议先掌握本节的基础概念',
    '向前串联：\n本节内容为后续更高级的主题奠定了基础',
    '向前串联：\n本章内容为理解MiniMax后续更高级的技术主题',
    '实践建议：\n在将本节技术应用于实际项目时，建议遵循',
    '学习路径建议：\n建议先理解Transformer注意力机制',
]

# 深入探讨 (最常见重复deep)
DUPLICATE_DEEP_PATTERNS = [
    '思考与练习：\n\n总结本节的核心原理和关键技术点',
    '深入探讨：从理论深度看，标准自注意力的O(n²)复杂度',
    '深入探讨：从统计学角度看，模型评测的核心问题',
    '深入探讨：从博弈论角度看，RLHF本质上是一个',
    '深入探讨：从控制论角度看，Agent系统的核心挑战',
    '深入探讨：Softmax注意力的计算复杂度为O(n²d)',
    '深入探讨：从数学角度分析，本节涉及的核心算法',
]
```

## 检测脚本

```python
import re
from pathlib import Path
from collections import Counter

def audit_generic_content(directories):
    """审计通用模板内容"""
    generic_found = []
    tip_texts = Counter()
    deep_texts = Counter()
    
    for dir_path in directories:
        for f in dir_path.rglob("*.html"):
            if "index" in f.name.lower():
                continue
            html = f.read_text(encoding='utf-8', errors='ignore')
            
            # Check generic body patterns
            for marker in GENERIC_BODY_PATTERNS:
                if marker in html:
                    generic_found.append((str(f), marker[:40]))
            
            # Collect tip/deep texts for duplicate check
            for t in re.findall(r'class="tip"[^>]*>(.*?)</div>', html, re.S):
                text = re.sub(r'<[^>]+>', '', t).strip()[:80]
                tip_texts[text] += 1
            for d in re.findall(r'class="deep"[^>]*>(.*?)</div>', html, re.S):
                text = re.sub(r'<[^>]+>', '', d).strip()[:80]
                deep_texts[text] += 1
    
    # Report
    print(f"Generic markers found: {len(generic_found)}")
    print(f"Duplicate tip patterns (>5 copies): {sum(1 for c in tip_texts.values() if c > 5)}")
    print(f"Duplicate deep patterns (>5 copies): {sum(1 for c in deep_texts.values() if c > 5)}")
    
    return generic_found, tip_texts, deep_texts
```

## 清理策略

1. **先清Body Templates** → 大幅降低字数，暴露真实内容
2. **再清Duplicate Tips** → 移除重复的教学元素
3. **最后清Duplicate Deeps** → 移除重复的深入分析
4. **重新评分** → 接受真实分数
5. **用子agent补充主题相关内容** → 提升分数和质量

**核心原则**: 诚实的A+级(内容真实)优于虚假的S级(靠模板垃圾撑字数)。
