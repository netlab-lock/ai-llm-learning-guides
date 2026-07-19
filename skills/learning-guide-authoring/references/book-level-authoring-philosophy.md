# Book-Level Authoring Philosophy — 像写书一样制作技术指南

## 核心理念

从"技术百科"升级为"技术书籍"。百科是工具——查完就走；书是体验——从头读到尾，每一页都在推进理解。

## 一、叙事红线 (Narrative Thread)

每本指南必须有一条贯穿全书的核心叙事线。不是"第1章讲A，第2章讲B"的并列结构，而是"问题→探索→深入→贯通"的递进结构。

### 设计方法

1. **提炼核心问题**：这个领域要解决的根本问题是什么？（如：集合通信→"如何让1000张GPU高效协同训练一个模型？"）
2. **拆解子问题链**：核心问题自然分解为哪些子问题？每个子问题的答案引出下一个问题。
3. **章节顺序 = 问题链顺序**：不是按"概念分类"排序，而是按"回答问题的逻辑"排序。

### 示例：集合通信指南的叙事红线

```
核心问题：如何让GPU集群高效协同？
  → 问题1：GPU之间怎么通信？（互连硬件）
    → 问题2：多GPU间传什么数据？（集合通信原语）
      → 问题3：数据怎么路由？（拓扑与算法）
        → 问题4：怎么保证正确性？（同步与容错）
          → 问题5：怎么优化到极致？（NCCL工程实践）
            → 问题6：下一代怎么做？（前沿方向）
```

### 检验标准

读者读完第N章后，应该自然产生第N+1章要回答的问题。如果章节顺序可以任意调换而不影响理解，说明叙事红线没建立起来。

---

## 二、章节内部结构 (Chapter Anatomy)

每章不是"知识点的堆砌"，而是一个完整的学习旅程：

```
┌─────────────────────────────────────────────┐
│  🎣 开篇钩子 (Hook)                          │
│  故事/场景/问题/反直觉事实                     │
│  目的：30秒内抓住注意力，让读者知道"为什么要读"  │
├─────────────────────────────────────────────┤
│  🎯 学习目标 (Learning Objectives)            │
│  3-5个明确的"读完本章你能..."                   │
│  目的：设定预期，让读者有方向感                  │
├─────────────────────────────────────────────┤
│  📖 正文 (Body)                               │
│  按逻辑递进展开，穿插：                         │
│  - 类比（用熟悉的事物解释陌生概念）              │
│  - 图解（SVG/CSS架构图，不是纯ASCII）           │
│  - 数字（具体参数、性能数据）                   │
│  - 代码（可运行的示例）                         │
│  - 作者注（"这里容易混淆的是..."、"实战中..."）  │
├─────────────────────────────────────────────┤
│  ⚡ 关键洞察 (Key Insights)                    │
│  2-3个"本章最重要的领悟"，用高亮框展示           │
│  目的：帮读者抓住精髓，方便回顾                  │
├─────────────────────────────────────────────┤
│  ⚠️ 常见误区 (Misconceptions)                 │
│  2-3个"大多数人会犯的错"，用警告框展示           │
│  目的：预防性教育，比事后纠正更有效              │
├─────────────────────────────────────────────┤
│  🗺️ 知识定位 (Where Am I)                    │
│  一张小图：本章在全书知识地图中的位置             │
│  箭头标注：← 前置知识 | 后续需要 →              │
│  目的：消除"我学这个干嘛"的迷茫                 │
├─────────────────────────────────────────────┤
│  📝 本章小结 (Summary)                        │
│  表格形式：概念 | 一句话总结 | 关键数字          │
│  目的：快速回顾，方便复习                       │
├─────────────────────────────────────────────┤
│  🧠 深度思考题 (Reflection Questions)          │
│  3-5道题，分三个层次：                          │
│  L1 理解题：检验基本概念（"用自己的话解释..."）  │
│  L2 分析题：比较与推理（"如果X改为Y，会..."）   │
│  L3 创造题：开放性思考（"设计一个方案..."）      │
│  目的：真正的学习发生在思考中，不是阅读中         │
├─────────────────────────────────────────────┤
│  🔗 下章预告 (Next Chapter Preview)           │
│  1-2句话：下一章要解决什么问题？                 │
│  目的：制造期待，驱动继续阅读                    │
└─────────────────────────────────────────────┘
```

### 开篇钩子的五种写法

1. **故事型**："2024年，DeepSeek团队在训练V3时发现..."
2. **问题型**："如果你有1000张GPU，怎么让它们同时读取同一份梯度？"
3. **反直觉型**："增加GPU数量反而让训练变慢了——这在2023年之前是常态。"
4. **场景型**："假设你要训练一个1万亿参数的模型，单卡放不下..."
5. **历史型**："2012年之前，没有人认为GPU能用来训练神经网络。"

**禁止的开头**："本章介绍XXX技术"、"XXX是YYY的一种"——这是百科，不是书。

---

