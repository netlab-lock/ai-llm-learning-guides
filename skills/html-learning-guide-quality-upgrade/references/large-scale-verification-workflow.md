# 大规模文件验证工作流

## 背景
当完成200+文件的质量提升后，需要逐文件验证所有文件都满足要求。

## 验证脚本（单次运行，检查全部文件）

```python
import re, os, subprocess

BASE = '.'
with open('窗口2文件清单.txt', 'r', encoding='utf-8') as f:
    content = f.read()

entries = []
for line in content.split('\n'):
    m = re.match(r'\s*(\d+)分\s*\[([^\]]+)\]\s*补:([^|]*)\|\s*(.+)', line)
    if m:
        entries.append({'orig': int(m.group(1)), 'path': m.group(4).strip()})

passed = failed = 0
for e in entries:
    fp = os.path.join(BASE, e['path'])
    try:
        r = subprocess.run(['python3', 'analyze_html.py', fp], capture_output=True, text=True, timeout=10)
        score_m = re.search(r'Score: (\d+)', r.stdout)
        score = int(score_m.group(1)) if score_m else 0
    except:
        score = 0
    if score >= 450: passed += 1
    else: failed += 1
    fname = e['path'].split('/')[-1]
    print(str(e['orig']).rjust(4) + ' -> ' + str(score).rjust(4) + ' ' + ('OK' if score >= 450 else 'FAIL').rjust(5) + ' | ' + fname)

print(f'\nPassed: {passed}/{len(entries)}  Failed: {failed}/{len(entries)}')
```

## 关键注意事项
1. **先验证文件清单完整性** — 清单可能被截断或损坏，先对比磁盘实际文件数
2. **用subprocess运行analyze_html.py** — 不要在Python中内联评分逻辑（容易出错）
3. **单次运行** — 验证脚本应该一次跑完全部文件，不要分批
4. **输出格式** — 显示原始分数→当前分数→OK/FAIL，便于对比
5. **不要反复验证** — 验证一次后声明完成，不要因循环目标重复执行
