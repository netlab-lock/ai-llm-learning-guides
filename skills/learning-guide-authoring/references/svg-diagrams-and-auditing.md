# SVG Diagrams & Iterative Auditing

## SVG Architecture Diagrams (优于ASCII)

**用户明确偏好**: 在HTML指南中，SVG图远优于ASCII art。用户说："html下不是有办法画出更好看，更直观的图吗？"

**实现方式**: 使用 `architecture-diagram` 技能的设计系统创建内联SVG图：
- 语义化颜色: 应用=青色(#22d3ee), 编排=绿色(#34d399), 能力=紫色(#a78bfa), 模型=琥珀(#fbbf24), 安全=玫红(#fb7185)
- 暗色背景: #020617 + 40px网格线(#1e293b)
- 圆角矩形: rx="6", 1.5px stroke
- 半透明填充: rgba(color, 0.08-0.4)

**SVG wrapper模板**:
```python
def svg(title, content, w=900, h=400):
    return f'''<div class="diagram">
<div class="diagram-title">{title}</div>
<svg width="100%" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 7" refX="10" refY="3.5" markerWidth="8" markerHeight="6" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#475569"/>
    </marker>
  </defs>
  <rect width="{w}" height="{h}" fill="#020617" rx="8"/>
  <rect width="{w}" height="{h}" fill="url(#grid)" rx="8"/>
{content}
</svg>
</div>'''
```

**何时用SVG vs ASCII**:
- SVG: 架构图、流程图、层次图、对比图（核心图必须用SVG）
- ASCII: 小型对比表(3-4行)、简单流程(2-3步)、代码输出示例

**CSS注入**: 在HTML的 `<style>` 标签中加入:
```css
.diagram{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin:1.5rem 0}
.diagram-title{color:var(--blue);font-weight:700;font-size:1.05em;margin-bottom:1rem;text-align:center}
```

## 面试专题模块创建模式

1. **调研真实JD**: 用 `ddgs text -k "XX岗位 面试题 2025 2026"` 搜索真实面试题
2. **结构化Q&A**: 每个问题包含 回答要点 + 追问方向 + 面试回答模板
3. **STAR模板**: 项目经验用 Situation-Task-Action-Result 结构
4. **准备清单**: 按优先级排序，附建议准备天数

## 迭代审计模式 (7轮实战经验)

| 轮次 | 检查维度 | 典型发现 |
|------|----------|----------|
| 1 | 元素计数 | 缺tip/warn/exercise/deep框 |
| 2 | 主题覆盖度 | 缺chunking/JSON Schema等具体技术 |
| 3 | 全局缺失 | 缺Grounding/红队测试等跨模块主题 |
| 4 | 模块内子主题 | 缺Least-to-Most/垂直行业等 |
| 5 | 节级密度 | 某些h2节只有14行，需要充实 |
| 6 | 面试覆盖 | 缺RAG/微调/Harness等面试高频主题 |
| 7 | 视觉质量 | ASCII图应升级为SVG |

**审计命令**:
```bash
# 元素计数 + 密度检查
for f in *.html; do
  chars=$(sed 's/<[^>]*>//g' "$f" | tr -d '[:space:]' | wc -c)
  h2=$(grep -c '<h2' "$f"); avg=$((chars / h2))
  t=$(grep -c 'class="tip"' "$f"); w=$(grep -c 'class="warn"' "$f")
  e=$(grep -c 'class="exercise"' "$f"); d=$(grep -c 'class="deep"' "$f")
  a=$(grep -c 'class="ascii"' "$f"); s=$(grep -c '<svg' "$f")
  printf "%-30s %5d字/%2d节=%4d字/节 tip:%d warn:%d ex:%d deep:%d ascii:%d svg:%d\n" \
    "$f" "$chars" "$h2" "$avg" "$t" "$w" "$e" "$d" "$a" "$s"
done
```

## Pitfalls: Multi-Module Guide

### f-string curly braces
When generating HTML with Python f-strings, `{` and `}` in code examples must be escaped as `{{` and `}}`. Common breakage: JSON examples, dict comprehensions.

### Duplicate 小结 sections
When patching content before a 小结 section, verify the patch didn't create two 小结 headings. Use `grep -n '小结' file.html` to check.

### Cross-references between non-adjacent modules
Modules should link to RELATED modules, not just prev/next. After generating all modules, add cross-reference tip boxes.

### Content accuracy for fast-moving fields
For Agent/LLM content, ALWAYS search for latest papers and frameworks before writing. Use `ddgs text -k "topic 2025 2026"` for research.
