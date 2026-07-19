# Source Code Analysis via GitHub API (源码级研究)

## When to Use

When the user wants "源码级分析" or when documentation is insufficient and open-source code is available.

## Technique

Use the GitHub API to browse repo structure and read source files directly:

```bash
# Browse source tree structure
curl -s "https://api.github.com/repos/OWNER/REPO/contents/src" | python3 -c "
import json,sys
for f in json.load(sys.stdin):
    print(f'{f[\"type\"]:4s} {f[\"name\"]}')
"

# Read specific source files (raw content, no HTML)
curl -sL "https://raw.githubusercontent.com/OWNER/REPO/master/src/path/to/file.h" | head -200
```

## Key Files to Target

**Communication libraries (NCCL, HCCL):**
- include/*.h — Data structures, enums (algorithms, protocols)
- device/*.h — GPU kernel implementations (Ring/Tree execution)
- graph/*.cc — Topology detection, tuning constants
- init.cc — Initialization flow

## Validation: NCCL Source Code Analysis (2026-06)

Successfully extracted from github.com/NVIDIA/nccl:
- 7 algorithm enum values (Tree, Ring, CollNetDirect, CollNetChain, NVLS, NVLSTree, PAT)
- 3 protocol definitions (LL, LL128, Simple)
- Ring AllReduce step-by-step execution from all_reduce.h
- Double binary tree construction via bit manipulation from trees.cc
- Tuning constants: Tree base latency 6.8us, Ring 14.0us

## Pitfalls

- GitHub API rate limits (60 req/hr unauthenticated). Use raw.githubusercontent.com for file reads.
- Gitee has different API: gitee.com/api/v5/repos/OWNER/REPO/contents/path
- Source code comments may be in Chinese (HCCL) — valuable for design intent
