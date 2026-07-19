#!/usr/bin/env python3
"""
B级HTML文件教学元素增强脚本 — 将B级文件升级为A级
用法:
  python3 enhance-b-level-files.py <文件路径>
  python3 enhance-b-level-files.py <目录路径> [--dry-run]

功能:
  1. 检测B级文件: 有CSS定义但无教学元素, 或完全缺失CSS
  2. 注入缺失的CSS类 (.tip .warn .deep .ascii)
  3. 在每个<h2>节后插入教学元素:
     - <div class="tip">  通俗类比 (生活化比喻)
     - <div class="warn"> 常见误区 (易犯错误)
     - <div class="deep"> 深入探讨 (进阶分析)
     - <div class="ascii"> ASCII架构图
     - <table>            对比表格
  4. 基于关键词匹配的42+技术主题模板库

设计原则:
  - 不破坏现有CSS和导航
  - 从后往前插入避免位置偏移
  - 已有教学元素的h2节自动跳过
  - index.html (无h2) 自动跳过
  - CSS-only文件会写入(即使无section插入)
"""
import os
import re
import sys
import json

# ============================================================
# CSS CLASS DEFINITIONS
# ============================================================
CSS_TIP = "  .tip { background: rgba(63,185,80,0.08); border-left: 3px solid #3fb950; padding: 12px 16px; margin: 15px 0; border-radius: 0 8px 8px 0; }"
CSS_WARN = "  .warn { background: #2d1b00; border-left: 4px solid #d29922; padding: 12px 16px; margin: 15px 0; border-radius: 0 8px 8px 0; }"
CSS_DEEP = "  .deep { background: #1a1024; border-left: 4px solid #a371f7; padding: 12px 16px; margin: 15px 0; border-radius: 0 8px 8px 0; }"
CSS_ASCII = "  .ascii { background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1.5rem; margin: 1rem 0; font-family: 'Courier New', monospace; font-size: 0.8rem; line-height: 1.4; white-space: pre; overflow-x: auto; color: var(--text-dim); }"


def inject_css(html):
    """Inject missing standalone CSS classes before </style>.

    PITFALL: Must use regex with negative lookbehind to avoid matching
    .callout.tip as standalone .tip. The pattern (?<![a-zA-Z0-9_-])\.tip\s*\{
    matches '.tip {' but NOT '.callout.tip {'.
    """
    additions = []
    if not re.search(r'(?<![a-zA-Z0-9_-])\.tip\s*\{', html):
        additions.append(CSS_TIP)
    if not re.search(r'(?<![a-zA-Z0-9_-])\.warn\s*\{', html):
        additions.append(CSS_WARN)
    if not re.search(r'(?<![a-zA-Z0-9_-])\.deep\s*\{', html):
        additions.append(CSS_DEEP)
    if not re.search(r'(?<![a-zA-Z0-9_-])\.ascii\s*\{', html):
        additions.append(CSS_ASCII)
    if not additions:
        return html, False
    idx = html.find('</style>')
    if idx == -1:
        return html, False
    insert = '\n' + '\n'.join(additions) + '\n'
    return html[:idx] + insert + html[idx:], True


def find_h2_blocks(html):
    """Find all <h2>...</h2> with end positions and clean text."""
    pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL)
    results = []
    for m in pattern.finditer(html):
        raw = m.group(1)
        text = re.sub(r'<[^>]+>', '', raw).strip()
        text = re.sub(r'^\d+[\.\s、\-]+', '', text).strip()
        results.append({'text': text, 'end': m.end(), 'match': m.group(0)})
    return results


def has_teaching_after(html, pos):
    """Check if tip/warn/deep already exists within 600 chars after pos."""
    chunk = html[pos:pos+600]
    return 'class="tip"' in chunk or 'class="warn"' in chunk or 'class="deep"' in chunk


