"""
LLM 推理加速每日速报生成器
生成 HTML 格式的每日论文速报
"""
import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
REPORTS_DIR = os.path.join(BASE_DIR, "daily-reports")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")


def load_papers():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_categories():
    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_today_papers(papers, date_str=None):
    """获取今天的论文"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    today_papers = []
    for pid, p in papers.items():
        fetch_date = p.get("fetch_date", "")[:10]
        if fetch_date == date_str:
            today_papers.append(p)
    
    # 按分类分组
    return sorted(today_papers, key=lambda x: x.get("published", ""), reverse=True)


def group_by_category(papers, categories):
    """按技术分类分组"""
    # 建立分类 ID 到名称的映射
    cat_map = {}
    for layer_key, layer in categories["categories"].items():
        for sub_key, sub in layer["subcategories"].items():
            cat_id = f"{layer_key}.{sub_key}"
            cat_map[cat_id] = {
                "layer": layer["name"],
                "name": sub["name"],
                "papers": []
            }
    
    # 分类论文
    unclassified = []
    for paper in papers:
        paper_cats = paper.get("categories_auto", [])
        if not paper_cats:
            unclassified.append(paper)
        else:
            for cat_id in paper_cats:
                if cat_id in cat_map:
                    cat_map[cat_id]["papers"].append(paper)
    
    # 只返回有论文的分类
    result = []
    for cat_id, info in cat_map.items():
        if info["papers"]:
            result.append({
                "id": cat_id,
                "layer": info["layer"],
                "name": info["name"],
                "papers": info["papers"]
            })
    
    if unclassified:
        result.append({
            "id": "unclassified",
            "layer": "未分类",
            "name": "待人工审核",
            "papers": unclassified
        })
    
    return result


def generate_html(papers, categories, date_str=None):
    """生成 HTML 速报"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    grouped = group_by_category(papers, categories)
    total = len(papers)
    
    # 统计
    stats = {}
    for group in grouped:
        layer = group["layer"]
        if layer not in stats:
            stats[layer] = 0
        stats[layer] += len(group["papers"])
    
    # 生成分类卡片
    category_cards = ""
    for group in grouped:
        paper_items = ""
        for p in group["papers"]:
            arxiv_id = p.get("arxiv_id", "")
            title = p.get("title", "未知标题")
            authors = ", ".join(p.get("authors", [])[:3])
            if len(p.get("authors", [])) > 3:
                authors += " et al."
            abstract = p.get("abstract", "")[:200]
            if len(p.get("abstract", "")) > 200:
                abstract += "..."
            confidence = p.get("classify_confidence", "")
            
            paper_items += f"""
            <div class="paper-card">
              <div class="paper-title">
                <a href="https://arxiv.org/abs/{arxiv_id}" target="_blank">{title}</a>
              </div>
              <div class="paper-meta">
                <span class="paper-id">{arxiv_id}</span>
                <span class="paper-date">{p.get('published', '')}</span>
                <span class="confidence confidence-{confidence}">{confidence}</span>
              </div>
              <div class="paper-authors">{authors}</div>
              <div class="paper-abstract">{abstract}</div>
            </div>"""
        
        category_cards += f"""
        <div class="category-section">
          <h3 class="category-title">
            <span class="category-layer">{group['layer']}</span>
            {group['name']}
            <span class="paper-count">{len(group['papers'])} 篇</span>
          </h3>
          <div class="papers-list">
            {paper_items}
          </div>
        </div>"""
    
    # 统计卡片
    stats_html = ""
    for layer, count in stats.items():
        stats_html += f'<div class="stat-card"><div class="stat-number">{count}</div><div class="stat-label">{layer}</div></div>'
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>LLM 推理加速论文速报 - {date_str}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; line-height: 1.7; }}
.container {{ max-width: 960px; margin: 0 auto; padding: 20px; }}
h1 {{ color: #58a6ff; font-size: 1.8em; margin-bottom: 5px; }}
h2 {{ color: #f0f6fc; border-left: 4px solid #58a6ff; padding-left: 12px; margin: 25px 0 12px; font-size: 1.3em; }}
h3 {{ color: #79c0ff; margin: 15px 0 8px; }}
.header {{ background: linear-gradient(135deg, #161b22 0%, #0d1d30 100%); border: 1px solid #30363d; border-radius: 10px; padding: 20px; margin-bottom: 20px; }}
.header .date {{ color: #8b949e; font-size: 0.9em; }}
.stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 15px 0; }}
.stat-card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px; min-width: 120px; text-align: center; }}
.stat-number {{ color: #58a6ff; font-size: 1.8em; font-weight: bold; }}
.stat-label {{ color: #8b949e; font-size: 0.8em; }}
.category-section {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 16px; margin: 12px 0; }}
.category-title {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
.category-layer {{ background: #21262d; border: 1px solid #30363d; border-radius: 4px; padding: 2px 8px; font-size: 0.7em; color: #8b949e; }}
.paper-count {{ color: #8b949e; font-size: 0.8em; margin-left: auto; }}
.paper-card {{ border-bottom: 1px solid #21262d; padding: 12px 0; }}
.paper-card:last-child {{ border-bottom: none; }}
.paper-title a {{ color: #58a6ff; text-decoration: none; font-weight: bold; }}
.paper-title a:hover {{ text-decoration: underline; }}
.paper-meta {{ display: flex; gap: 10px; margin: 4px 0; font-size: 0.8em; }}
.paper-id {{ color: #8b949e; }}
.paper-date {{ color: #8b949e; }}
.confidence {{ padding: 1px 6px; border-radius: 4px; font-size: 0.75em; }}
.confidence-high {{ background: #0d2818; color: #3fb950; }}
.confidence-medium {{ background: #2d1b00; color: #d29922; }}
.confidence-low {{ background: #2d0000; color: #f85149; }}
.confidence-none {{ background: #21262d; color: #8b949e; }}
.paper-authors {{ color: #8b949e; font-size: 0.85em; }}
.paper-abstract {{ color: #8b949e; font-size: 0.85em; margin-top: 6px; }}
.nav {{ display: flex; gap: 15px; margin: 20px 0; }}
.nav a {{ color: #58a6ff; text-decoration: none; padding: 6px 12px; border: 1px solid #30363d; border-radius: 6px; }}
.nav a:hover {{ border-color: #58a6ff; }}
.footer {{ margin-top: 30px; padding-top: 15px; border-top: 1px solid #21262d; text-align: center; color: #8b949e; font-size: 0.85em; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📡 LLM 推理加速论文速报</h1>
    <div class="date">{date_str} | 共 {total} 篇新论文</div>
    <div class="stats">
      {stats_html}
    </div>
  </div>
  
  <div class="nav">
    <a href="../index.html">← 首页</a>
    <a href="../data/papers.json" target="_blank">📄 全部论文 JSON</a>
  </div>
  
  {category_cards}
  
  <div class="footer">
    <p>自动生成于 {datetime.now().strftime("%Y-%m-%d %H:%M")} | 
       数据来源: arXiv | 分类: MiMo API</p>
    <p><a href="../index.html" style="color:#58a6ff">返回首页</a></p>
  </div>
</div>
</body>
</html>"""
    
    return html


def generate_today(date_str=None):
    """生成今天的速报"""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    
    papers = load_papers()
    categories = load_categories()
    
    today_papers = get_today_papers(papers, date_str)
    
    if not today_papers:
        print(f"今天 ({date_str}) 没有新论文!")
        return None
    
    html = generate_html(today_papers, categories, date_str)
    
    # 保存
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_file = os.path.join(REPORTS_DIR, f"{date_str}.html")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"速报已生成: {report_file}")
    print(f"包含 {len(today_papers)} 篇论文")
    
    return report_file


def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else None
    generate_today(date_str)


if __name__ == "__main__":
    import sys
    main()
