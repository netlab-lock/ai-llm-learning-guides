# Breadth + Depth Two-Dimensional Audit Methodology

When reviewing a multi-module technical guide, audit on TWO independent dimensions:

## Dimension 1: Breadth (广度) — Are all topics covered?

### Keyword Coverage Check
Run a keyword search across ALL files for every topic that should be covered:

```bash
base="/path/to/guide/"
for kw in 'Topic1' 'Topic2' 'Topic3' ...; do
  cnt=$(grep -rl "$kw" ${base}*.html 2>/dev/null | wc -l)
  if [ $cnt -gt 0 ]; then echo "  ✅ $kw ($cnt files)"; else echo "  ❌ $kw"; fi
done
```

**Target**: 90%+ keyword coverage. Missing keywords = missing topics.

### Category Coverage Check
For the specific domain, list ALL expected sub-topics and verify each:

Example for collective communication:
- Primitives: Broadcast, Scatter, Gather, Reduce, AllGather, ReduceScatter, AllReduce, All-to-All, Barrier, Scan
- Algorithms: Ring, Tree, Double Tree, Recursive Halving, Recursive Doubling, Rabenseifner, Bruck, Binomial
- Hardware: NVLink, NVSwitch, PCIe, CXL, IB, RoCE, RDMA, GPUDirect
- Libraries: NCCL, MPI, Gloo, RCCL, HCCL
- Advanced: SHARP, NVLS, NVSHMEM, MSCCL++, UALink, UEC, CPO

## Dimension 2: Depth (深度) — Is each topic truly explained?

### Depth Marker Count
Count occurrences of depth-indicating patterns in each file:

```python
depth_checks = {
    "为什么(Why)": "为什么",
    "原理(Principle)": "原理",
    "工作方式(How)": "工作方式|工作原理|怎么工作|如何实现",
    "对比分析(vs)": "vs|对比|区别|不同",
    "实际数据(Numbers)": "GB/s|Gbps|μs|ms|TFLOPS",
    "代码示例(Code)": "python|import|def |class |torch\.",
    "公式推导(Formula)": "公式|推导|证明|=.*×|=.*/",
    "ASCII图解(Diagram)": 'class="ascii"',
    "历史背景(History)": "年|历史|演进|首次",
    "局限性(Limitation)": "局限|缺点|问题|瓶颈|不足",
    "最佳实践(Best Practice)": "最佳实践|推荐|建议|应该",
    "向前串联(Forward Link)": "向前串联|如何影响|直接影响|决定了",
    "内部机制(Internal)": "内部机制|工作机制|内部工作|怎么工作",
}
```

### Depth Quality Assessment
For each module, check:
- **"为什么" count**: Should be ≥5 per module. If <3, the module only describes "what" without explaining "why"
- **"工作方式" count**: Should be ≥3 per module. If 0, the module lacks mechanism explanations
- **"向前串联" count**: Should be ≥1 per module. If 0, the module is isolated — reader can't see how it connects to later topics
- **"内部机制" count**: Should be ≥1 for hardware/software modules. If 0, the module only describes "what exists" without "how it works internally"
- **"公式/推导" count**: Should be ≥5 for algorithm modules, ≥2 for hardware modules
- **"代码" count**: Should be ≥3 for practical modules, ≥1 for all modules
- **"局限性" count**: Should be ≥2 per module. Balanced coverage includes limitations

### Visualization
Create a bar chart per module to spot weak dimensions:
```
Module 01:  为什么 ████░░ 4    工作方式 ░░░░░░ 0    代码 ░░░░░░ 0
Module 13:  为什么 ████░░ 14   工作方式 █░░░░░ 1    代码 █████░ 40
```

## The "浮于表面" Test (Surface-Level Test)

A module is "浮于表面" (surface-level) if:
1. It explains WHAT something is but not WHY it was designed that way
2. It lists features but doesn't explain the INTERNAL MECHANISM
3. It has concepts but no FORMULAS or MATHEMATICAL PROOFS
4. It has tables but no ASCII DIAGRAMS showing how things connect
5. It has no CODE EXAMPLES showing how to actually use it
6. It doesn't connect to LATER MODULES — reader can't see the dependency chain

**Fix**: For each surface-level module, add:
- "为什么这样设计" section (design rationale)
- "内部工作机制" section with ASCII diagram showing physical/logical mechanism
- "向前串联" section connecting to 2-3 later modules with concrete mechanisms
- Mathematical formulas or complexity analysis
- Runnable code example
- Limitations and failure modes

## Theory-to-Practice Bridge Pattern

When a guide has strong theory but weak practice, create a dedicated "实操" module:

**What to include**:
1. **API/Code examples** — How to call the theoretical primitives in real code
2. **Configuration recipes** — Copy-paste configs for common frameworks
3. **Benchmarking commands** — How to measure what the theory predicts
4. **Profiling workflow** — How to diagnose performance issues
5. **Production case studies** — Real problems and how they were solved
6. **Common mistakes** — Pitfalls that theory doesn't prepare you for

**Example**: For collective communication:
- Theory module covers Ring AllReduce algorithm
- Practice module shows: PyTorch DDP code, nccl-tests commands, NCCL_DEBUG interpretation, production troubleshooting cases

## Audit Report Template

```markdown
## 审查报告

### 广度检查
- 覆盖关键词: X/Y (Z%)
- 缺失主题: [list]

### 深度检查
| 模块 | 为什么 | 工作方式 | 向前串联 | 内部机制 | 对比 | 数据 | 代码 | 公式 | 图解 | 评级 |
|------|--------|----------|----------|----------|------|------|------|------|------|------|
| 01   | 4      | 0        | 0        | 0        | 3    | 10   | 0    | 5    | 6    | ⚠️   |
| 13   | 14     | 1        | 0        | 0        | 47   | 67   | 40   | 133  | 47   | ✅   |

### 结构性问题
1. [issue 1]
2. [issue 2]

### 优先修复建议
1. [P0 fix]
2. [P1 fix]
```