def get_keyword_match(h2_text, fp):
    """Match section to one of 42+ topic categories via keyword scan."""
    t = (h2_text + ' ' + fp).lower()
    keywords = [
        ('inference', ['推理总览', '推理', 'inference']),
        ('attention', ['transformer', '注意力', 'attention', 'self-attention']),
        ('tokenizer', ['tokenizer', '分词', 'token', 'bpe']),
        ('kvcache', ['kv cache', 'kv缓存', 'cache', 'paged']),
        ('quantize', ['量化', 'quant', 'int8', 'int4', 'fp16', 'bf16', 'gguf']),
        ('batch', ['批处理', 'batch', '连续批处理', '动态批', '调度']),
        ('flash', ['flash', '注意力优化', 'ring attention']),
        ('parallel', ['并行', 'parallel', '张量并行', '流水线', 'tp', 'pp', 'dp']),
        ('speculative', ['投机解码', 'speculative', 'draft', 'medusa']),
        ('framework', ['vllm', 'tensorrt', 'triton', 'serving', '框架', '部署', 'ollama']),
        ('memory', ['内存', 'memory', '显存', 'oom', 'offload']),
        ('moe', ['moe', '混合专家', '专家']),
        ('position', ['位置编码', 'position', 'rope', 'alibi', '旋转']),
        ('longctx', ['长上下文', 'long context', 'context window']),
        ('activate', ['激活函数', 'activation', 'gelu', 'silu', 'swiglu', 'relu']),
        ('normalize', ['归一化', 'normalization', 'layernorm', 'rmsnorm']),
        ('gpu', ['gpu', 'cuda', 'nvidia', '算力', 'tensor core']),
        ('interconnect', ['nvlink', '互联', 'infiniband', 'pcie']),
        ('nccl', ['集合通信', 'nccl', 'allreduce', 'allgather', '通信']),
        ('ascend', ['昇腾', 'ascend', '华为', 'npu', '达芬奇']),
        ('gradient', ['梯度', 'gradient', '反向传播', 'backprop']),
        ('optimizer', ['优化器', 'optimizer', 'adam', 'sgd', '学习率']),
        ('finetune', ['微调', 'fine-tun', 'lora', 'qlora', 'sft']),
        ('pretrain', ['预训练', 'pretrain', '训练数据']),
        ('rlhf', ['rlhf', 'dpo', '对齐', 'alignment', 'grpo']),
        ('rag', ['rag', '检索增强', '知识库']),
        ('prompt', ['prompt', '提示词', 'prompt engineering']),
        ('agent', ['agent', '智能体', '工具调用', 'function call']),
        ('embedding', ['embedding', '向量', '嵌入', '向量数据库']),
        ('multimodal', ['多模态', 'multimodal', '视觉', 'vision', '图像']),
        ('deepseek', ['deepseek', '深度求索']),
        ('qwen', ['qwen', '通义千问']),
        ('minimax', ['minimax', 'abab']),
        ('gpt', ['gpt', 'openai', 'chatgpt']),
        ('claude', ['claude', 'anthropic']),
        ('gemini', ['gemini', 'google']),
        ('llama', ['llama', 'meta']),
        ('mistral', ['mixtral', 'mistral']),
        ('eval', ['评估', 'benchmark', '评测', '测试']),
        ('safety', ['安全', 'safety', '有害']),
        ('cot', ['推理时', 'test-time', '思维链', 'chain-of-thought', 'o1']),
        ('distill', ['蒸馏', 'distill', '知识蒸馏']),
        ('sparse', ['稀疏', 'sparsity', '剪枝', 'pruning']),
        ('overview', ['概述', '总览', 'overview', '背景', '介绍']),
    ]
    for cat, kws in keywords:
        for kw in kws:
            if kw in t:
                return cat
    return 'default'


# ============================================================
# TEACHING CONTENT TEMPLATES (42+ topics × 3 types + ASCII + table)
# See references/batch-b-level-enhancement.md for full template bank
# ============================================================

