# 深度要求与 SVG 图规范 (2026-06 补充)

## 用户深度要求 — 核心教训

用户反复强调："不要浮于概念，要深入"、"拿出写书的精神"。

### 三层深度标准

每个技术主题必须覆盖三层，缺一不可：

| 层次 | 内容 | 反面教材 |
|------|------|---------|
| **概念层** | 是什么、为什么需要 | 只停留在这层 = "泛泛而谈" |
| **实现层** | 源码级分析、伪代码、数据结构、算法流程 | 只讲概念不讲实现 = "浮于表面" |
| **数据层** | 真实 benchmark、具体参数、量化公式推导 | 只有定性没有定量 = "不够深入" |

### 必须包含的深度内容类型

1. **源码级请求追踪** — 从 API 入口到执行的完整调用链，带实际类名/方法名
2. **核心算法伪代码** — 不是描述算法，是写出算法的伪代码并逐行注释
3. **数学公式推导** — 量化公式、通信量计算、内存估算，带具体数值示例
4. **CUDA/kernel 原理** — 内存访问模式、计算复杂度、SIMD 指令使用
5. **真实 benchmark 数据** — 搜集最新的吞吐/延迟数据，用搜索工具获取
6. **参数调优的具体影响** — 不是"调大调小"，是"设为 X 时吞吐从 Y 变为 Z"
7. **面试高频问题** — 每个框架 4-5 个 Q&A，答案要深入到实现细节

### 内容深度检查清单

写完一个技术指南后自检：
- [ ] 有没有源码级的代码片段（不是 shell 命令）？
- [ ] 有没有数学公式或算法伪代码？
- [ ] 有没有具体数字（benchmark、参数值、内存大小）？
- [ ] 如果删掉所有概念描述，剩下的实现细节还能独立成文吗？
- [ ] 面试官追问实现细节时，这份指南能回答吗？

## SVG 架构图规范

### 设计系统

| 元素 | 配色 (fill) | 描边 (stroke) | 用途 |
|------|-------------|---------------|------|
| API/Server 层 | `rgba(8,51,68,0.4)` | `#22d3ee` (cyan) | 接口、网关、前端 |
| 核心引擎 | `rgba(6,78,59,0.4)` | `#34d399` (emerald) | 调度器、执行器、运行时 |
| 内存/缓存 | `rgba(76,29,149,0.4)` | `#a78bfa` (violet) | KV Cache、内存池 |
| GPU/硬件 | `rgba(120,53,15,0.3)` | `#fbbf24` (amber) | GPU、Tensor Core |
| 高亮/警告 | 透明 | `#fb7185` (rose) | 重要标注、瓶颈 |
| 次要/外部 | `rgba(30,41,59,0.5)` | `#94a3b8` (slate) | 外部依赖、辅助 |

### 组件规范

```html
<!-- 标准组件: 圆角矩形 + 半透明填充 -->
<rect x="100" y="50" width="200" height="60" rx="6" 
      fill="rgba(6,78,59,0.4)" stroke="#34d399" stroke-width="1.5"/>
<text x="200" y="75" fill="#e6edf3" font-size="12" font-weight="600" 
      text-anchor="middle">组件名称</text>
<text x="200" y="92" fill="#94a3b8" font-size="9" 
      text-anchor="middle">子标签</text>

<!-- 箭头 marker -->
<defs>
  <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
    <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
  </marker>
</defs>

<!-- 连线 -->
<line x1="300" y1="80" x2="400" y2="80" stroke="#64748b" stroke-width="1.5" 
      marker-end="url(#arr)"/>
```

### 嵌入方式

SVG 直接内嵌在 HTML 页面中，不用外链文件。用 `<div class="diagram">` 包裹。

```html
<div class="diagram" style="padding:0;overflow:hidden">
  <svg viewBox="0 0 900 600" width="100%" style="display:block">
    <rect width="900" height="600" fill="#161b22"/>
    <!-- 组件和连线 -->
  </svg>
</div>
```

### viewBox 规范

- 宽度: 900px (单列) 或 860px (紧凑)
- 高度: 根据内容，通常 300-700px
- 内边距: 组件距边缘至少 40px
- 组件间距: 垂直 30-50px，水平 20-40px

## 子 agent 并行生成大文件的模式

### 最佳实践

1. **先调研再写** — 用 `ddgs text -k "..." -m 5` 搜集最新数据
2. **子 agent 并行写多个文件** — 每个框架/主题一个子 agent
3. **最大并发 3** — `max_concurrent_children: 3`，超过会报错
4. **子 agent 生成 HTML 用 Python 脚本** — 比直接 write_file 大段 HTML 更可靠
5. **ASCII→SVG 转换** — 子 agent 生成 Python 脚本批量替换 `class="diagram"` 块

### 常见陷阱

- **429 限流** — 子 agent 用搜索工具时容易触发。降低并发或减少搜索次数
- **600s 超时** — `child_timeout_seconds` 配置有时不生效(可能是 CLI_CONFIG 加载问题)。如果子 agent 600s 超时，检查配置是否在 `delegation:` 节点下
- **子 agent 中断** — 如果父 agent 收到新消息，子 agent 会被 interrupt。确保父 agent 空闲
- **patch 冲突** — 多个子 agent 同时 patch 同一个文件会冲突。每个子 agent 只负责一个文件
- **write_file 大文件** — 超过 100KB 的 HTML 用 terminal 的 Python 脚本写入更可靠

### 质量验证流程

写完后用浏览器检查：
```bash
# 在浏览器中打开文件
open /path/to/file.html   # macOS
xdg-open /path/to/file.html  # Linux
```

用 browser_vision 检查：
- 颜色是否正确显示
- 文字是否清晰可读
- 布局是否合理，有没有溢出截断
- SVG 图的组件是否有圆角和半透明效果
- 箭头连线是否可见