## 三、三层阅读模式 (Three-Layer Reading)

每个模块设计三个阅读深度，用CSS类区分：

### 速读层 (Speed Read) — 5分钟/章
- 只看：标题 + 关键洞察框 + 本章小结表
- 标记：用 `.speed-read-marker` 在关键段落前标注
- 适合：复习、快速查找、决定是否需要深读

### 标准层 (Standard Read) — 20分钟/章
- 看：全文正文 + 图表 + 代码
- 跳过：`.deep-dive` 折叠区域
- 适合：系统学习、首次阅读

### 深挖层 (Deep Dive) — 60分钟/章
- 看：全部内容，包括 `.deep-dive` 折叠区域
- 做：所有练习题
- 查：交叉引用的关联章节
- 适合：研究、面试准备、写论文

### CSS实现

```css
/* 深挖区域 - 默认折叠，点击展开 */
.deep-dive {
  background: #1a1024;
  border-left: 4px solid #a371f7;
  margin: 1rem 0;
  overflow: hidden;
}
.deep-dive summary {
  cursor: pointer;
  color: #a371f7;
  font-weight: 600;
  padding: 0.5rem 1rem;
}
.deep-dive summary:hover { color: #d2a8ff; }
.deep-dive[open] summary { border-bottom: 1px solid #30363d; }
```

HTML用法：
```html
<details class="deep-dive">
<summary>🔬 深入：XXX的数学推导</summary>
<div class="deep-dive-content">
  ...详细推导过程...
</div>
</details>
```

---

## 四、视觉设计升级 (Visual Design)

### 从ASCII到CSS图解

ASCII图是权宜之计，不是最终形态。优先使用纯CSS/SVG图解：

#### 架构图 (用CSS Grid/Flexbox)
```html
<div class="arch-diagram">
  <div class="arch-layer" style="--layer-color: #58a6ff">
    <span class="layer-label">应用层</span>
    <div class="arch-box">PyTorch</div>
    <div class="arch-box">JAX</div>
  </div>
  <div class="arch-arrow">↕</div>
  <div class="arch-layer" style="--layer-color: #3fb950">
    <span class="layer-label">通信层</span>
    <div class="arch-box">NCCL</div>
    <div class="arch-box">Gloo</div>
  </div>
</div>
```

CSS:
```css
.arch-diagram { display: flex; flex-direction: column; gap: 0; margin: 1.5rem 0; }
.arch-layer {
  display: flex; align-items: center; gap: 0.5rem;
  padding: 0.8rem 1rem;
  background: var(--surface);
  border-left: 3px solid var(--layer-color);
}
.arch-box {
  background: #21262d; border: 1px solid #30363d;
  padding: 0.4rem 0.8rem; border-radius: 4px;
  font-family: monospace; font-size: 0.9rem;
}
.arch-arrow {
  text-align: center; color: #8b949e;
  font-size: 1.2rem; padding: 0.2rem 0;
}
.layer-label {
  color: var(--layer-color); font-weight: 600;
  min-width: 4rem; font-size: 0.85rem;
}
```

#### 对比图 (CSS Table增强)
不是简单的`<table>`，而是带视觉编码的对比矩阵：
- 胜出项：绿色高亮
- 劣势项：红色/橙色标注
- 中性项：默认色

#### 流程图 (CSS连接线)
```css
.flow-step {
  position: relative; padding: 1rem 1.5rem;
  background: #161b22; border: 1px solid #30363d;
  margin-bottom: 0; border-radius: 6px;
}
.flow-step::after {
  content: '↓'; position: absolute;
  bottom: -1.2rem; left: 50%; transform: translateX(-50%);
  color: #58a6ff; font-size: 1.2rem;
}
.flow-step:last-child::after { content: none; }
```

### 保留ASCII图的场景
- 纯文本环境查看（终端、SSH）
- 复杂的网络拓扑（ASCII更适合表达不规则连接）
- 代码注释中的图解

**原则**：正式的架构图用CSS/SVG，临时的示意图可以用ASCII。

---

## 五、作者视角 (Author's Voice)

书和百科的最大区别：书有作者。

### 必须出现的作者声音

1. **经验之谈**（`.experience` 框）：
   > 💡 实战经验：在实际部署中，NCCL会自动选择算法，但当你看到Ring AllReduce被选用于小消息时，手动设置NCCL_ALGO=Tree通常能获得20%的延迟改善。

2. **观点判断**（`.opinion` 框）：
   > 🤔 作者观点：DeepSeek的MLA是2024年最优雅的注意力优化——它用一个工程技巧同时解决了KV Cache和长上下文两个问题。相比之下，GQA只是"少存几个头"的权宜之计。

3. **踩坑记录**（`.pitfall` 框）：
   > ⚠️ 踩坑提醒：官方文档说"支持所有集合通信操作"，但实际上AlltoAll在异构拓扑上性能极差。我们在8机64卡的环境中测过，AlltoAll的带宽利用率只有AllReduce的40%。