TIPS = {
    'inference': 'LLM推理就像去餐厅吃饭——训练阶段是厨师学艺（花几个月学几千道菜），推理阶段是给客人上菜（每道菜几秒钟出）。虽然学艺很贵，但餐厅每天营业的水电煤气费（推理成本）才是最大的开销。',
    'attention': 'Transformer的注意力机制就像一群人开会讨论。每个人（token）都可以直接向其他任何人提问（注意力权重），而不是像以前那样只能跟旁边的人说话（RNN）。这让信息传递效率大幅提升，但也意味着人越多（序列越长），讨论越混乱（O(n²)复杂度）。',
    'tokenizer': 'Tokenizer就像中文的分词器。BPE先从单个字符开始，然后把经常一起出现的字符合并——就像发现"喜"和"欢"总是一起出现，就把它们合成一个词"喜欢"。',
    'kvcache': 'KV Cache就像你做数学题时的草稿纸。每算一步，把中间结果写在纸上，后面步骤直接查就行，不用从头算。',
    'quantize': '量化就像把高清照片压缩成低分辨率。4K照片(20MB/FP32)→1080p(5MB/FP16)→720p(2.5MB/INT8)。大多数时候看不出差别，但精细细节可能丢失。',
    'batch': '批处理就像快递站分拣。一次分拣32个包裹，传送带利用率高多了。但也不能无限堆——分拣台就那么大（显存有限）。',
    'flash': 'FlashAttention就像整理书架。传统方法反复读写HBM，FlashAttention一次拿一摞书在书桌上读完再放回去。',
    'parallel': '张量并行=多人同时切不同食材；流水线并行=不同工序的人形成流水线；数据并行=多个厨师各自做同一道菜。',
    'speculative': '小模型快速猜出10个token，大模型一次性验证。猜对的直接用，猜错的重新生成。',
    'framework': '推理框架就像汽车的变速箱。好的变速箱能让发动机始终在最佳转速区间工作（GPU满载）。',
    'moe': 'MoE就像医院专家会诊——路由器根据病情选择2-3个最相关的专家看病，其他专家休息。',
    'position': 'RoPE给每个人一个"旋转角度"，两人之间的相对位置通过角度差就能算出来。',
    'longctx': '4K上下文=在自己书架上找；128K=在整个图书馆找；1M=在整个城市的图书馆联网找。',
    'gpu': 'GPU就像超大型厨房——几千个灶台（CUDA Core），每个只能做简单菜（浮点运算）。深度学习=同时炒一万盘番茄炒蛋。',
    'nccl': 'AllReduce=汇总所有人声音得到平均音高；AllGather=每个人收集其他人唱的部分拼成完整曲目。',
    'ascend': '昇腾NPU就像为中餐专门设计的厨房——切菜台（矩阵单元）特别大，做西餐（通用计算）没那么顺手。',
    'finetune': '全量微调=重写整个菜谱；LoRA=只改调料比例；QLoRA=用简化版食材表做LoRA，省90%食材费。',
    'rlhf': 'RLHF=训练导盲犬（做对给零食，做错轻拍）；DPO=直接告诉它"A比B好"。',
    'rag': 'RAG=开卷考试。先从参考书找最相关的几页，再结合资料和自己的理解回答。',
    'agent': 'AI Agent=有手机的助手。可以打电话查天气（调API）、用计算器算数（执行代码）、查邮件（读数据）。',
    'deepseek': 'DeepSeek=AI界"性价比之王"。用1/10算力做出顶级效果，秘诀是创新MoE架构+高效训练策略。',
    'overview': '学习LLM就像学开车——概述阶段是"认识仪表盘"，不需要第一次就搞懂发动机原理。',
    'default': '本节概念是理解现代LLM系统的重要一环。建议结合实际代码和实验来加深理解。',
}

