#!/usr/bin/env python3
"""
Fix duplicate teaching elements: call LLM API to generate unique tip/warn/deep/ascii/table
for each h2 section in HTML files.

Usage: python3 fix_duplicates.py <dir_or_file> [--dry-run] [--limit N]
Requires: hermes auth.json with xiaomi credential pool.
"""
import os, re, sys, json, time
import urllib.request, urllib.error

API_URL = 'https://token-plan-cn.xiaomimimo.com/v1/chat/completions'
MODEL = 'mimo-v2.5-pro'
API_KEY = ''

def load_config():
    global API_KEY
    with open(os.path.expanduser('~/.hermes/auth.json')) as f:
        auth = json.load(f)
    creds = auth.get('credential_pool', {}).get('xiaomi', [])
    if creds: API_KEY = creds[0].get('access_token', '')
    if not API_KEY: sys.exit("ERROR: No API key")

def call_llm(prompt, retries=3):
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {API_KEY}'}
    data = json.dumps({'model': MODEL, 'messages': [{'role': 'user', 'content': prompt}],
                       'temperature': 0.7, 'max_tokens': 16384}).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request(API_URL, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=600) as resp:
                r = json.loads(resp.read())
                return r['choices'][0]['message'].get('content') or r['choices'][0]['message'].get('reasoning_content')
        except urllib.error.HTTPError as e:
            if e.code == 429: time.sleep(30*(i+1))
            elif e.code == 500: time.sleep(10)
            else: return None
        except: 
            if i == retries-1: return None
            time.sleep(5)
    return None

def parse_json(resp):
    m = re.search(r'\{[\s\S]*"sections"[\s\S]*\}', resp)
    if not m: return None
    raw = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', m.group(0))
    raw = re.sub(r'\\(?!["\\/bfnrtu])', '', raw)
    try: return json.loads(raw, strict=False).get('sections', [])
    except json.JSONDecodeError:
        secs = []
        for m in re.finditer(r'"index"\s*:\s*(\d+)', raw):
            s, d = int(m.group(1)), m.start()
            sec = {'index': s}
            for k in ['h2','tip','warn','deep','ascii','table']:
                km = re.search(rf'"{k}"\s*:\s*"([^"]*)"', raw[d:d+2000])
                sec[k] = km.group(1) if km else ''
            secs.append(sec)
        return secs or None

def gen_content(fpath, sections):
    fn, dn = os.path.basename(fpath), os.path.basename(os.path.dirname(fpath))
    all_g = []
    for bs in range(0, len(sections), 8):
        batch = sections[bs:bs+8]
        sl = [f'[{i+1}] "{s["h2_text"]}" | {s["ctx"][:80]}' for i,s in enumerate(batch)]
        p = f'为HTML学习指南每个h2节生成独特教学内容。文件:{dn}/{fn}\nh2({len(batch)}):\n'+'\n'.join(sl)+'\n每节:tip(类比30-60字) warn(误区30-60字) deep(数字50-100字) ascii(3-6行) table(3-4行)\nJSON(无反斜杠):{{"sections":[{{"index":1,"h2":"","tip":"","warn":"","deep":"","ascii":"<pre></pre>","table":"<tr><th></th></tr>"}}]}}'
        resp = call_llm(p)
        if not resp: continue
        parsed = parse_json(resp)
        if parsed:
            for s in parsed: s['index'] = s.get('index',0)+bs
            all_g.extend(parsed)
    return all_g or None

def patch(html, secs, gen):
    gm = {g['index']-1: g for g in gen if 0 < g.get('index',0) <= len(secs)}
    n = 0
    for i in range(len(secs)-1, -1, -1):
        if i not in gm: continue
        g, s, e = gm[i], secs[i]['end'], secs[i+1]['end']-len(secs[i+1]['match']) if i+1<len(secs) else min(secs[i]['end']+3000, len(html))
        sec = html[s:e]
        for c in ['tip','warn','deep','ascii']: sec = re.sub(rf'<div class="{c}"[^>]*>.*?</div>','',sec,flags=re.DOTALL)
        el = f'\n<div class="tip"><strong>通俗类比：</strong>{g.get("tip","")}</div>\n<div class="warn"><strong>常见误区：</strong>{g.get("warn","")}</div>\n<div class="deep"><strong>深入探讨：</strong>{g.get("deep","")}</div>\n<div class="ascii">{g.get("ascii","")}</div>\n<table>{g.get("table","")}</table>\n'
        p = len(sec)-len(sec.lstrip())
        html = html[:s]+sec[:p]+el+sec[p:]+html[e:]; n+=1
    return html, n

def proc(fpath, dry=False):
    with open(fpath) as f: c = f.read()
    secs = [{'h2_text':re.sub(r'<[^>]*>','',m.group(1)).strip(),'ctx':re.sub(r'<[^>]*>','',c[m.end():m.end()+300]).strip()[:150],'end':m.end(),'match':m.group(0)} for m in re.finditer(r'<h2[^>]*>(.*?)</h2>',c,re.DOTALL)]
    if len(secs)<=1: return {'s':'skip'}
    tips = re.findall(r'class="tip"[^>]*>.*?通俗类比[：:]?(.*?)</div>',c,re.DOTALL)
    if tips and 1-len(set(re.sub(r'<[^>]*>','',t).strip()[:80] for t in tips))/max(len(tips),1)<0.2: return {'s':'skip'}
    gen = gen_content(fpath, secs)
    if not gen: return {'s':'err','e':'gen failed'}
    nc,n = patch(c,secs,gen)
    if not dry and n>0: open(fpath,'w').write(nc)
    return {'s':'ok','sec':len(secs),'fix':n}

def main():
    load_config(); p=sys.argv[1]; dry='--dry-run' in sys.argv
    if os.path.isfile(p): print(json.dumps(proc(p,dry),ensure_ascii=False))
    else:
        f=e=0
        for r,_,fs in os.walk(p):
            for fn in sorted(fs):
                if not fn.endswith('.html'): continue
                fp=os.path.join(r,fn); res=proc(fp,dry)
                if res['s']=='ok': f+=1; print(f"  +{fn}:{res['fix']}",file=sys.stderr)
                elif res['s']=='err': e+=1; print(f"  !{fn}:{res.get('e','')}",file=sys.stderr)
                time.sleep(5)
        print(f"\nDone: fixed={f} errors={e}")

if __name__=='__main__': main()