4. **类比解释**（正文中的自然融入）：
   > 如果把GPU集群比作一个餐厅，Ring AllReduce就是回转寿司——每道菜按固定顺序传一圈。而Tree AllReduce则是分桌传菜——先小组合并，再大组合并。

### 禁止的写法

- "XXX具有以下优点：1. 2. 3." — 这是清单，不是书
- "XXX是一种用于YYY的技术" — 这是词典定义
- 没有任何作者判断的纯罗列 — 读者需要你的洞见

---

## 六、知识地图 (Knowledge Map)

每本指南必须有一张全局知识地图，在index.html中展示。

### 设计要求

1. **节点** = 每个章节/模块
2. **边** = 前置依赖关系（必须先学A才能学B）
3. **颜色** = 难度级别（入门/中级/高级/专家）
4. **可点击** = 跳转到对应章节

### CSS实现（简化版树形图）

```html
<div class="knowledge-map">
  <div class="km-level km-l1">
    <a href="01-xxx.html" class="km-node km-beginner">基础概念</a>
  </div>
  <div class="km-connector">↙ ↘</div>
  <div class="km-level km-l2">
    <a href="02-xxx.html" class="km-node km-intermediate">核心技术A</a>
    <a href="03-xxx.html" class="km-node km-intermediate">核心技术B</a>
  </div>
  <div class="km-connector">↘ ↙</div>
  <div class="km-level km-l3">
    <a href="04-xxx.html" class="km-node km-advanced">综合应用</a>
  </div>
</div>
```

```css
.knowledge-map { text-align: center; margin: 2rem 0; }
.km-level { display: flex; justify-content: center; gap: 2rem; margin: 0.5rem 0; }
.km-node {
  display: inline-block; padding: 0.6rem 1.2rem;
  border-radius: 8px; text-decoration: none;
  font-weight: 600; transition: transform 0.2s;
}
.km-node:hover { transform: scale(1.05); }
.km-beginner { background: #0d2818; color: #3fb950; border: 1px solid #238636; }
.km-intermediate { background: #0d1d30; color: #58a6ff; border: 1px solid #1f6feb; }
.km-advanced { background: #2d1b00; color: #d29922; border: 1px solid #9e6a03; }
.km-expert { background: #2d1020; color: #f778ba; border: 1px solid #db61a2; }
.km-connector { color: #484f58; font-size: 1.2rem; letter-spacing: 1rem; }
```

---

## 七、练习题设计 (Exercise Design)

从"装饰性练习"升级为"设计过的学习活动"。

### 三个层次

| 层次 | 目标 | 示例 | 标记 |
|------|------|------|------|
| L1 理解 | 检验基本概念 | "用自己的话解释Ring AllReduce的工作原理" | `level-1` |
| L2 分析 | 比较与推理 | "如果将AllReduce从Ring改为Tree，在什么情况下性能会变差？为什么？" | `level-2` |
| L3 创造 | 开放性思考 | "设计一个适用于异构GPU集群的集合通信方案" | `level-3` |

### 好练习题的特征

1. **有具体场景**：不是"解释X"，而是"在Y场景下，X会怎样？"
2. **有思考空间**：不是背诵式的，而是需要推理的
3. **有实用价值**：答案对工作/面试有帮助
4. **有提示**：给一个思考方向，不是完全开放

### 练习题框样式

```html
<div class="exercise">
  <div class="exercise-header">
    <span class="exercise-level level-2">L2 分析</span>
    <span class="exercise-topic">集合通信</span>
  </div>
  <p class="exercise-question">
    在一个4节点、每节点8卡的集群中，AllReduce分别使用Ring和Tree算法。
    当消息大小从1KB增加到1GB时，两种算法的性能曲线会如何变化？
    画出你预期的延迟-消息大小曲线。
  </p>
  <details class="exercise-hint">
    <summary>💡 提示</summary>
    <p>考虑两个因素：(1) 延迟主导 vs 带宽主导的切换点，(2) Ring的链路跳数 vs Tree的树深度</p>
  </details>
</div>
```

---

## 八、写作语气 (Writing Tone)

### 原则：像一个经验丰富的同事在跟你解释

✅ 好的语气：
> "你可能会问，为什么不直接用AllReduce？答案是：AllReduce假设所有GPU都要同步，但MoE训练中，不同专家处理不同token，同步模式完全不同。"

❌ 不好的语气：
> "AllReduce是一种集合通信操作，用于在所有参与者之间聚合数据。在MoE训练中，由于专家分布的特点，AllReduce不能满足需求。"

### 具体规则

1. 用"你"而不是"读者"——直接对话
2. 用"我们"表示共同探索——"我们来看看这个公式"
3. 允许口语化表达——"说白了就是..."、"说人话的话..."
4. 主动使用反问——"这不是很合理吗？但等等..."
5. 承认不确定性——"这里我的理解是..."、"论文没有明确说，但..."
6. 适度使用比喻——每个核心概念至少一个类比