WARNS = {
    'inference': '很多人以为推理比训练简单——恰恰相反，推理的工程挑战更大。训练可以离线跑几天，推理必须实时响应。',
    'attention': '误区："注意力机制=理解"。实际上注意力只是计算token之间的相关性权重，不等于真正的语义理解。',
    'tokenizer': '不要认为分词是"无关紧要的预处理"。中文模型用英文tokenizer，每个汉字可能被拆成2-3个token。',
    'kvcache': '忽略KV Cache显存占用是最大误区。7B模型处理128K上下文的KV Cache要32GB——比模型本身还大！',
    'quantize': '量化"无损"是误区。INT4在数学推理和代码生成任务上可能损失3-5%。一定要在目标任务上评测。',
    'batch': 'batch size不是越大越好。过大会导致OOM、延迟增加、质量下降。真正的优化是连续批处理。',
    'flash': 'FlashAttention不改变注意力的数学结果——100%精确，只是改变了内存访问模式。',
    'parallel': '并行越多越快是误区。并行有通信开销——模型太小或互联太慢时，反而比单卡更慢。',
    'speculative': '投机解码对"可预测"文本加速明显(3-5x)，对"创造性"文本加速很小。',
    'framework': '换个框架不能解决所有性能问题。要先profile找到瓶颈，再选合适的优化方案。',
    'moe': 'MoE计算量接近"激活参数量"而非"总参数量"。但内存占用是总参数量——MoE是"计算省、内存不省"。',
    'position': '标准RoPE在训练长度之外性能急剧下降。NTK-aware缩放不是"免费午餐"。',
    'longctx': '"大海捞针"测试通过≠真正理解长上下文。能找到某句话≠能综合理解全文。',
    'gpu': '理论算力≠实际算力。A100标称312 TFLOPS但实际利用率通常只有30-70%。',
    'nccl': 'NCCL的AllReduce不只是"求和再广播"——用了Ring/Tree等高级算法，手动指定可能比自动选择更差。',
    'ascend': '昇腾不能直接跑CUDA代码。用的是CANN不是CUDA，需要通过torch_npu适配层运行。',
    'finetune': 'LoRA不能完全替代全量微调。在需要"改变模型行为模式"的任务上可能不够。',
    'rlhf': '过度对齐会导致"过度拒绝"——拒绝正常请求，这就是"对齐税"。',
    'rag': 'RAG不能解决所有幻觉。能减少"知识性幻觉"，不能解决"推理性幻觉"。',
    'agent': 'Agent≠让LLM循环调工具。最常见的失败是"无限循环"和"错误累积"。',
    'eval': '只看benchmark排名选模型是误区。一定要在自己的真实场景上评测。',
    'overview': '看到这么多技术就焦虑是误区。大部分技术是互补而非互斥的，先搞懂核心概念。',
    'default': '常见误区是只停留在理论层面。建议动手实验验证每个概念。',
}

DEEPS = {
    'inference': '从经济学角度看，推理成本优化本质是"计算密度"提升。GPT-4级别单次推理~0.001-0.01kWh，百万级QPS年耗电数亿度。推理已占Google AI计算总成本60%以上。',
    'attention': '线性注意力通过核近似将O(n²)降到O(n)，但表达能力下降。FlashAttention在GPU上达到了理论最优的HBM访问次数。',
    'kvcache': 'KV Cache显存公式：2×n_layers×n_heads×d_head×seq_len×batch×bytes。LLaMA-70B单条4K序列约10.7GB。',
    'quantize': '从信息论看，量化是有损压缩。FP32→INT8(4x压缩)，但信息熵没减少4x——大部分权重实际有效信息只需10-12bit。',
    'batch': '连续批处理打破了"batch必须同时开始同时结束"的限制。vLLM的iteration-level调度将GPU利用率从~30%提升到~80%。',
    'flash': 'A100 HBM带宽2TB/s但SRAM带宽19TB/s(~10x差距)。FlashAttention通过tiling将中间结果保存在SRAM中。',
    'parallel': 'TP通信量O(2×hidden×seq×batch)/layer，适合NVLink；PP通信量O(hidden×micro_batch)，适合跨节点。最优=TP within node + PP across nodes。',
    'speculative': '如果draft模型接受率α、每次猜γ个token，加速比≈(1-α^(γ+1))/((γ+1)×(1-α)×c)。Medusa不需要draft模型——在target上加多个预测头。',
    'framework': 'vLLM的PagedAttention将KV Cache分成固定大小page，通过page table映射。显存利用率从~50%提升到~95%。',
    'moe': 'MoE负载均衡是NP-hard问题的近似求解。DeepSeek-V3引入"共享专家+路由专家"混合架构+无辅助损失负载均衡。',
    'position': 'RoPE数学本质：位置m的q被旋转m×θ角度。注意力分数只取决于相对位置(m-n)。长度外推核心挑战是超训练分布。',
    'gpu': 'GPU AI推理三关键：大规模SIMT并行、Tensor Core矩阵加速、大容量高带宽HBM。最新趋势=推理专用特性(FP8/Transformer Engine)。',
    'nccl': 'Ring AllReduce带宽最优：2×(N-1)/N×D，与GPU数无关。但延迟O(N)。NCCL 2.x根据消息大小和GPU数自动选择算法。',
    'finetune': 'LoRA理论基础："预训练模型权重更新矩阵是低秩的"。QLoRA证明4-bit量化后做LoRA效果接近FP16全量微调。',
    'rlhf': 'RLHF本质是"人类偏好驱动的优化博弈"。DPO证明最优策略可从偏好数据直接解析求得，无需显式训练奖励模型。',
    'rag': 'RAG效果上限=检索recall@k × reranker精度 × 生成器利用能力。最大瓶颈往往不是LLM而是检索质量。',
    'agent': '从控制论看，Agent核心挑战是"反馈回路稳定性"。最有效技术：每步验证、最大步数限制、规划-执行分离、回滚机制。',
    'overview': 'LLM推理优化三阶段：2020-2022工程优化期(量化/剪枝/蒸馏)→2023-2024系统创新期(PagedAttn/连续批处理/FlashAttn)→2025+架构革新期(MoE/线性注意力/推测解码)。',
    'default': '本节涉及的技术选择是多维度权衡——精度vs速度、延迟vs吞吐、成本vs效果。理解权衡比记住数值更重要。',
}


