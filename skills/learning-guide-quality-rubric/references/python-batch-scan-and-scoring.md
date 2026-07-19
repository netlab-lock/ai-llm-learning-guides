# Python批量扫描脚本（从2026-06实战中提取）

## 完整的五维度评分+文件清单生成脚本

```python
import os, re, json
from hermes_tools import terminal
from collections import defaultdict

base = "/mnt/d/学习/AI-LLM技术/"

# Step 1: 获取所有HTML文件
result = terminal("find '" + base + "' -name '*.html' ! -name 'index.html' -type f")
all_files = [f.strip() for f in result['output'].strip().split('\n') if f.strip()]

# Step 2: Python直接读取评分（不要用shell grep！）
records = []
for fp in all_files:
    try:
        with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        text = re.sub(r'<[^>]*>', '', content)
        chars = len(re.sub(r'\s+', '', text))
        h2 = len(re.findall(r'<h2', content))
        h3 = len(re.findall(r'<h3', content))
        tables = len(re.findall(r'<table', content))
        pre = len(re.findall(r'<pre', content))
        # 匹配所有CSS变体: class="tip", class="box tip", class="co-tip", class="co co-tip"
        tips = len(re.findall(r'class="[^"]*tip', content))
        warns = len(re.findall(r'class="[^"]*warn', content))
        deeps = len(re.findall(r'class="[^"]*deep', content)) + len(re.findall(r'class="[^"]*info', content))
        ascii_c = len(re.findall(r'class="[^"]*ascii', content))
        svg = len(re.findall(r'<svg', content))

        # 维度1: 内容密度 (100)
        s1 = 0
        if chars >= 8000: s1 += 25
        elif chars >= 4000: s1 += 20
        elif chars >= 2000: s1 += 10
        if h2 >= 5: s1 += 15
        elif h2 >= 3: s1 += 10
        if h3 >= 10: s1 += 10
        elif h3 >= 5: s1 += 5
        if tables >= 3: s1 += 15
        elif tables >= 1: s1 += 10
        if pre >= 3: s1 += 15
        elif pre >= 1: s1 += 10
        if (tips+warns+deeps) >= 5: s1 += 20
        elif (tips+warns+deeps) >= 1: s1 += 10

        # 维度2: 教学设计 (100)
        s2 = 0
        if tips >= 3: s2 += 15
        elif tips >= 1: s2 += 8
        if warns >= 2: s2 += 10
        elif warns >= 1: s2 += 5
        if deeps >= 2: s2 += 15
        elif deeps >= 1: s2 += 8
        viz = ascii_c + svg
        if viz >= 3: s2 += 15
        elif viz >= 1: s2 += 8
        if tables >= 2: s2 += 10
        elif tables >= 1: s2 += 5
        s2 += 30

        # 维度3: 结构完整性 (100) - 全部满分
        s3 = 100

        # 维度4: 准确性 (100) - 固定75（需人工验证）
        s4 = 75

        # 维度5: 可读性 (100) - 暗色主题+viewport
        s5 = 85

        total = s1 + s2 + s3 + s4 + s5
        if total >= 450: grade = 'S'
        elif total >= 380: grade = 'A'
        elif total >= 300: grade = 'B'
        else: grade = 'C'

        # 可提升项
        boosts = []
        potential = 0
        if chars < 8000: boosts.append('chars'); potential += 5
        if tables < 3: boosts.append('tables'); potential += 5
        if tips < 3: boosts.append('tips'); potential += 7
        if warns < 2: boosts.append('warns'); potential += 5
        if deeps < 2: boosts.append('deeps'); potential += 7
        if viz < 3: boosts.append('viz'); potential += 7

        records.append({
            'file': fp.replace(base, ''),
            'total': total, 'grade': grade,
            'gap': max(0, 450 - total),
            'potential': potential, 'boosts': boosts,
            's_target': total + potential >= 450,
            'chars': chars, 'h2': h2, 'tables': tables,
            'tips': tips, 'warns': warns, 'deeps': deeps,
            'viz': viz,
        })
    except:
        pass

# Step 3: 输出统计
from collections import Counter
grade_counts = Counter(r['grade'] for r in records)
for g in ['S', 'A', 'B', 'C']:
    print(f"  {g}级: {grade_counts.get(g, 0)}")

# Step 4: 保存为JSON（供多窗口分配使用）
with open('/tmp/scores.json', 'w') as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
```

## 内容质量检测（区分结构性完成 vs 内容质量）

```python
def check_content_quality(filepath):
    """检查文件的教学元素是否有重复/通用模板"""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # 提取所有tip内容
    tip_texts = re.findall(r'通俗类比[：:](.*?)</div>', content, re.DOTALL)
    if not tip_texts:
        return {'status': 'no_tips'}
    
    unique_tips = set(re.sub(r'<[^>]*>', '', t).strip()[:80] for t in tip_texts)
    repeat_rate = 1 - len(unique_tips) / max(len(tip_texts), 1)
    
    # 检测通用模板
    generic_phrases = [
        'LLM推理就像去餐厅吃饭', '本节概念是理解现代LLM',
        '学习LLM就像学开车', '不要认为这只是理论', '从更深层次来看'
    ]
    has_generic = any(any(p in t for p in generic_phrases) for t in tip_texts)
    
    return {
        'status': 'fail' if (repeat_rate > 0.2 or has_generic) else 'pass',
        'repeat_rate': repeat_rate,
        'has_generic': has_generic,
        'unique': len(unique_tips),
        'total': len(tip_texts),
    }
```

## 多窗口分配脚本

```python
# 将665个文件按目录平衡分配到4个窗口
from collections import defaultdict

by_dir = defaultdict(list)
for r in targets:
    parts = r['file'].split('/')
    d = '/'.join(parts[:2]) if len(parts) > 1 else parts[0]
    by_dir[d].append(r)

dirs_sorted = sorted(by_dir.keys(), key=lambda x: -len(by_dir[x]))
groups = [[], [], [], []]
group_sizes = [0, 0, 0, 0]

for d in dirs_sorted:
    min_idx = group_sizes.index(min(group_sizes))
    groups[min_idx].extend(by_dir[d])
    group_sizes[min_idx] += len(by_dir[d])

# 每个窗口保存为独立JSON
for i, g in enumerate(groups):
    with open(f'/tmp/group_{i}.json', 'w') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
```
