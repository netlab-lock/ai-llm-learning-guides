# Paper-to-Learning-Guide Workflow

When the user asks to "find a paper, analyze it, and create a learning guide" (找论文原文, 解读, 做学习指南), follow this pipeline:

## Step 1: Find the Paper

```bash
# Chinese paper search (ChinaXiv, CNKI, etc.)
ddgs text -q '<中文关键词> 论文 原文' -m 5
ddgs text -q '<English title> paper PDF arxiv chinaxiv' -m 5
```

**Key platforms for Chinese papers:**
- ChinaXiv (中国科学院预印本): `chinaxiv.org/abs/...`
- CNKI (中国知网): `cnki.net`
- arXiv: `arxiv.org/abs/...`

**Always capture:** DOI, author, publication date, platform URL.

## Step 2: Gather Context from Multiple Sources

Fetch 3-5 sources in parallel via delegate_task:
- Official announcement (press release)
- Detailed Chinese analysis (观察者网, 钛媒体, 知乎专栏)
- English coverage (TechXplore, CarNewsChina, SemiAnalysis)
- Industry commentary (财联社, 36氪, IT之家)

**Scraping pattern for Chinese sites** (often have anti-bot):
```bash
curl -sL -H 'User-Agent: Mozilla/5.0 ...' 'URL' | sed 's/<[^>]*>//g' | sed '/^$/d' | head -500
```

## Step 3: Create the Learning Guide Structure

Standard structure for a paper-based guide:
```
D:\学习\<topic-name>\
├── index.html              ← Paper info + roadmap + key concepts
├── 00-前置知识.html         ← FOUNDATION: what reader needs to know first
├── 01-背景与动机.html       ← Why this paper exists
├── 02-核心理论.html         ← The main contribution
├── 03-关键技术.html         ← Implementation details
├── 04-系统应用.html         ← Real-world applications
├── 05-对比与定位.html       ← Comparison with prior work
└── 06-开放问题与展望.html   ← Limitations and future
```

## Step 4: The Foundation Module (00) Pattern

**Critical for non-expert users.** When user says they're a beginner (小白/完全不懂):

1. **Identify prerequisite knowledge** by listing every technical term in the paper that a layperson wouldn't know
2. **Organize bottom-up**: physical basics → building blocks → systems → the paper's context
3. **Use heavy visual aids**: ASCII diagrams, life analogies (类比), comparison tables
4. **Include a glossary** (术语表) at the end — 15-30 terms with one-line definitions
5. **Add a self-test** (自测题) — "if you can answer these, you're ready to read the paper"
6. **Target 50-60KB** for the foundation module — it should be the longest file

Example foundation topics for a semiconductor paper:
```
沙子→晶圆 → 晶体管/MOSFET → 逻辑门 → 工艺节点(nm) → 光刻(DUV/EUV)
→ RC延迟/关键路径 → 时钟分配 → 存储层次(SRAM/DRAM/缓存)
→ 封装(2D/2.5D/3D/TSV/混合键合) → HBM/存储墙 → SerDes/互连
→ 扇出困境(N² vs N) → 术语表 → 自测题
```

## Pitfalls

1. **Don't assume the user knows the field.** Always ask or infer from context. If they say "小白", the foundation module is mandatory and must be truly beginner-friendly.
2. **Multi-part file generation.** For files >30KB, write in parts (3-4 segments), then concatenate via terminal:
   ```python
   write_file("file_part1.html", part1)
   write_file("file_part2.html", part2)
   terminal("cat part1.html part2.html > final.html && rm part*.html")
   ```
3. **Update navigation after adding foundation module.** The index.html needs a new card, and the original first module (01) needs its prev-link updated to point to 00.
4. **Chinese paper sources are often behind anti-bot walls.** Use User-Agent header with curl. Guancha.cn and tmtpost.com both require this.
5. **Verify DOI/URL before citing.** ChinaXiv DOIs use format `10.12074/YYYYMM.NNNNNN`.
