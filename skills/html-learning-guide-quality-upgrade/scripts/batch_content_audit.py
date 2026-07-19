#!/usr/bin/env python3
"""
批量内容质量审计脚本 — 一次性检查217个文件的全部质量维度。
用法: python3 batch_content_audit.py /path/to/AI-LLM技术

输出: 每个文件的chars/tips/warns/deeps/tables/codes/viz + 问题标记。
"""
import re, os, sys

BASE = sys.argv[1] if len(sys.argv) > 1 else "."
DIRS = ["01-基础理论", "03-训练技术", "07-应用技术"]

GENERIC_PATTERNS = [
    "建议先从最小规模的端到端demo开始",
    "掌握这个主题的高效路径：先理解原理，再动手实践",
    "关于「",
    "实用建议：在实际应用中，建议先从最小规模",
]

all_htmls = []
for d in DIRS:
    for root, _, files in os.walk(os.path.join(BASE, d)):
        for f in sorted(files):
            if f.endswith('.html') and f != 'index.html':
                all_htmls.append(os.path.join(root, f))

total_issues = 0
for fp in all_htmls:
    try:
        html = open(fp, encoding='utf-8').read()
    except:
        print(f"  READ_FAIL | {os.path.relpath(fp, BASE)}")
        total_issues += 1
        continue

    rel = os.path.relpath(fp, BASE)
    text = re.sub(r'<style.*?</style>', '', html, flags=re.DOTALL)
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)
    chars = len(re.sub(r'\s+', '', text))

    is_a = '.box.tip' in html or 'class="box tip"' in html
    if is_a:
        tips = len(re.findall(r'class="box tip"', html))
        warns = len(re.findall(r'class="box warn"', html))
        deeps = len(re.findall(r'class="box deep"', html))
    else:
        tips = len(re.findall(r'class="tip"', html))
        warns = len(re.findall(r'class="warn"', html))
        deeps = len(re.findall(r'class="deep"', html))

    tables = len(re.findall(r'<table', html))
    codes = len(re.findall(r'<pre', html))
    viz = len(re.findall(r'class="ascii"', html)) + len(re.findall(r'<svg', html))

    has_template = any(p in html for p in GENERIC_PATTERNS)

    paras = re.findall(r'<p>(.*?)</p>', html, re.DOTALL)
    clean_paras = [re.sub(r'<[^>]+>', '', p).strip() for p in paras if len(re.sub(r'<[^>]+>', '', p).strip()) > 50]
    seen = set()
    has_dupes = any(p in seen or seen.add(p) for p in clean_paras)

    issues = []
    if chars < 6000: issues.append(f"c{chars}")
    if tips < 3: issues.append(f"t{tips}")
    if warns < 2: issues.append(f"w{warns}")
    if deeps < 2: issues.append(f"d{deeps}")
    if tables < 2: issues.append(f"tbl{tables}")
    if codes < 1: issues.append("no_code")
    if viz < 1: issues.append("no_viz")
    if has_template: issues.append("TMPL")
    if has_dupes: issues.append("DUP")

    fname = rel.split('/')[-1][:35]
    status = "OK" if not issues else "ISSUE:" + ",".join(issues)
    if issues:
        total_issues += 1
    print(f"  {status} c={chars} t={tips}w={warns}d={deeps} tbl={tables} code={codes} viz={viz} | {fname}")

print(f"\n总计: {len(all_htmls)}文件, {total_issues}个有问题")
