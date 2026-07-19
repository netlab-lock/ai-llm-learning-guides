#!/usr/bin/env python3
"""
扫描HTML文件中tip/warn/deep内容重复率，找出问题文件。
用法: python3 scan_duplicates.py [目录路径]
输出: 每个问题文件的重复率详情 + 汇总统计
"""
import os
import re
import sys
import json
from collections import defaultdict

def extract_teaching_texts(html, class_name):
    """提取某类教学元素的文本内容（前100字符用于比较）"""
    labels = {'tip': '通俗类比', 'warn': '常见误区', 'deep': '深入探讨'}
    label = labels.get(class_name, class_name)
    pattern = rf'class="{class_name}"[^>]*>.*?{label}[：:]?(.*?)</div>'
    matches = re.findall(pattern, html, re.DOTALL)
    cleaned = []
    for m in matches:
        text = re.sub(r'<[^>]*>', '', m).strip()
        text = re.sub(r'\s+', ' ', text)[:100]
        cleaned.append(text)
    return cleaned

def calc_repeat_rate(texts):
    if len(texts) <= 1:
        return 0.0
    return 1 - len(set(texts)) / len(texts)

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None

    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    if len(h2s) <= 1:
        return None

    result = {'file': filepath, 'h2_count': len(h2s), 'issues': []}

    for cls in ['tip', 'warn', 'deep']:
        texts = extract_teaching_texts(content, cls)
        if not texts:
            continue
        rate = calc_repeat_rate(texts)
        result[f'{cls}_count'] = len(texts)
        result[f'{cls}_unique'] = len(set(texts))
        result[f'{cls}_rate'] = rate
        if rate > 0.5:
            result['issues'].append(
                f'{cls}:重复率{rate:.0%}({len(texts)}个仅{len(set(texts))}个不同)')

    return result if result['issues'] else None

def scan_directory(dir_path):
    problems = []
    for root, dirs, files in os.walk(dir_path):
        for f in sorted(files):
            if not f.endswith('.html'):
                continue
            r = check_file(os.path.join(root, f))
            if r:
                problems.append(r)
    return problems

if __name__ == '__main__':
    base = sys.argv[1] if len(sys.argv) > 1 else '/mnt/d/学习/AI-LLM技术/'
    all_problems = scan_directory(base)
    all_problems.sort(key=lambda x: len(x['issues']), reverse=True)

    print(f"扫描完成: {len(all_problems)} 个文件存在重复问题\n")

    by_dir = defaultdict(list)
    for p in all_problems:
        short = p['file'].replace(base, '')
        by_dir[os.path.dirname(short)].append(p)

    for d in sorted(by_dir.keys()):
        files = by_dir[d]
        print(f"📁 {d}/ ({len(files)}个问题文件)")
        for p in files[:3]:
            fname = os.path.basename(p['file'])
            issues = ', '.join(p['issues'])
            print(f"  ❌ {fname}: h2={p['h2_count']} | {issues}")
        if len(files) > 3:
            print(f"  ... 还有{len(files)-3}个文件")
        print()

    with open('/tmp/problem_files.json', 'w') as f:
        json.dump([p['file'] for p in all_problems], f, ensure_ascii=False)
    print(f"问题文件列表已保存到 /tmp/problem_files.json ({len(all_problems)}个)")