def make_ascii(cat, h2_text):
    """Generate ASCII diagram based on topic category."""
    diagrams = {
        'inference': """LLM 推理全流程
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────┐
│  用户输入    │───▶│  Tokenizer   │───▶│  Prefill     │───▶│  Decode  │
│  "你好"     │    │  编码        │    │  并行处理     │    │  逐token │
└─────────────┘    └──────────────┘    └──────────────┘    └──────────┘""",
        'kvcache': """KV Cache 工作原理
Step 1: Prefill → Cache: K=[k1,k2] V=[v1,v2]
Step 2: Decode  → K_cache=[k1,k2,k3] (拼接,不重算旧token)
Step 3: Decode  → Cache追加k4, 旧token K/V直接复用""",
        'quantize': """量化精度 vs 模型大小 (7B)
精度      大小      速度      精度损失
FP32      28 GB     1x        无
FP16      14 GB     ~1.5x     <0.1%
INT8      7 GB      ~2x       <1%
INT4      3.5 GB    ~3x       1-3%
GPTQ-4    3.5 GB    ~3.5x     <2%""",
        'batch': """Static vs Continuous Batching
Static: [A██][B███][C█][pad] → GPU ~30%
Continuous: [A██][B███][C█][D██] → GPU ~80%""",
        'flash': """FlashAttention: 减少HBM访问
标准: Q,K,V→HBM, 计算S, 写HBM, 读HBM, 计算O → O(n²) HBM访问
Flash: 分块加载到SRAM, 中间结果留在SRAM, 一次性写回 → O(n²d/M)""",
        'parallel': """三种并行策略
TP: [GPU0部分权重][GPU1部分权重][GPU2部分权重] 每层通信
PP: [GPU0:L0-7][GPU1:L8-15][GPU2:L16-23] 层间通信
DP: [GPU0:batch0][GPU1:batch1][GPU2:batch2] 只同步梯度""",
        'moe': """MoE 混合专家
输入→Router→[E1][E2][E3][E4][E5]
              0.1 0.4 0.05 0.4 0.05
                 │       │
              w2×E2 + w4×E4 (只算Top-K)""",
        'nccl': """Ring AllReduce (4 GPUs)
Step1: GPU0→1:chunk0, GPU1→2:chunk1, ... (Scatter-Reduce)
Step2: GPU0→1:聚合chunk0, ... (AllGather)
总通信量: 2×(N-1)/N × D ← 带宽最优""",
        'gpu': """GPU 内存层次
HBM(80GB,2TB/s) → L2(50MB,10TB/s) → SRAM(20MB,19TB/s) → Register(最快)
FlashAttention: 减少HBM访问, 多用SRAM""",
        'longctx': """上下文长度 vs 开销 (7B)
4K:   KV=1GB,   O(16M),  ~0.1s
128K: KV=32GB,  O(16G),  ~5s
1M:   KV=256GB, O(1T),   ~60s""",
    }
    raw = diagrams.get(cat, f'{h2_text}\n┌──────────────────────────────┐\n│  参见对应技术文档获取详细架构  │\n└──────────────────────────────┘')
    return f'<div class="ascii"><pre>{raw}</pre></div>'


