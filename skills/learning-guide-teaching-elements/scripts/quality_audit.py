#!/usr/bin/env python3
"""质量审计脚本 - 检查教学元素的唯一性、通用模板、缺失元素"""
import os, re, sys, json
from collections import Counter

GENERIC_PHRASES = ['LLM推理就像去餐厅吃饭', '本节概念是理解现代LLM', '学习LLM就像学开车',
                   '不要认为这只是理论', '从更深层次来看']

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    except: return None
    
    result = {'file': filepath, 'h2_count': len(re.findall(r'<h2', content)), 'issues': []}
    
    for cls, name in [('tip', '通俗类比'), ('warn', '常见误区'), ('deep', '深入探讨')]:
        pattern = rf'class="{cls}"[^>]*>.*?(?:通俗类比|常见误区|深入探讨)[：:]?(.*?)</div>'
        texts = [re.sub(r'<[^>]*>', '', m).strip()[:80] for m in re.findall(pattern, content, re.DOTALL)]
        if not texts:
            result['issues'].append(f'缺少{name}'); continue
        n, u = len(texts), len(set(texts))
        rate = (n - u) / max(n, 1) * 100
        if rate > 20:
            result['issues'].append(f'{name}重复率{rate:.0f}%({n}个仅{u}个不同)')
        has_gen = any(any(p in t for p in GENERIC_PHRASES) for t in texts)
        if has_gen:
            result['issues'].append(f'{name}含通用模板')
    
    return result

def scan_dirs(base_dirs):
    results = []
    for d in base_dirs:
        for root, _, files in os.walk(d):
            for f in sorted(files):
                if f.endswith('.html'):
                    r = check_file(os.path.join(root, f))
                    if r: results.append(r)
    return results

if __name__ == '__main__':
    base = '/mnt/d/学习/AI-LLM技术/'
    dirs = [os.path.join(base, d) for d in ['05-推理优化', '09-厂商与前沿', '02-模型架构',
        '06-硬件生态', '12-AI基础设施', 'NVIDIA集合通信', '昇腾超节点集合通信', '经典优化方法', '10-工具与项目']]
    results = scan_dirs([d for d in dirs if os.path.isdir(d)])
    total = len(results)
    perfect = sum(1 for r in results if not r['issues'])
    has_issues = [r for r in results if r['issues']]
    issue_types = Counter()
    for r in has_issues:
        for i in r['issues']:
            if '重复率' in i: issue_types['内容重复'] += 1
            elif '通用模板' in i: issue_types['通用模板'] += 1
            elif '缺少' in i: issue_types['缺失元素'] += 1
    print(f"\n{'='*50}\n  质量审计报告\n{'='*50}")
    print(f"总文件: {total} | 完美: {perfect} ({perfect*100//total}%) | 问题: {len(has_issues)}")
    for t, c in issue_types.most_common(): print(f"  {t}: {c}")
    if has_issues:
        has_issues.sort(key=lambda r: len(r['issues']), reverse=True)
        print(f"\n前5个问题文件:")
        for r in has_issues[:5]:
            short = r['file'].replace(base, '')
            print(f"  ❌ {short}: {'; '.join(r['issues'][:2])}")
    with open('/tmp/quality_audit.json', 'w') as f:
        json.dump({'total': total, 'perfect': perfect, 'issues': len(has_issues),
            'problem_files': [{'file': r['file'].replace(base, ''), 'issues': r['issues']} for r in has_issues]}, f, ensure_ascii=False, indent=2)
