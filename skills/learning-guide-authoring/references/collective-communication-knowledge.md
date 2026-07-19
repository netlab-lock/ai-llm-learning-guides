# Collective Communication for AI Training — Knowledge Bank

Collected from web research and guide authoring session (2026-05-24). Covers GPU interconnects, RDMA networking, and collective communication algorithms for distributed AI training.

## Hardware Interconnect Hierarchy

```
GPU内部:   HBM (3-8 TB/s) → L2 Cache → L1/SM
节点内:    NVLink (900-1800 GB/s) via NVSwitch
节点间:    InfiniBand NDR/XDR (400-800 Gbps) or RoCE v2
```

## Key Numbers (verified 2026-05)

| Component | Bandwidth | Latency |
|-----------|-----------|---------|
| H100 HBM3 | 3,350 GB/s | ~400-600 cycles |
| H100 NVLink 4.0 | 900 GB/s (18 links) | ~0.5 μs |
| B200 NVLink 5.0 | 1,800 GB/s (18 links, PAM4) | ~0.5 μs |
| PCIe 5.0 x16 | ~126 GB/s | ~1-6 μs |
| IB NDR (400G) | 50 GB/s per port | ~0.6 μs |
| IB XDR (800G) | 100 GB/s per port | ~0.4 μs |

## NVLink Version History

| Version | GPU | Links | Per-link | Total |
|---------|-----|-------|----------|-------|
| 1.0 | P100 (2016) | 4 | 20 GB/s | 160 GB/s |
| 2.0 | V100 (2017) | 6 | 25 GB/s | 300 GB/s |
| 3.0 | A100 (2020) | 12 | 25 GB/s | 600 GB/s |
| 4.0 | H100 (2022) | 18 | 25 GB/s | 900 GB/s |
| 5.0 | B200 (2024) | 18 | 50 GB/s | 1,800 GB/s |

NRZ→PAM4 transition at NVLink 5.0 (doubled per-link bandwidth).

## Collective Communication Primitives

| Primitive | Direction | Per-GPU comm | Use case |
|-----------|-----------|-------------|----------|
| Broadcast | 1→N | D | Model init |
| Reduce | N→1 | D | Loss汇总 |
| AllReduce | N→N | 2D(N-1)/N | Gradient sync ★most important |
| AllGather | N→N | 2D(N-1)/N | Tensor parallel |
| ReduceScatter | N→N | 2D(N-1)/N | AllReduce step 1 |
| All-to-All | N→N | 2D(N-1)/N | MoE expert routing |

**Core identity**: AllReduce = ReduceScatter + AllGather

## AllReduce Algorithms

### Ring AllReduce
- Steps: 2(N-1)
- Per-GPU comm: 2D(N-1)/N ≈ 2D (bandwidth-optimal)
- Latency: O(N) — linear with GPU count
- Best for: few GPUs, large messages

### Tree AllReduce
- Steps: 2log₂(N)
- Per-GPU comm: D×log₂(N)
- Latency: O(log N)
- Bandwidth utilization: ~50% (only half links active per level)

### Double Binary Tree (NCCL 2.4+)
- Steps: 2log₂(N)
- Two trees work simultaneously → ~2x bandwidth vs single tree
- Best for: many GPUs, balanced bandwidth+latency

### NCCL Strategy
- Intra-node (NVLink): Ring (high bandwidth utilization)
- Inter-node (IB): Double Tree (latency-controlled)
- Small messages: Tree (latency priority)

## RDMA Key Concepts

- **Zero Copy**: No intermediate memory copies (vs 4x in TCP/IP)
- **Kernel Bypass**: User-space driver, no context switches
- **Hardware Offload**: Protocol processing in NIC hardware
- **Memory Registration**: Lock physical pages, generate lkey/rkey
- **Operations**: Send/Recv (needs remote CPU), RDMA Write/Read (doesn't)

## GPUDirect RDMA (GDR)

Eliminates CPU memory as intermediary between GPU and NIC:
- Traditional: GPU→PCIe→CPU mem→PCIe→NIC (4 PCIe transfers)
- GDR: GPU→PCIe P2P→NIC (2 PCIe transfers)
- Requires GPU and NIC on same PCIe Root Complex
- ~2-3x latency improvement, ~1.6x bandwidth improvement

## Network Topologies

| Topology | Hops | Blocking | Cables | Scale |
|----------|------|----------|--------|-------|
| Fat-Tree | 4-6 | Non | O(N·logN) | 1K-30K GPUs |
| Dragonfly | 2-3 | Possible | O(N) | 10K+ GPUs |
| Rail-Only | 2-4 | Non | O(N) | 10K+ GPUs |

NVL72: 72 GPUs connected via NVLink Switch (no IB needed).

## NCCL Architecture

```
Application (PyTorch DDP / DeepSpeed / Megatron)
  ↓
NCCL API (ncclAllReduce, ncclBroadcast, ...)
  ↓
Core Engine: Topology Detection + Algorithm Selector + Channel Manager
  ↓
Transport Plugins: P2P (NVLink) | SHM (shared mem) | NET (IB/RoCE)
```

Key concepts: Channel (parallel ring/tree instances), Protocol (Simple/LL/LL128).

## Sources
- NCCL GitHub + Official Docs (developer.nvidia.com/nccl)
- Demystifying NCCL paper (arXiv:2507.12847, 2025)
- NVIDIA NVLink & NVSwitch docs (nvidia.cn/data-center/nvlink)
- GPUDirect RDMA docs (docs.nvidia.com/cuda/gpudirect-rdma)
- MindSpore collective communication docs
- CSDN/阿里云/知乎 technical blogs (various, 2024-2026)
