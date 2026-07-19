# Collective Communication (集合通信) — Knowledge Landscape

Reference map for building a systematic learning guide. Covers hardware interconnects, network protocols, communication primitives, algorithms, and libraries used in distributed AI training/inference.

## Knowledge Tree

```
硬件层 (Hardware Interconnects)
├── PCIe — GPU↔CPU 通用总线 (PCIe 5.0 x16 ≈ 64 GB/s)
├── NVLink — GPU↔GPU 高速直连 (H100: 900 GB/s, Blackwell: 1.8 TB/s)
├── NVSwitch — 多GPU交换芯片 (H100: 8卡全连接, Blackwell NVL72: 72卡)
├── NVLink-C2C — Die-to-Die 芯片间互联 (Grace Hopper用)
├── IO Die — 芯片内负责I/O的独立小芯片 (PCIe/NVLink/内存控制器)
├── Compute Die — 芯片内负责计算的小芯片 (GPC/SM/CUDA Core)
└── HBM — 高带宽内存 (HBM3e: 4.8 TB/s per stack)

网络层 (Network Protocols for Cross-Node)
├── RDMA — 远程直接内存访问 (零拷贝, 绕过CPU)
│   ├── InfiniBand — 专用高速网络 (HDR: 200Gb/s, NDR: 400Gb/s)
│   ├── RoCE v2 — 以太网上跑RDMA (需要无损网络/PFC/ECN)
│   └── iWARP — TCP上跑RDMA (较少用)
├── GPUDirect — GPU与外部设备直接通信
│   ├── GPUDirect Storage — GPU↔NVMe 直连
│   └── GPUDirect RDMA — GPU↔NIC 直连 (绕过CPU和系统内存)
└── TCP/IP — 传统网络 (延迟高, CPU开销大, 仅作fallback)

通信原语 (Collective Primitives)
├── Broadcast — 一对多 (1→N)
├── Reduce — 多对一 + 归约操作 (N→1)
├── AllReduce — 所有人得到归约结果 (N→N) ★最常用
├── AllGather — 所有人收集所有人的数据片段 (N→N)
├── ReduceScatter — 归约 + 分散 (N→N)
├── All-to-All — 每人给每人发不同数据 (N→N, 全交换)
└── Barrier — 同步屏障 (所有人到达后才继续)

关键等式: AllReduce = ReduceScatter + AllGather

通信算法 (Communication Algorithms)
├── Ring AllReduce — 环形传递, 带宽最优, 延迟随GPU数线性增长
├── Tree AllReduce — 树形传递, 延迟最优(log N), 带宽不均
├── Recursive Halving/Doubling — 超算常用
└── NCCL实际做法 — Ring + Tree混合, 按数据量选择

通信库 (Communication Libraries)
├── NCCL — NVIDIA集体通信库 (最主流, 支持NVLink/IB/RoCE)
├── Gloo — Facebook (PyTorch默认CPU后端)
├── MPI — 老牌HPC标准 (OpenMPI, MPICH)
├── HCCL — 华为昇腾
├── XCCL — 百度XPU
└── OneCCL — Intel

网络拓扑 (Network Topologies for Large Clusters)
├── Fat-Tree (胖树) — 传统HPC, 无阻塞, 成本高
├── Dragonfly — 低直径, 高带宽, 适合超大规模
├── Rail-Only — NVIDIA推荐, GPU直连交换机, 减少跳数
└── Torus/Mesh — 3D/2D环面, 适合特定硬件 (TPU)
```

## New Hardware (2025-2026)
- NVLink 6.0 (Rubin VR200): 3.6 TB/s per GPU, NVL72 = 260 TB/s aggregate
- CXL 3.0: memory pooling across servers, cache-coherent
- UALink 1.0: open accelerator interconnect (200 Gbps/lane), AMD/Intel/Google/Meta
- UEC 1.0: AI-optimized Ethernet, congestion-aware, multi-path, in-network collectives
- CPO (Co-Packaged Optics): 3-5 pJ/bit, enables 100K+ GPU clusters

## 13 Algorithms
Ring, Tree, Double Binary Tree, Recursive Halving, Recursive Doubling,
Rabenseifner (latency+bandwidth optimal), Bruck, Binomial Tree,
Scatter-Allgather, Direct Exchange, Pairwise Exchange, NVLS, SHARP

