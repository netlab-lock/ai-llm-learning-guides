#!/usr/bin/env python3
"""
Comprehensive content quality audit for HTML learning guides.
Checks both structural metrics AND content quality.
Usage: python3 audit_content_quality.py <base_dir>
"""
import re, os, sys, json
from collections import Counter

BASE = sys.argv[1] if len(sys.argv) > 1 else "/mnt/d/学习/AI-LLM技术"
DK = ['公式','推导','证明','原理','工作机制','数学本质','为什么','底层','本质']

GENERIC_H3_SUFFIXES = [
    '的核心机制', '的实际应用', '的核心算法与数据结构',
    '的性能瓶颈与优化策略', '在生产环境中的工程实践',
    '的数学原理与复杂度分析', '的常见问题与解决方案',
    '的技术演进与未来方向', '的系统架构与组件交互',
    '的性能度量与基准测试', '的工程部署考量',
    '的未来技术趋势', '的性能调优要点',
]

GENERIC_TEMPLATES = ['深入原理与数学推导','工程实践与常见问题','应用场景广泛']
GENERIC_TIPS = ['LLM推理就像去餐厅吃饭','很多人以为推理比训练简单','从经济学角度看，推理成本']

def score_file(content):
    cc = len(re.sub(r'<[^>]+>', ' ', re.sub(r'\s+', ' ', content)).strip())
    h2 = len(re.findall(r'<h2[^>]*>', content))
    h3 = len(re.findall(r'<h3[^>]*>', content))
    tbl = len(re.findall(r'<table[^>]*>', content))
    pre = len(re.findall(r'<pre[^>]*>', content))
    dk = sum(len(re.findall(k, content)) for k in DK)
    tip = len(re.findall(r'class="tip"', content))
    warn = len(re.findall(r'class="warn"', content))
    deep = len(re.findall(r'class="deep"', content))
    asc = len(re.findall(r'class="ascii"', content))
    ex = len(re.findall(r'class="exercise"', content)) + len(re.findall(r'思考题', content))
    fw = len(re.findall(r'向前串联|后续内容|进阶学习', content))
    cr = len(re.findall(r'href="[^"]*"', content))
    d1 = (25 if cc>=8000 else 20 if cc>=6000 else 15 if cc>=4000 else 10) + min(15,h2*3) + min(10,h3) + min(15,tbl*5) + min(15,pre*5) + min(20,dk*2)
    d2 = min(15,tip*5) + min(10,warn*5) + min(15,deep*5) + min(15,asc*5) + min(10,tbl*5) + (10 if ex>0 else 0) + (10 if fw>0 else 0) + (min(10,cr) if cr>0 else 0) + (5 if '学习路径' in content or '前置知识' in content else 0)
    return d1 + d2 + 260

def audit_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    issues = []
    score = score_file(content)
    if score < 450: issues.append(f"SCORE:{score}")
    if '</html>' not in content: issues.append("NO_HTML")
    if '</body>' not in content: issues.append("NO_BODY")
    ex = len(re.findall(r'class="exercise"', content)) + len(re.findall(r'思考题', content))
    fw = len(re.findall(r'向前串联|后续内容|进阶学习', content))
    if ex == 0: issues.append("NO_EXERCISE")
    if fw == 0: issues.append("NO_FORWARD")
    if '学习路径' not in content and '前置知识' not in content: issues.append("NO_PATH")
    if '返回' not in content and 'index.html' not in content: issues.append("NO_NAV")
    for m in GENERIC_TEMPLATES:
        if m in content: issues.append(f"TEMPLATE:{m[:15]}")
    for m in GENERIC_TIPS:
        if m in content: issues.append(f"GENERIC_TIP:{m[:15]}")
    for cls in ['tip','warn']:
        for b in re.findall(f'class="{cls}"[^>]*>(.*?)</div>', content, re.DOTALL):
            if len(re.sub(r'<[^>]+>', '', b).strip()) < 50: issues.append(f"SHORT_{cls}"); break
    h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', content, re.DOTALL)
    for h in h3s:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        for s in GENERIC_H3_SUFFIXES:
            if s in clean: issues.append(f"GENERIC_H3:{s}"); break
    if '</p<' in content: issues.append("BROKEN_HTML")
    tips = re.findall(r'class="tip"[^>]*>(.*?)</div>', content, re.DOTALL)
    for text, count in Counter(re.sub(r'<[^>]+>', '', t).strip()[:80] for t in tips).items():
        if count > 1 and len(text) > 20: issues.append("DUP_TIP"); break
    # Dead link check
    file_dir = os.path.dirname(filepath)
    for link in re.findall(r'href="([^"]*)"', content):
        if link.startswith(('http', '#', 'mailto')):
            continue
        target = os.path.normpath(os.path.join(file_dir, link))
        base = os.path.dirname(filepath)
        # Walk up to find the project root
        while base and not os.path.exists(os.path.join(base, target)):
            parent = os.path.dirname(base)
            if parent == base: break
            base = parent
        if not os.path.exists(os.path.join(os.path.dirname(filepath), target)):
            issues.append(f"DEAD_LINK:{link[:30]}")
            break
    
    return score, issues

def main():
    target_files = []
    for root, dirs, fnames in os.walk(BASE):
        for fname in sorted(fnames):
            if fname.endswith('.html') and not fname.startswith('index'):
                target_files.append(os.path.join(root, fname))
    results = []
    for fp in sorted(target_files):
        try:
            score, issues = audit_file(fp)
            results.append({'file': os.path.relpath(fp, BASE), 'score': score, 'issues': issues})
        except Exception as e:
            results.append({'file': fp, 'score': 0, 'issues': [f"ERROR:{e}"]})
    total = len(results)
    s_count = sum(1 for r in results if r['score'] >= 450 and not r['issues'])
    issue_counts = Counter()
    for r in results:
        for i in r['issues']: issue_counts[i.split(':')[0]] += 1
    print(f"{'='*55}\n  Content Quality Audit — {total} files\n{'='*55}")
    print(f"\n  All checks passed: {s_count}/{total}")
    print(f"\n  Issue breakdown:")
    for issue, count in issue_counts.most_common(): print(f"    {issue}: {count}")
    failing = [r for r in results if r['issues']]
    if failing:
        print(f"\n  Failing files ({len(failing)}):")
        for r in failing[:10]: print(f"    {r['file'][-50:]}: {', '.join(r['issues'][:3])}")

if __name__ == '__main__':
    main()
