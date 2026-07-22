# AI-LLM 学习指南 & 制作方法论

> 956+ 篇 HTML 学习指南，覆盖 LLM 技术全栈。附带完整的制作方法论（Hermes Agent Skills），可复用。

---

## 📖 在线浏览

**[点击这里打开学习指南](https://netlab-lock.github.io/ai-llm-learning-guides/)**

## 📁 内容结构

```
guides/
├── 01-基础理论/          106篇  深度学习经典模型 → Transformer → BERT → GPT → LLaMA
├── 02-模型架构/           27篇  MoE → 注意力机制前沿 → 长上下文 → Tokenizer
├── 03-训练技术/           49篇  数据工程 → 分布式训练 → 蒸馏 → 模型融合
├── 04-对齐与安全/         36篇  RLHF → DPO → GRPO → Red Teaming → Constitutional AI
├── 05-推理优化/          134篇  vLLM → TensorRT-LLM → SGLang → llama.cpp → 量化
├── 06-硬件生态/           31篇  GPU架构 → 非NVIDIA加速器 → 集合通信
├── 07-应用技术/           62篇  RAG → Agent → 代码生成 → 多模态 → Structured Output
├── 08-评测体系/           11篇  MMLU → GSM8K → HumanEval → Arena → 安全评测
├── 09-厂商与前沿/        335篇  DeepSeek → Qwen → GLM → Kimi → MiniMax → 联邦学习
├── 10-工具与项目/          1篇
├── 11-推理模型/           12篇
├── 12-AI基础设施/         10篇
├── 13-推理时计算/         10篇  Test-Time Compute → Extended Thinking → 推理经济学
├── 14-AI-Agent系统/       20篇  Agent基础 → 架构设计 → RAG → 微调 → 面试实战
├── NVIDIA集合通信/         9篇
├── 昇腾超节点集合通信/       7篇
└── 经典优化方法/           12篇  LP/IP → 启发式 → 近似算法
```

**总计 956 篇 HTML，覆盖 10 大知识支柱、25 个专题方向。**

详见 [知识库全景图](知识库全景图.md)。

---

## 🔧 制作方法论（Hermes Agent Skills）

本仓库附带完整的制作方法论，以 [Hermes Agent](https://hermes-agent.nousresearch.com) Skill 格式存储在 `skills/` 目录。

### 四个 Skill 及其职责

| Skill | 职责 | 类比 |
|-------|------|------|
| [learning-guide-authoring](skills/learning-guide-authoring/) | 怎么创建指南 | 建筑图纸 |
| [learning-guide-quality-rubric](skills/learning-guide-quality-rubric/) | 怎么评价质量 | 质检标准 |
| [learning-guide-teaching-elements](skills/learning-guide-teaching-elements/) | 怎么写好教学元素 | 施工工艺 |
| [html-learning-guide-quality-upgrade](skills/html-learning-guide-quality-upgrade/) | 怎么批量改进 | 翻新流程 |

### 核心方法论

**1. 八维度内容框架**（每个文件必须覆盖）

| 维度 | 说明 | 例子 |
|------|------|------|
| 背景 | 问题/历史背景 | "为什么需要 MoE？" |
| 名字由来 | 术语来源 | "Mixture of Experts 首次出现在 1991 年 Jacobs et al." |
| 原理 | 数学/算法原理 | 含公式推导、代码实现 |
| 技术细节 | 实现层面设计 | 伪代码、配置示例 |
| 使用场景 | 什么时候用 | "超大模型、推理成本敏感场景" |
| 相似技术对比 | 横向对比表 | 性能/精度/复杂度/适用场景 |
| 关联技术 | 上下游关系 | 知识网络图 |
| 实际效果 | benchmark 数据 | 真实案例、部署经验 |

**2. 三层解释法**（每个核心概念）

```
第一层：生活类比    → "KV Cache 就像做数学题时的草稿纸"
第二层：技术原理    → "2 × n_layers × n_heads × d_head × seq_len × batch_size × bytes"
第三层：数学推导    → FlashAttention 的 IO 复杂度 O(N²d²/M) 推导
```

**3. 五维度质量标准**（每篇文件 500 分制）

| 维度 | 满分 | 关键指标 |
|------|------|---------|
| 内容密度 | 100 | ≥8000字, ≥5个h2, ≥3个表格, ≥3个代码块 |
| 教学设计 | 100 | tip/warn/deep 各节独立不重复, 有练习题和交叉引用 |
| 结构完整性 | 100 | 有index, 有导航, 无空壳文件, CSS统一 |
| 知识准确性 | 100 | 数据有出处, 无过时信息 |
| 可读性/UX | 100 | 暗色主题, 移动端适配, 无死链 |

等级: S(≥450) > A(≥380) > B(≥300) > C(≥200) > D(≥100) > F

### 如何使用这些 Skill

**方式 A：直接阅读 Markdown**（任何人都能用）

打开 `skills/` 下的 `SKILL.md` 文件，就是完整的制作规范。每个 skill 目录下还有 `references/` 子目录，包含 14 轮迭代的实战经验和踩坑记录。

**方式 B：在 Hermes Agent 中加载**（需要安装 [Hermes Agent](https://hermes-agent.nousresearch.com)）

```bash
# 将 skills 复制到 Hermes skills 目录
cp -r skills/* ~/.hermes/skills/productivity/

# 然后在对话中即可使用
# Hermes 会自动加载相关 skill
```

```
# 或在对话中手动查看
skill_view(name='learning-guide-authoring')
skill_view(name='learning-guide-quality-rubric')
skill_view(name='learning-guide-teaching-elements')
skill_view(name='html-learning-guide-quality-upgrade')
```

---

## 📊 质量标准速查

### ✅ 好的教学元素

```html
<!-- tip: 具体的生活类比，有映射关系 -->
<div class="tip"><strong>通俗类比：</strong>
KV Cache就像你做数学题时的草稿纸。每算一步把中间结果写在纸上，
后面步骤直接查就行。映射关系：草稿纸=显存中的KV Cache，
中间结果=K/V向量，翻找=注意力计算，纸张大小=显存容量。
</div>

<!-- warn: 该主题特有的误区 -->
<div class="warn"><strong>常见误区：</strong>
很多人以为KV Cache只是"缓存"，删了也无所谓。实际上没有KV Cache，
每生成一个token都要重新计算所有之前token的K和V，时间复杂度从O(1)
退化到O(n²)，推理速度下降100倍以上。
</div>

<!-- deep: 有具体数字和公式 -->
<div class="deep"><strong>深入探讨：</strong>
KV Cache的显存公式为：2 × n_layers × n_heads × d_head × seq_len ×
batch_size × bytes_per_element。以LLaMA-70B为例(80层、64头、128维、FP16)，
单条4K序列的KV Cache约10.7GB。batch_size=32时需要342GB显存——
这就是为什么KV Cache量化和PagedAttention如此重要。
</div>
```

### ❌ 坏的教学元素（通用模板，必须避免）

```html
<!-- 任何主题都能用 = 没有价值 -->
❌ 本节概念是理解现代LLM系统的重要一环...
❌ LLM推理就像去餐厅吃饭...              ← 每个节都用同一个
❌ 不要认为这只是理论知识...
❌ 从更深层次来看，这个技术代表了AI领域的重要趋势。
```

### 核心原则

> **诚实的 A+ 优于虚假的 S。**
> 模板垃圾撑出来的高分没有意义，真实的内容质量才是价值。

---

## 🛠️ 项目结构

```
ai-llm-learning-guides/
├── README.md                          ← 你正在读的文件
├── 知识库全景图.md                       ← 知识库整体架构
├── .gitignore
├── skills/                            ← 制作方法论（Hermes Agent Skills）
│   ├── learning-guide-authoring/      ← 创建规范
│   ├── learning-guide-quality-rubric/ ← 评分体系
│   ├── learning-guide-teaching-elements/ ← 教学元素写法
│   └── html-learning-guide-quality-upgrade/ ← 批量升级流水线
├── templates/                         ← CSS 模板
│   └── guide-style-b.css
└── guides/                            ← 学习指南本体
    ├── 01-基础理论/
    ├── 02-模型架构/
    ├── ...
    └── 经典优化方法/
```

---

## License

学习指南内容仅供个人学习使用。制作方法论（skills/）可自由使用和修改。