def make_table(cat, h2_text):
    """Generate comparison table based on topic category."""
    tables = {
        'inference': '<table><tr><th>维度</th><th>训练</th><th>推理</th></tr><tr><td>计算模式</td><td>前向+反向</td><td>仅前向</td></tr><tr><td>延迟要求</td><td>天/周</td><td>毫秒/秒</td></tr><tr><td>成本特征</td><td>一次性</td><td>持续性</td></tr></table>',
        'attention': '<table><tr><th>变体</th><th>复杂度</th><th>适用</th></tr><tr><td>标准</td><td>O(n²d)</td><td>通用</td></tr><tr><td>FlashAttn</td><td>O(n²d)IO减少</td><td>长序列</td></tr><tr><td>线性</td><td>O(nd²)</td><td>超长序列</td></tr><tr><td>GQA/MQA</td><td>减少KV头</td><td>推理加速</td></tr></table>',
        'kvcache': '<table><tr><th>方法</th><th>压缩比</th><th>精度影响</th></tr><tr><td>KV量化INT8</td><td>2x</td><td>&lt;1%</td></tr><tr><td>KV量化INT4</td><td>4x</td><td>1-3%</td></tr><tr><td>GQA</td><td>4-8x</td><td>&lt;1%</td></tr><tr><td>PagedAttn</td><td>减碎片</td><td>0%</td></tr></table>',
        'quantize': '<table><tr><th>方法</th><th>精度</th><th>速度</th></tr><tr><td>GPTQ</td><td>★★★★</td><td>★★★</td></tr><tr><td>AWQ</td><td>★★★★★</td><td>★★★★</td></tr><tr><td>GGUF</td><td>★★★</td><td>★★★</td></tr><tr><td>SmoothQuant</td><td>★★★★★</td><td>★★★★</td></tr></table>',
        'batch': '<table><tr><th>策略</th><th>GPU利用率</th><th>延迟</th></tr><tr><td>Static</td><td>~30%</td><td>高</td></tr><tr><td>Continuous</td><td>~80%</td><td>低</td></tr><tr><td>Chunked Prefill</td><td>~85%</td><td>更低</td></tr></table>',
        'framework': '<table><tr><th>框架</th><th>核心特性</th><th>适用</th></tr><tr><td>vLLM</td><td>PagedAttn</td><td>通用</td></tr><tr><td>TRT-LLM</td><td>NVIDIA优化</td><td>NVIDIA</td></tr><tr><td>TGI</td><td>HF生态</td><td>快速部署</td></tr><tr><td>SGLang</td><td>RadixAttn</td><td>复杂推理</td></tr></table>',
        'moe': '<table><tr><th>模型</th><th>总参数</th><th>激活</th><th>专家</th></tr><tr><td>Mixtral 8x7B</td><td>46.7B</td><td>12.9B</td><td>8</td></tr><tr><td>DeepSeek-V3</td><td>671B</td><td>37B</td><td>256</td></tr></table>',
        'gpu': '<table><tr><th>GPU</th><th>显存</th><th>FP16算力</th><th>带宽</th></tr><tr><td>A100</td><td>80GB</td><td>312T</td><td>2.0TB/s</td></tr><tr><td>H100</td><td>80GB</td><td>990T</td><td>3.35TB/s</td></tr><tr><td>H200</td><td>141GB</td><td>990T</td><td>4.8TB/s</td></tr></table>',
        'nccl': '<table><tr><th>操作</th><th>语义</th><th>用途</th></tr><tr><td>AllReduce</td><td>全局归约广播</td><td>梯度同步</td></tr><tr><td>AllGather</td><td>全局收集</td><td>参数广播</td></tr><tr><td>AllToAll</td><td>全局交换</td><td>MoE分发</td></tr></table>',
        'finetune': '<table><tr><th>方法</th><th>参数量</th><th>显存</th><th>效果</th></tr><tr><td>全量</td><td>100%</td><td>极高</td><td>★★★★★</td></tr><tr><td>LoRA</td><td>0.1-1%</td><td>中</td><td>★★★★</td></tr><tr><td>QLoRA</td><td>0.1-1%</td><td>低</td><td>★★★★</td></tr></table>',
        'rag': '<table><tr><th>方式</th><th>优势</th><th>劣势</th></tr><tr><td>BM25</td><td>精确匹配强</td><td>语义弱</td></tr><tr><td>向量检索</td><td>语义强</td><td>精确弱</td></tr><tr><td>混合+Reranker</td><td>效果最好</td><td>延迟增加</td></tr></table>',
    }
    return tables.get(cat, f'<table><tr><th>方面</th><th>要点</th><th>注意</th></tr><tr><td>核心</td><td>{h2_text}</td><td>理解机制比记忆参数重要</td></tr><tr><td>实践</td><td>项目中的使用</td><td>先跑通demo再优化</td></tr></table>')


