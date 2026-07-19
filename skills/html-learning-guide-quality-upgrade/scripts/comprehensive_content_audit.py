"""
Comprehensive content quality audit for HTML learning guides.
Checks: empty h2 sections, missing exercises/learning paths, duplicate h3,
        template content, warn/deep uniqueness, and score verification.

Usage: python3 comprehensive_content_audit.py <base_dir>
"""
import re, os, glob, sys
from collections import Counter

base = sys.argv[1] if len(sys.argv) > 1 else "."

def get_score(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    b = re.sub(r'<style[^>]*>.*?</style>', '', c, flags=re.DOTALL)
    b = re.sub(r'<script[^>]*>.*?</script>', '', b, flags=re.DOTALL)
    b = re.sub(r'<[^>]+>', ' ', b)
    wc = len(re.sub(r'\s+', ' ', b).strip())
    h2 = len(re.findall(r'<h2[^>]*>', c)); h3 = len(re.findall(r'<h3[^>]*>', c))
    tbl = len(re.findall(r'<table[^>]*>', c)); code = len(re.findall(r'<pre[^>]*>|<code[^>]*>', c))
    tips = len(re.findall(r'class="tip"', c)); warns = len(re.findall(r'class="warn"', c))
    deeps = len(re.findall(r'class="deep"', c)); asciis = len(re.findall(r'class="ascii"', c))
    dk = len(re.findall(r'公式|推导|证明|原理|工作机制|数学本质|为什么', c))
    cr = len(re.findall(r'href="[^"]*"', c))
    ex = 1 if re.search(r'思考与练习|思考题|练习题|习题|exercises', c, re.IGNORECASE) else 0
    lp = 1 if re.search(r'学习路径|学习路线|学习建议', c) else 0
    d1 = min(25, wc/8000*25)+min(15, h2/5*15)+min(10, h3/10*10)+min(15, tbl/3*15)+min(15, code/3*15)+min(20, dk/5*20)
    d2 = min(15, tips/3*15)+min(10, warns/2*10)+min(15, deeps/2*15)+min(15, asciis/3*15)+min(10, tbl/2*10)+(10 if ex else 0)+(10 if cr>3 else (5 if cr>0 else 0))+(5 if lp else 0)
    return round(d1+d2+260)

def audit_content(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    issues = []
    
    # 1. Empty h2 sections
    h2_positions = [(m.start(), m.group(1)) for m in re.finditer(r'<h2[^>]*>(.*?)</h2>', c)]
    for pos, title in h2_positions:
        ns = re.search(r'<h[23][^>]*>', c[pos+10:])
        between = c[pos+10:pos+10+ns.start()] if ns else c[pos+10:]
        text = re.sub(r'<[^>]+>', '', between).strip()
        if len(text) < 30:
            issues.append(f"empty_h2: {title[:30]}")
    
    # 2. Missing exercises (broad regex)
    if not re.search(r'思考与练习|思考题|练习题|习题|exercises', c, re.IGNORECASE):
        issues.append("missing_exercises")
    
    # 3. Missing learning path (broad regex)
    if not re.search(r'学习路径|学习路线|学习建议', c):
        issues.append("missing_learning_path")
    
    # 4. Duplicate h3 titles
    h3t = [re.sub(r'<[^>]+>', '', m.group(1)) for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', c)]
    for t, cnt in Counter(h3t).items():
        if cnt > 1 and len(t) > 3:
            issues.append(f"duplicate_h3({cnt}): {t[:20]}")
    
    # 5. Template h3 titles
    for m in re.finditer(r'<h3[^>]*>(.*?)</h3>', c):
        title = re.sub(r'<[^>]+>', '', m.group(1))
        if '核心组件与工作原理' in title or '训练流程与优化策略' in title:
            issues.append(f"template_h3: {title[:20]}")
    
    # 6. Short tips/warns/deeps
    for m in re.finditer(r'<div class="tip">.*?通俗类比[：:](.*?)</div>', c, re.DOTALL):
        if len(m.group(1).strip()) < 30:
            issues.append("short_tip")
    for m in re.finditer(r'<div class="warn">.*?常见误区[：:](.*?)</div>', c, re.DOTALL):
        if len(m.group(1).strip()) < 30:
            issues.append("short_warn")
    for m in re.finditer(r'<div class="deep">.*?深入探讨[：:](.*?)</div>', c, re.DOTALL):
        if len(m.group(1).strip()) < 30:
            issues.append("short_deep")
    
    return issues

# Main
files = sorted(glob.glob(os.path.join(base, "**/*.html"), recursive=True))
non_idx = [f for f in files if not f.endswith('index.html')]

print(f"Auditing {len(non_idx)} files...")

# Score distribution
scores = Counter()
clean = 0
issue_files = []
issue_types = Counter()
warn_texts = []
deep_texts = []

for fp in non_idx:
    score = get_score(fp)
    grade = 'S' if score >= 450 else ('A+' if score >= 440 else 'A')
    scores[grade] += 1
    
    issues = audit_content(fp)
    if not issues:
        clean += 1
    else:
        rel = fp.replace(base+'/', '')
        issue_files.append((rel, score, issues))
        for iss in issues:
            issue_types[iss.split(':')[0]] += 1

# Collect warn/deep for uniqueness check
for fp in non_idx:
    with open(fp, 'r', encoding='utf-8') as f:
        c = f.read()
    for m in re.finditer(r'<div class="warn"><strong>常见误区：</strong>(.*?)</div>', c, re.DOTALL):
        warn_texts.append(m.group(1).strip()[:100])
    for m in re.finditer(r'<div class="deep"><strong>深入探讨：</strong>(.*?)</div>', c, re.DOTALL):
        deep_texts.append(m.group(1).strip()[:100])

# Report
print(f"\n{'='*55}")
print(f"  Content Quality Audit Report")
print(f"{'='*55}")
print(f"  Files: {len(non_idx)}")
print(f"  Score: S={scores['S']} A+={scores['A+']} A={scores['A']} S+A+={scores['S']+scores['A+']}/{len(non_idx)}")
print(f"  Clean: {clean}/{len(non_idx)} ({clean/len(non_idx)*100:.0f}%)")
print(f"  Issues: {len(non_idx)-clean} files, {sum(issue_types.values())} total issues")
print(f"  Warn unique: {len(set(warn_texts))}/{len(warn_texts)} ({len(set(warn_texts))/max(1,len(warn_texts))*100:.0f}%)")
print(f"  Deep unique: {len(set(deep_texts))}/{len(deep_texts)} ({len(set(deep_texts))/max(1,len(deep_texts))*100:.0f}%)")

if issue_types:
    print(f"\n  Issue types:")
    for itype, cnt in issue_types.most_common():
        print(f"    {itype}: {cnt}")

if issue_files:
    print(f"\n  Problem files (first 20):")
    for rel, score, issues in issue_files[:20]:
        print(f"    [{score}] {rel[:50]} | {', '.join(issues[:3])}")
