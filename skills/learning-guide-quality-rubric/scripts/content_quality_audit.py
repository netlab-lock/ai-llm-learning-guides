#!/usr/bin/env python3
"""
Content quality audit for HTML learning guides.
Checks for generic templates, short tips, duplicate content, and broken HTML.

Usage: python3 content_quality_audit.py <base_dir> [--verbose]

Returns exit code 0 if all files pass, 1 otherwise.
"""
import re, os, sys
from collections import Counter

# Known generic phrases (update as new patterns are discovered)
GENERIC_PHRASES = [
    'LLM推理就像去餐厅吃饭', '本节概念是理解现代LLM', '学习LLM就像学开车',
    '不要认为这只是理论', '从更深层次来看', '关注点分离的原则',
    '掌握这个主题的高效路径', '类比搜索引擎排序', '选择了最灵活的实现路径',
    '核心挑战在于扩展性', '由三个关键组件构成', '采用了分层抽象的设计哲学',
    '建议先从最小规模的端到端demo', '应用场景广泛，从模型训练到推理部署',
    '从经济学角度看，推理成本', '很多人以为推理比训练简单',
    '深入原理与数学推导', '工程实践与常见问题',
    '就像一套精密的工厂流水线', '就像学习一门新语言',
    '很多人只关注理论而忽略实践', '建议先在小规模环境验证方案可行性',
    '通俗类比：通俗类比：',
]

GENERIC_H3_SUFFIXES = [
    '的核心机制', '的实际应用', '的核心算法与数据结构',
    '的性能瓶颈与优化策略', '在生产环境中的工程实践',
    '的数学原理与复杂度分析', '的常见问题与解决方案',
    '的技术演进与未来方向', '的系统架构与组件交互',
    '的性能度量与基准测试', '的工程部署考量',
    '的未来技术趋势', '的性能调优要点',
]

def audit_file(filepath, verbose=False):
    """Audit a single file. Returns list of issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    issues = []
    
    # 1. Generic phrases
    for phrase in GENERIC_PHRASES:
        if phrase in c:
            issues.append(f"generic_phrase:{phrase[:25]}")
            break
    
    # 2. Generic h3 suffixes
    h3s = re.findall(r'<h3[^>]*>(.*?)</h3>', c, re.DOTALL)
    for h in h3s:
        clean = re.sub(r'<[^>]+>', '', h).strip()
        for suffix in GENERIC_H3_SUFFIXES:
            if suffix in clean:
                issues.append(f"generic_h3:{clean[:25]}")
                break
    
    # 3. Short tips/warns (<50 chars)
    for cls in ['tip', 'warn']:
        blocks = re.findall(f'class="{cls}"[^>]*>(.*?)</div>', c, re.DOTALL)
        for b in blocks:
            if len(re.sub(r'<[^>]+>', '', b).strip()) < 50:
                issues.append(f"short_{cls}")
                break
    
    # 4. Duplicate tips within file
    tips = re.findall(r'class="tip"[^>]*>(.*?)</div>', c, re.DOTALL)
    tip_texts = [re.sub(r'<[^>]+>', '', t).strip()[:80] for t in tips]
    for text, count in Counter(tip_texts).items():
        if count > 1 and len(text) > 20:
            issues.append("dup_tip")
            break
    
    # 5. Broken HTML
    if '</p<' in c:
        issues.append("broken_html")
    
    # 6. h2 title leakage
    if re.search(r'学习[一二三四五六七八九十\d]+[、.]', c):
        issues.append("h2_leakage")
    
    # 7. HTML integrity
    if '</html>' not in c:
        issues.append("no_closing_html")
    
    return issues

def main():
    base = sys.argv[1] if len(sys.argv) > 1 else "."
    verbose = '--verbose' in sys.argv
    
    total = 0
    passed = 0
    issue_counts = Counter()
    
    for root, dirs, fnames in os.walk(base):
        for fname in sorted(fnames):
            if not fname.endswith('.html') or fname.startswith('index'):
                continue
            total += 1
            path = os.path.join(root, fname)
            rel = os.path.relpath(path, base)
            
            issues = audit_file(path, verbose)
            
            if issues:
                for issue in issues:
                    issue_counts[issue.split(':')[0]] += 1
                if verbose:
                    print(f"  FAIL: {rel}: {', '.join(issues)}")
            else:
                passed += 1
    
    print(f"\nContent Quality Audit: {base}")
    print(f"  Total: {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {total - passed}")
    
    if issue_counts:
        print(f"\n  Issue breakdown:")
        for issue, count in issue_counts.most_common():
            print(f"    {issue}: {count}")
    
    sys.exit(0 if passed == total else 1)

if __name__ == '__main__':
    main()
