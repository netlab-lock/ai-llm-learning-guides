#!/usr/bin/env python3
"""
修复教学元素重复：用LLM API为每个h2节生成独特的tip/warn/deep/ascii/table
用法: python3 fix_duplicates.py <目录或文件> [--dry-run] [--limit N]
"""
import os, re, sys, json, time
import urllib.request, urllib.error

API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions'
MODEL = 'mimo-v2.5-pro'
API_KEY = ''

GENERIC_PHRASES = ['LLM推理就像去餐厅吃饭', '本节概念是理解现代LLM', '学习LLM就像学开车',
                   '不要认为这只是理论', '从更深层次来看']

def load_config():
    global API_KEY
    auth_path = os.path.expanduser('~/.hermes/auth.json')
    try:
        with open(auth_path) as f:
            auth = json.load(f)
        pool = auth.get('credential_pool', {})
        creds = pool.get('xiaomi', [])
        if creds:
            API_KEY = creds[0].get('access_token', '')
    except Exception as e:
        print(f"Warning: {e}", file=sys.stderr)
    if not API_KEY:
        print("ERROR: No API key in auth.json", file=sys.stderr)
        sys.exit(1)

def call_llm(prompt, max_retries=3):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    data = {'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.7, 'max_tokens': 16384}
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(API_URL, data=json.dumps(data).encode(), headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=600) as resp:
                result = json.loads(resp.read().decode())
                content = result['choices'][0]['message'].get('content', '')
                if not content:
                    content = result['choices'][0]['message'].get('reasoning_content', '')
                return content
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(30 * (attempt + 1))
            elif e.code == 500:
                time.sleep(10)
            else:
                if attempt == max_retries - 1: return None
                time.sleep(5)
        except Exception:
            if attempt == max_retries - 1: return None
            time.sleep(5)
    return None

def parse_llm_json(response):
    """Parse JSON from LLM, handling invalid backslash escapes (MiMo specific)"""
    try:
        json_match = re.search(r'\{[\s\S]*"sections"[\s\S]*\}', response)
        if not json_match: return None
        raw = json_match.group(0)
        # Nuclear cleaning: preserve standard escapes, strip all others
        raw = raw.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')
        raw = raw.replace('\\"', '"ESC_QUOTE"')
        raw = raw.replace('\\\\', 'DBL_BSLASH')
        raw = re.sub(r'\\/', '/', raw)
        raw = raw.replace('\\', '')  # Remove ALL remaining backslashes
        raw = raw.replace('"ESC_QUOTE"', '\\"')
        raw = raw.replace('DBL_BSLASH', '\\\\')
        try:
            data = json.loads(raw, strict=False)
        except json.JSONDecodeError:
            # Level 2: regex per-field extraction
            sections_data = []
            for m in re.finditer(r'"index"\s*:\s*(\d+)', raw):
                idx = int(m.group(1)); start = m.start(); chunk = raw[start:start+3000]
                def ext(name, text):
                    pat = re.search(rf'"{name}"\s*:\s*"(.*?)"(?=\s*,\s*"|\s*\}})', text, re.DOTALL)
                    return pat.group(1).strip() if pat else ''
                sections_data.append({'index': idx, 'h2': ext('h2', chunk),
                    'tip': ext('tip', chunk), 'warn': ext('warn', chunk),
                    'deep': ext('deep', chunk), 'ascii': ext('ascii', chunk), 'table': ext('table', chunk)})
            data = {'sections': sections_data} if sections_data else None
        return data.get('sections', []) if data else None
    except Exception as e:
        print(f"  WARNING: {e}", file=sys.stderr); return None

def generate_unique_content(file_path, sections):
    file_name = os.path.basename(file_path)
    dir_name = os.path.basename(os.path.dirname(file_path))
    BATCH_SIZE = 8; all_generated = []
    for bs in range(0, len(sections), BATCH_SIZE):
        batch = sections[bs:bs+BATCH_SIZE]
        sl = [f"[{i+1}] \"{s['h2_text']}\" | {s['context'][:80]}" for i, s in enumerate(batch)]
        prompt = f"""为HTML学习指南的每个h2节生成独特教学内容。文件: {dir_name}/{file_name}
h2节({len(batch)}个):
{chr(10).join(sl)}

每个节生成: tip(生活类比30-60字) warn(特有误区30-60字) deep(数字/公式50-100字) ascii(3-6行图) table(3-4行HTML表格)
JSON输出(字符串中不要用反斜杠): {{"sections":[{{"index":1,"h2":"标题","tip":"...","warn":"...","deep":"...","ascii":"<pre>...</pre>","table":"<tr>...</tr>"}}]}}"""
        resp = call_llm(prompt)
        if not resp: continue
        parsed = parse_llm_json(resp)
        if parsed:
            for s in parsed:
                if 'index' in s: s['index'] += bs
            all_generated.extend(parsed)
    return all_generated if all_generated else None

def extract_h2_sections(html):
    pattern = re.compile(r'<h2[^>]*>(.*?)</h2>', re.IGNORECASE | re.DOTALL)
    sections = []
    for m in pattern.finditer(html):
        text = re.sub(r'<[^>]*>', '', m.group(1)).strip()
        after = html[m.end():m.end()+500]
        after_clean = re.sub(r'<[^>]*>', '', after).strip()[:200]
        sections.append({'h2_text': text, 'context': after_clean, 'end_pos': m.end(), 'full_match': m.group(0)})
    return sections

def patch_file(html, sections, generated):
    if not generated: return html, 0
    gen_map = {g.get('index',0)-1: g for g in generated if 0 <= g.get('index',0)-1 < len(sections)}
    replacements = 0
    for i in range(len(sections)-1, -1, -1):
        if i not in gen_map: continue
        s = sections[i]; g = gen_map[i]
        start = s['end_pos']
        end = sections[i+1]['end_pos'] - len(sections[i+1]['full_match']) if i+1 < len(sections) else min(start+3000, len(html))
        chunk = html[start:end]
        tip = f'<div class="tip"><strong>通俗类比：</strong>{g.get("tip","")}</div>'
        warn = f'<div class="warn"><strong>常见误区：</strong>{g.get("warn","")}</div>'
        deep = f'<div class="deep"><strong>深入探讨：</strong>{g.get("deep","")}</div>'
        ascii_c = g.get("ascii","")
        ascii_h = f'<div class="ascii"><pre>{ascii_c}</pre></div>' if ascii_c else ''
        table_c = g.get("table","")
        table_h = f'<table>{table_c}</table>' if table_c and '<table>' not in table_c else table_c
        new_teaching = f"\n{tip}\n{warn}\n{deep}\n{ascii_h}\n{table_h}\n"
        for cls in ['tip','warn','deep']:
            chunk = re.sub(rf'<div class="{cls}"[^>]*>.*?</div>', '', chunk, flags=re.DOTALL)
        chunk = re.sub(r'<div class="ascii"[^>]*>.*?</div>', '', chunk, flags=re.DOTALL)
        ins = len(chunk) - len(chunk.lstrip())
        chunk = chunk[:ins] + new_teaching + chunk[ins:]
        html = html[:start] + chunk + html[end:]
        replacements += 1
    return html, replacements

def process_file(file_path, dry_run=False):
    try:
        with open(file_path, 'r', encoding='utf-8') as f: content = f.read()
    except Exception as e: return {'status': 'error', 'file': file_path, 'error': str(e)}
    sections = extract_h2_sections(content)
    if len(sections) <= 1: return {'status': 'skip', 'file': file_path, 'reason': 'too few h2'}
    # Check BOTH repeat rate AND generic content
    tips = re.findall(r'class="tip"[^>]*>.*?通俗类比[：:]?(.*?)</div>', content, re.DOTALL)
    if tips:
        tip_texts = [re.sub(r'<[^>]*>', '', t).strip()[:80] for t in tips]
        rate = 1 - len(set(tip_texts)) / max(len(tip_texts), 1)
        has_generic = any(any(p in t for p in GENERIC_PHRASES) for t in tip_texts)
        if rate < 0.2 and not has_generic:
            return {'status': 'skip', 'file': file_path, 'reason': f'already ok ({rate:.0%})'}
    print(f"  Processing: {os.path.basename(file_path)} ({len(sections)} sections)", file=sys.stderr)
    generated = generate_unique_content(file_path, sections)
    if not generated: return {'status': 'error', 'file': file_path, 'error': 'generation failed'}
    new_content, count = patch_file(content, sections, generated)
    if not dry_run and count > 0:
        with open(file_path, 'w', encoding='utf-8') as f: f.write(new_content)
    return {'status': 'fixed', 'file': file_path, 'sections_fixed': count, 'sections_total': len(sections)}

def process_directory(dir_path, dry_run=False, limit=0):
    results = []; count = 0
    for root, dirs, files in os.walk(dir_path):
        for f in sorted(files):
            if not f.endswith('.html'): continue
            fpath = os.path.join(root, f)
            try:
                with open(fpath) as fh: head = fh.read()
                tips = re.findall(r'class="tip"[^>]*>.*?通俗类比[：:]?(.*?)</div>', head, re.DOTALL)
                if len(tips) <= 1: continue
                tip_texts = [re.sub(r'<[^>]*>', '', t).strip()[:80] for t in tips]
                rate = 1 - len(set(tip_texts)) / max(len(tip_texts), 1)
                has_generic = any(any(p in t for p in GENERIC_PHRASES) for t in tip_texts)
                if rate < 0.2 and not has_generic: continue
            except: continue
            r = process_file(fpath, dry_run=dry_run)
            results.append(r)
            if r['status'] == 'fixed': print(f"  ✓ {os.path.basename(fpath)}: {r['sections_fixed']}/{r['sections_total']}", file=sys.stderr)
            elif r['status'] == 'error': print(f"  ✗ {os.path.basename(fpath)}: {r.get('error','')}", file=sys.stderr)
            count += 1
            if limit and count >= limit: break
            time.sleep(5)
        if limit and count >= limit: break
    fixed = sum(1 for r in results if r['status']=='fixed')
    return results, fixed, sum(1 for r in results if r['status']=='error'), sum(1 for r in results if r['status']=='skip')

if __name__ == '__main__':
    load_config()
    path = sys.argv[1]; dry_run = '--dry-run' in sys.argv
    limit = int(sys.argv[sys.argv.index('--limit')+1]) if '--limit' in sys.argv else 0
    if os.path.isfile(path):
        print(json.dumps(process_file(path, dry_run), ensure_ascii=False, indent=2))
    elif os.path.isdir(path):
        results, fixed, errors, skipped = process_directory(path, dry_run, limit)
        print(f"\n=== Done: {len(results)} total | {fixed} fixed | {errors} errors | {skipped} skipped ===")
