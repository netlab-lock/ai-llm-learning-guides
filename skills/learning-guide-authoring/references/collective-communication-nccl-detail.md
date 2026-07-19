# Collective Communication Knowledge Bank (NCCL + HCCL)

## NCCL Source Code Architecture (github.com/NVIDIA/nccl, v2.30.7)

### 7 Algorithms
| ID | Name | Use | Notes |
|----|------|-----|-------|
| 0 | Tree | AllReduce | Binary tree, O(logN) latency |
| 1 | Ring | All ops | Bandwidth-optimal, O(N) latency |
| 2 | CollNetDirect | AllReduce | Through network switch reduction |
| 3 | CollNetChain | AllReduce | Chained network reduction |
| 4 | NVLS | AllReduce | NVLink SHARP, SM90+ only |
| 5 | NVLSTree | AllReduce | NVLS intra-node + Tree inter-node |
| 6 | PAT | AllGather/ReduceScatter | Parallel Aggregated Tree |

### 3 Protocols
| Name | Line Size | Use |
|------|-----------|-----|
| LL | 8 bytes | Small messages, lowest latency |
| LL128 | 128 bytes | Medium messages |
| Simple | uint64_t grains | Large messages, highest bandwidth |

### Ring AllReduce (from all_reduce.h runRing)
Step 0: directSend (push own chunk)
Steps 1..N-2: directRecvReduceDirectSend (recv+reduce+send, 3 ops overlapped)
Step N-1: directRecvReduceCopyDirectSend (final reduce, postOp=true)
Steps N..2N-3: directRecvCopyDirectSend (copy only, AllGather phase)
Total: 2(N-1) steps, bandwidth-optimal at 2(1-1/N)×M

### Double Binary Tree (from trees.cc ncclGetDtree)
Tree 0: standard binary tree (rank ^ bit | bit<<1 for parent)
Tree 1: mirror (nranks-1-rank) or shift
Each rank is root in one tree, leaf in the other
Bandwidth-optimal + O(logN) latency

### Topology Path Types
LOC (same GPU) → NVL (NVLink) → NVB (NVSwitch) → C2C (CPU-GPU)
→ PIX (same PCIe switch) → PXB (PCIe bridge) → P2C (PCIe to CPU)
→ SYS (cross CPU socket) → NET (InfiniBand/RoCE)

### Tuning Constants (from tuning.cc)
Tree base latency: 6.8μs intra, 6.6μs inter
Ring base latency: 14.0μs intra, 14.0μs inter
PAT base latency: 8.0μs
NVLS efficiency: Hopper=0.85, Blackwell=0.74
LL max BW: Hopper 141 GB/s, Blackwell 282 GB/s

### Algorithm Selection Rules
Broadcast/Reduce: Ring only
ReduceScatter/AllGather: PAT, Ring, NVLS, CollNetDirect
AllReduce: Tree, Ring, CollNet*, NVLS (NOT PAT)
AllToAll: Ring only

## NVLink Version History
| Version | Chip | Bandwidth | Key Feature |
|---------|------|-----------|-------------|
| 1.0 | Pascal P100 | 160 GB/s | First GPU interconnect |
| 2.0 | Volta V100 | 300 GB/s | NVSwitch introduced |
| 3.0 | Ampere A100 | 600 GB/s | 12 links |
| 4.0 | Hopper H100 | 900 GB/s | SHARP, NVLink-C2C |
| 5.0 | Blackwell GB200 | 1800 GB/s | NVL72, NV-HBI 10TB/s |
| 6.0 | Rubin VR200 | 3600 GB/s | NVL72 260TB/s aggregate, Vera CPU |

## SHARP (Scalable Hierarchical Aggregation and Reduction Protocol)
- Hardware reduction INSIDE NVSwitch (in-network computation)
- AllReduce data gets summed while passing through the switch
- Effect: ~2× less communication (single trip instead of round-trip)
- Limitation: SM90+ only (Hopper/Blackwell), AllReduce only
- No equivalent in Huawei Ascend — major differentiator

## HCCL Algorithms (gitee.com/ascend/cann-hccl)
Mesh (intra-node), Ring (general), RHD (2^k nodes),
PairWise (AllToAll), Star (rooted ops)
RHD bandwidth: 2log₂N×M/N (better than Ring for large N)
Hierarchical: node-intra Mesh + inter-node Ring = ~22% of single-layer Ring

## NVSHMEM (PGAS for GPU-initiated communication)
- CPU-initiated (NCCL) vs GPU-initiated (NVSHMEM) — different programming models
- NCCL: batch collectives (AllReduce, AllGather), high throughput
- NVSHMEM: fine-grained point-to-point (put, get, atomic), GPU kernel can call directly
- Use cases: sparse gradients, GNN neighbor aggregation, MoE dynamic routing
- NCCL 2.24+ uses NVSHMEM internally for some operations
- API: `nvshmem_float_put()`, `nvshmem_float_get()`, `nvshmem_quiet()`

## NCCL Tuning Environment Variables (Production)
| Variable | Default | Purpose |
|----------|---------|---------|
| NCCL_ASYNC_ERROR_HANDLING | 0 | MUST set to 1 for production |
| NCCL_IB_HCA | auto | Specify IB HCA (e.g., `=mlx5_0,mlx5_1`) |
| NCCL_ALGO | auto | Force algorithm: Ring/Tree/NVLS |
| NCCL_PROTO | auto | Force protocol: Simple/LL/LL128 |
| NCCL_MIN_NCHANNELS | auto | Min parallel channels (4-8) |
| NCCL_MAX_NCHANNELS | auto | Max channels (16-32) |
| NCCL_BUFFSIZE | 4M | Communication buffer size |
| NCCL_NVLS_ENABLE | 1 | Enable NVLink SHARP (Hopper+) |
| NCCL_DEBUG | WARN | INFO for debugging |

## MSCCL++ (Microsoft GPU-driven communication library)
- GPU-driven scheduling (moves logic from CPU to GPU)
- Custom collective primitives beyond NCCL's standard set
- Abstracted transport: supports IB, RoCE, shared memory
- Used in Azure Maia AI accelerator stack
- GitHub: github.com/microsoft/mscclpp
- Key paper: "SpeCL: GPU Communication Abstractions" (arXiv:2504.09014)

## Open Standards (2025-2026)
- **UALink**: Open accelerator interconnect (AMD/Intel/Google/Meta). 200 Gbps/lane. Scale-up.
- **UEC (Ultra Ethernet)**: AI-optimized Ethernet (congestion-aware, multi-path, in-network collectives). Scale-out.
- Together: UALink (node-intra) + UEC (node-inter) = open alternative to NVLink + IB

## Key Comparison Points
| Dimension | NVIDIA | Huawei |
|-----------|--------|--------|
| Max Scale-Up | 72 GPU (NVL72) | 384 NPU (CloudMatrix) |
| Per-GPU BW | 1800 GB/s | 392 GB/s |
| HW Reduction | SHARP (NVSwitch) | None |
| Memory Access | Load/Store (HW cache) | MTE async (SW scratchpad) |
| Transport | Direct + NVSwitch | Jetty (connectionless) |
| Ordering | Strong | Weak (RO/NO/SO) |
| Algorithms | 7 (incl NVLS/PAT) | 5 (incl Mesh/RHD) |