## Pipeline Bubble Formulas
GPipe: (p-1)/(m+p-1) ~50% | 1F1B: ~30% | Interleaved: ~15% | Zero-Bubble/DualPipe: ~3-5%

## New Parallel Strategies (2024-2026)
DualPipe (bidirectional PP), DP Attention (zero-comm attention), Context Parallelism (Ring+USP+StarTrail)

## Compression: FP8 (2x), 1-bit Adam (16x), TopK+ErrorFeedback (10-100x), PowerSGD (low-rank)

## Production Metrics
MFU: >35% OK, >45% good, >50% excellent. Comm overhead: <15% OK, <10% good.
nccl-tests efficiency: 80%+ single node, 70%+ 8 nodes, 60%+ 64 nodes.
```

## Key Concepts for Beginners

### IO Die vs Compute Die
- Modern GPUs/CPUs use chiplet architecture (多个小芯片封装)
- Compute Die: 执行计算 (CUDA cores, Tensor cores, SM)
- IO Die: 管理所有对外接口 (PCIe控制器, NVLink PHY, 内存控制器)
- Analogy: Compute Die = 研发部门, IO Die = 行政/前台

### NVLink vs PCIe
- PCIe: 通用总线, CPU和所有外设共享, 带宽有限
- NVLink: GPU专用, 点对点直连, 带宽10-15x PCIe
- NVSwitch: 让NVLink从"点对点"变成"全连接"

### RDMA vs Traditional Networking
- Traditional: App → Kernel → NIC → Network → NIC → Kernel → App (多次拷贝, CPU参与)
- RDMA: App → NIC → Network → NIC → App (零拷贝, CPU不参与)
- GPUDirect RDMA: GPU memory → NIC → Network (连系统内存都绕过)

### AllReduce为什么最重要
- 数据并行训练中, 每个GPU计算自己的梯度
- 需要把所有GPU的梯度汇总取平均, 然后更新模型
- 这个"汇总+广播"就是AllReduce
- 占据了分布式训练中绝大部分通信时间

## Planned Module Structure (for HTML guide)

1. 基础概念: 什么是集合通信, 为什么需要它
2. 硬件互联: PCIe → NVLink → NVSwitch → IO Die
3. RDMA与网络: RDMA原理, InfiniBand, RoCE
4. GPUDirect: GPU如何直接与网卡/NVMe通信
5. 通信原语: Broadcast, Reduce, AllReduce, AllGather, ReduceScatter
6. 通信算法: Ring, Tree, 混合算法
7. NCCL深入: 架构, 配置, 调优
8. 网络拓扑: Fat-Tree, Dragonfly, Rail-Only
9. 实战: PyTorch分布式训练中的集合通信
10. 前沿: NVLink Fusion, UALink, 超以太网

## Actual Module Structure (created 2026-05-25)

Final guide: 12 files / 201KB / 3,614 lines at `D:\学习\集合通信入门指南\`

```
01-芯片基础.html             376行  21KB   光刻/CoWoS/TSV/2.5D封装
02-GPU内部架构.html          319行  18KB   SM/Tensor Core/IO Die/内存层次
03-PCIe总线基础.html         255行  15KB   编码/带宽公式/延迟/TLP/DLLP
04-NVLink与NVSwitch.html    262行  16KB   NRZ vs PAM4/NVL72/NVLink Fusion
05-RDMA技术原理.html         284行  15KB   内存注册/lkey-rkey/Verbs/QP/WR/WC
06-InfiniBand与RoCE.html    280行  16KB   信用流控/PFC拥塞扩散/DCQCN/SM
07-GPUDirect技术.html        271行  14KB   PCIe BAR映射/GDR流程/GDS
08-集合通信原语.html          302行  16KB   六种原语/通信量公式/并行策略
09-AllReduce算法详解.html    391行  18KB   Ring推导/带宽公式2D/B/Double Tree
10-NCCL通信库.html           300行  16KB   架构/Channel/协议/分层策略
11-网络拓扑与大规模组网.html  368行  19KB   Fat-Tree数学/Dragonfly/SHARP
index.html                  206行  12KB   学习路线图/推荐资源
```

Each module follows the 8-dimension framework: 背景与动机→名字由来→核心原理→技术细节→使用场景→相似技术对比→关联技术→实际效果.

Key design decisions:
- User specified "侧重硬件架构和通信算法，实战部署不重点讲解"
- Used `.deep` CSS class (purple) for historical background sections
- All modules have exercises at the end
- Navigation: prev/next links + footer back to index
- Self-contained CSS (no external files)

## Sources
- NVIDIA NCCL docs: https://developer.nvidia.com/nccl
- NCCL GitHub: https://github.com/NVIDIA/nccl
- GPUDirect RDMA docs: https://docs.nvidia.com/cuda/gpudirect-rdma/
- NVLink: https://www.nvidia.com/en-us/data-center/nvlink/
- MindSpore collective ops: https://www.mindspore.cn/docs/programming_guide/zh-CN/r1.5/distributed_training_ops.html
- 阿里云 GPU通信技术: https://developer.aliyun.com/article/1606345

## Huawei Ascend Collective Communication (昇腾集合通信)

### Key Sources Found (2026-06)
- **CloudMatrix384 paper**: arXiv:2506.12708 — production benchmarks, EP320, MLA operator
- **UB protocol philosophy**: https://01.me/en/2025/09/a-story-of-unified-bus/ (Bojie Li, Huawei distributed lab)
- **DeepLink whitepaper**: https://deeplink-org.github.io/superpod-whitepaper/ (Shanghai AI Lab)
- **HCCL source**: https://gitee.com/ascend/cann-hccl (with docs/Ring.md, docs/RHD.md)
- **China Research Collective**: https://chinaresearchcollective.substack.com/p/huawei-ascend-cloudmatrix-384-supernode

### Ascend Interconnect Evolution
| Version | Chip | Bandwidth/NPU | Notes |
|---|---|---|---|
| HCCS 1.0 | 910 | ~25 GB/s | Initial high-speed interconnect |
| HCCS 3.0 | 910B | ~56 GB/s | Main training card interconnect |
| UB灵衢 | 910C | 196 GB/s | Bus-level unified interconnect, 3.5x improvement |

### CloudMatrix 384 Key Numbers
- 384 Ascend 910C NPUs + 192 Kunpeng CPUs
- UB: 224 Gbps transceivers × 7 per NPU = 196 GB/s unidirectional
- 7 sub-plane design, each independent full-mesh, zero contention
- L1: 336 UB switches (on-board), L2: 112 UB switches (rack-level)
- Three isolated network planes: UB (compute), RDMA (200Gbps RoCE), VPC (management)
- Total: ~300 PFLOPs BF16, 49.2 TB HBM, 269 TB/s interconnect BW
- Power: ~559 kW, 16 racks (12 compute + 4 communication)

### UB Protocol Design Philosophy
- **Core motivation**: Bridge the gap between buses (low latency, not scalable) and networks (scalable, high latency)
- **Peer architecture**: All devices are equal, can access each other's memory via Load/Store
- **Two memory modes**: Load/Store (sync, hundreds of ns) vs Read/Write (async, 2-5 μs)
- **Jetty**: Connectionless transport model (replaces RDMA's QP connection model, eliminates N² problem)
- **URMA**: Unified Remote Memory Access protocol
- **C-AQM**: Request-precise congestion control (better than ECN/DCQCN)
- **Weak ordering**: RO/NO/SO tags (gradient sync doesn't need strong ordering because addition is commutative)

### HCCL vs NCCL
| Dimension | HCCL | NCCL |
|---|---|---|
| Topology algorithms | 5: Mesh/Ring/RHD/PairWise/Star | 2: Ring/Tree |
| Interconnect | HCCS + UB (dual mode) | NVLink + NVSwitch (single mode) |
| Memory access | MTE async (software-managed) | GPUDirect (hardware cache) |
| Hierarchical comm | Built-in (node + inter-node) | Needs external libs (DeepSpeed) |
| Open source | 2024-end (Gitee) | 2015 (GitHub) |

### Ascend 950DT Roadmap (expected Aug 2026)
- HBM: 144 GB (海芝青2.0 self-developed), 4.0 TB/s bandwidth
- Dual-Die UMA architecture, on-device AI CPU
- FP8/BF16 > 1000 TFLOPS
- Next-gen CloudMatrix: 512+ NPUs, 280+ GB/s UB bandwidth
