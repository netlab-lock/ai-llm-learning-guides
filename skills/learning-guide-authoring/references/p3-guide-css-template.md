# P3 学习指南 CSS 模板

本文件记录了在创建 P3 学习指南时使用的标准 CSS 模板，供后续批量创建 HTML 文件时复用。

## 标准 CSS

```css
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#c9d1d9;--heading:#f0f6fc;--blue:#58a6ff;--green:#3fb950;--yellow:#d29922;--red:#f85149;--purple:#a371f7;--cyan:#39d2c0}
*{margin:0;padding:0;box-sizing:border-box}
body{background:var(--bg);color:var(--text);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;line-height:1.8;font-size:16px}
.container{max-width:900px;margin:0 auto;padding:2rem 1.5rem}
h1{color:var(--blue);font-size:2rem;margin:1rem 0 .5rem}
h2{color:var(--heading);font-size:1.5rem;margin:2rem 0 .8rem;padding-left:.8rem;border-left:4px solid var(--blue)}
h3{color:var(--cyan);font-size:1.2rem;margin:1.5rem 0 .5rem}
h4{color:var(--yellow);font-size:1.05rem;margin:1.2rem 0 .4rem}
p{margin:.6rem 0}a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
code{background:#21262d;color:#79c0ff;padding:.15em .4em;border-radius:4px;font-size:.9em}
pre{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem;overflow-x:auto;margin:1rem 0;font-size:.9em;line-height:1.6}
pre code{background:none;padding:0}
table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.9em}
th,td{border:1px solid var(--border);padding:.5rem .8rem;text-align:left}
th{background:#161b22;color:var(--blue);font-weight:600}
tr:nth-child(even){background:rgba(22,27,34,.5)}
.nav{background:var(--card);border-bottom:1px solid var(--border);padding:.6rem 1.5rem;display:flex;justify-content:space-between;align-items:center;position:sticky;top:0;z-index:100}
.nav a{color:var(--blue);font-size:.9rem}.nav span{color:var(--heading);font-weight:600;font-size:.95rem}
.footer{text-align:center;margin-top:3rem;padding:1.5rem;border-top:1px solid var(--border);color:#8b949e;font-size:.85rem}
.tip,.warn,.exercise,.deep{border-radius:8px;padding:1rem 1.2rem;margin:1rem 0}
.tip{background:#0d1d30;border-left:4px solid var(--blue)}
.warn{background:#2d1b00;border-left:4px solid var(--yellow)}
.exercise{background:#0d2818;border-left:4px solid var(--green)}
.deep{background:#1a1024;border-left:4px solid var(--purple)}
.ascii{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1rem;font-family:monospace;font-size:.85em;line-height:1.5;overflow-x:auto;white-space:pre}
.badge{display:inline-block;padding:.15em .6em;border-radius:12px;font-size:.75em;font-weight:600;margin:0 .3em}
.badge-blue{background:rgba(88,166,255,.15);color:var(--blue)}
.badge-green{background:rgba(63,185,80,.15);color:var(--green)}
.badge-yellow{background:rgba(210,153,34,.15);color:var(--yellow)}
.badge-purple{background:rgba(163,113,247,.15);color:var(--purple)}
.badge-red{background:rgba(248,81,73,.15);color:var(--red)}
.badge-cyan{background:rgba(57,210,192,.15);color:var(--cyan)}
.formula{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:1.2rem;margin:1rem 0;text-align:center;font-size:1.1em;color:var(--cyan);font-family:monospace}
.next-prev{display:flex;justify-content:space-between;margin-top:2rem;padding-top:1rem;border-top:1px solid var(--border)}
ul,ol{margin:.5rem 0 .5rem 1.5rem}li{margin:.3rem 0}
```

## 模块完成度检查命令

```bash
# 检查所有模块的图和代码块数量
for d in Topic1 Topic2 ...; do
  for f in "/path/to/$d"/*.html; do
    bn=$(basename "$f")
    test "$bn" = "index.html" && continue
    a=$(grep -c 'class="ascii"' "$f")
    c=$(grep -c '<pre><code>' "$f")
    if [ "$a" -lt 2 ] || [ "$c" -lt 1 ]; then
      echo "$d/$bn: ${a}图 ${c}码"
    fi
  done
done
```

## 文件大小检查命令

```bash
# 检查所有文件大小
for d in Topic1 Topic2 ...; do
  size=$(du -sb "/path/to/$d" | cut -f1)
  kb=$((size/1024))
  echo "$d: ${kb}KB"
done
```