def build_teaching_block(cat, h2_text):
    """Build complete teaching block for one h2 section."""
    tip = TIPS.get(cat, TIPS['default'])
    warn = WARNS.get(cat, WARNS['default'])
    deep = DEEPS.get(cat, DEEPS['default'])
    ascii_fig = make_ascii(cat, h2_text)
    table = make_table(cat, h2_text)
    return f"""
<div class="tip"><strong>通俗类比：</strong>{tip}</div>
<div class="warn"><strong>常见误区：</strong>{warn}</div>
<div class="deep"><strong>深入探讨：</strong>{deep}</div>
{ascii_fig}
{table}
"""


def enhance_file(file_path, dry_run=False):
    """Enhance a single B-level HTML file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return {'status': 'error', 'error': str(e), 'file': file_path}

    content_new, css_added = inject_css(content)
    h2s = find_h2_blocks(content_new)

    if not h2s:
        if css_added and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_new)
        return {'status': 'skip' if not css_added else 'css_only', 'file': file_path, 'css': css_added}

    insertions = []
    for i, h2 in enumerate(h2s):
        if has_teaching_after(content_new, h2['end']):
            continue
        cat = get_keyword_match(h2['text'], file_path)
        block = build_teaching_block(cat, h2['text'])
        insertions.append({'pos': h2['end'], 'block': block, 'text': h2['text'], 'cat': cat})

    if not insertions:
        if css_added and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content_new)
        return {'status': 'skip' if not css_added else 'css_only', 'file': file_path, 'css': css_added}

    insertions.sort(key=lambda x: x['pos'], reverse=True)
    for ins in insertions:
        rest = content_new[ins['pos']:]
        offset = len(rest) - len(rest.lstrip())
        point = ins['pos'] + offset
        content_new = content_new[:point] + ins['block'] + "\n" + content_new[point:]

    if not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content_new)

    return {
        'status': 'enhanced', 'file': file_path, 'css': css_added,
        'sections': len(insertions), 'cats': [ins['cat'] for ins in insertions],
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 enhance-b-level-files.py <path> [--dry-run]")
        sys.exit(1)

    path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv

    if os.path.isfile(path):
        r = enhance_file(path, dry_run=dry_run)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif os.path.isdir(path):
        results = []
        for root, dirs, files in os.walk(path):
            for f in sorted(files):
                if not f.endswith('.html'):
                    continue
                fpath = os.path.join(root, f)
                try:
                    with open(fpath, 'r', encoding='utf-8') as fh:
                        head = fh.read(5000)
                    # PITFALL: Must check BOTH CSS definitions AND actual teaching elements.
                    # Files with CSS but no teaching elements should still be processed.
                    has_css_tip = bool(re.search(r'(?<![a-zA-Z0-9_-])\.tip\s*\{', head))
                    has_css_warn = bool(re.search(r'(?<![a-zA-Z0-9_-])\.warn\s*\{', head))
                    has_css_deep = bool(re.search(r'(?<![a-zA-Z0-9_-])\.deep\s*\{', head))
                    has_els = 'class="tip"' in head or 'class="warn"' in head or 'class="deep"' in head
                    if has_css_tip and has_css_warn and has_css_deep and has_els:
                        continue  # Already A-level (has both CSS and content)
                except:
                    pass
                r = enhance_file(fpath, dry_run=dry_run)
                results.append(r)
                if r['status'] == 'enhanced':
                    sys.stderr.write(f"  ✓ {os.path.basename(fpath)}: {r['sections']} sections\n")

        enhanced = [r for r in results if r['status'] == 'enhanced']
        skipped = [r for r in results if r['status'] == 'skip']
        errors = [r for r in results if r['status'] == 'error']
        css_only = [r for r in results if r['status'] == 'css_only']

        print(f"\n=== Done ===")
        print(f"Total: {len(results)} | Enhanced: {len(enhanced)} | CSS-only: {len(css_only)} | Skipped: {len(skipped)} | Errors: {len(errors)}")
        if enhanced:
            print(f"Total sections enhanced: {sum(r['sections'] for r in enhanced)}")
        if errors:
            for e in errors:
                print(f"  ERROR: {e['file']}: {e.get('error','')}")
    else:
        print(f"Path not found: {path}")
        sys.exit(1)


if __name__ == '__main__':
    main()
