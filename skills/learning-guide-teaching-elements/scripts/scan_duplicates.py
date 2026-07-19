#!/usr/bin/env python3
"""扫描HTML文件中tip/warn/deep内容重复率，找出问题文件"""
import os, re, sys, json
from collections import defaultdict, Counter

def extract_teaching_texts(html, class_name):
    """提取某类教学元素的文本内容（前100字符用于比较）"""
    patterns = {
        'tip': r'class="tip"[^>]*>.*?通俗类比[：:]?(.*?)</div>',
        'warn': r'class="warn"[^>]*>.*?常见误区[：:]?(.*?)</div>',
        'deep': r'class="deep"[^>]*>.*?深入探讨[：:]?(.*?)</div>',
    }
    matches = re.findall(patterns.get(class_name, patterns['tip']), html, re.DOTALL)
    return [re.sub(r'<[^>]*>', '', m).strip()[:100] for m in matches]

def calc_repeat_rate(texts):
    if len(texts) <= 1: return 0.0
    return 1 - len(set(texts)) / len(texts)

def check_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f: content = f.read()
    except: return None
    
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', content, re.DOTALL)
    if len(h2s) <= 1: return None
    
    result = {'file': filepath, 'h2_count': len(h2s), 'issues': []}
    for cls in ['tip', 'warn', 'deep']:
        texts = extract_teaching_texts(content, cls)
        if not texts: continue
        rate = calc_repeat_rate(texts)
        result[f'{cls}_count'] = len(texts)
        result[f'{cls}_unique'] = len(set(texts))
        result[f'{cls}_rate'] = rate
        if rate > 0.5:
            result['issues'].append(f'{cls}:重复率{rate:.0%}({len(texts)}个仅{len(set(texts))}个不同)')
    
    return result if result['issues'] else None

def scan_directory(dir_path):
    problems = []
    for root, dirs, files in os.walk(dir_path):
        for f in sorted(files):
            if not f.endswith('.html'): continue
            r = check_file(os.path.join(root, f))
            if r: problems.append(r)
    return problems

if __name__ == '__main__':
    base = '/mnt/d/学习/AI-LLM技术/'
    dirs = sys.argv[1:] if len(sys.argv) > 1 else [
        '05-推理优化/推理框架', '09-厂商与前沿/国产LLM系列',
        '09-厂商与前沿/国际LLM-Anthropic', '09-厂商与前沿/国际LLM-Google',
        '09-厂商与前沿/国际LLM-Meta', '09-厂商与前沿/国际LLM-Mistral',
        '09-厂商与前沿/国际LLM-OpenAI', '09-厂商与前沿/DeepSeek',
        '经典优化方法', 'NVIDIA集合通信', '昇腾超节点集合通信',
        '12-AI基础设施', '06-硬件生态', '10-工具与项目',
    ]
    all_problems = []
    for d in dirs:
        full = os.path.join(base, d)
        if os.path.isdir(full):
            all_problems.extend(scan_directory(full))
    
    all_problems.sort(key=lambda x: len(x['issues']), reverse=True)
    print(f"扫描完成: {len(all_problems)} 个文件存在重复问题")
    
    by_dir = defaultdict(list)
    for p in all_problems:
        by_dir[os.path.dirname(p['file'].replace(base, ''))].append(p)
    
    for d in sorted(by_dir.keys()):
        files = by_dir[d]
        print(f"\n📁 {d}/ ({len(files)}个问题文件)")
        for p in files[:3]:
            fname = os.path.basename(p['file'])
            print(f"  ❌ {fname}: h2={p['h2_count']} | {', '.join(p['issues'])}")
        if len(files) > 3: print(f"  ... 还有{len(files)-3}个文件")
    
    with open('/tmp/problem_files.json', 'w') as f:
        json.dump([p['file'] for p in all_problems], f, ensure_ascii=False)
    print(f"\n问题文件列表已保存到 /tmp/problem_files.json ({len(all_problems)}个)")
