"""
LLM 推理加速论文抓取器
使用 arXiv API 搜索并下载论文元数据
"""
import json
import os
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")

# arXiv API 配置
ARXIV_API = "http://export.arxiv.org/api/query"
MAX_RESULTS_PER_QUERY = 50
DELAY_BETWEEN_REQUESTS = 3  # 秒，遵守 arXiv rate limit


def load_categories():
    """加载分类体系"""
    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_papers():
    """加载已有论文"""
    if os.path.exists(PAPERS_FILE):
        with open(PAPERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_papers(papers):
    """保存论文"""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)


def search_arxiv(query, max_results=50, days_back=7):
    """搜索 arXiv 论文"""
    # 构建查询：关键词 + 时间范围
    search_query = f'all:"{query}"'
    
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    
    url = f"{ARXIV_API}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LLM-Inference-Radar/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            xml_data = response.read().decode("utf-8")
        return parse_arxiv_response(xml_data)
    except Exception as e:
        print(f"  [ERROR] 搜索失败: {query[:30]}... - {e}")
        return []


def parse_arxiv_response(xml_data):
    """解析 arXiv API 的 XML 响应"""
    root = ET.fromstring(xml_data)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    
    papers = []
    for entry in root.findall("atom:entry", ns):
        paper = {}
        
        # ID
        id_elem = entry.find("atom:id", ns)
        if id_elem is not None:
            paper["arxiv_id"] = id_elem.text.split("/abs/")[-1]
        
        # 标题
        title_elem = entry.find("atom:title", ns)
        if title_elem is not None:
            paper["title"] = " ".join(title_elem.text.strip().split())
        
        # 摘要
        summary_elem = entry.find("atom:summary", ns)
        if summary_elem is not None:
            paper["abstract"] = " ".join(summary_elem.text.strip().split())
        
        # 作者
        authors = []
        for author in entry.findall("atom:author", ns):
            name = author.find("atom:name", ns)
            if name is not None:
                authors.append(name.text.strip())
        paper["authors"] = authors
        
        # 发布日期
        published = entry.find("atom:published", ns)
        if published is not None:
            paper["published"] = published.text[:10]
        
        # 更新日期
        updated = entry.find("atom:updated", ns)
        if updated is not None:
            paper["updated"] = updated.text[:10]
        
        # 分类
        categories = []
        for cat in entry.findall("atom:category", ns):
            term = cat.get("term")
            if term:
                categories.append(term)
        paper["categories"] = categories
        
        # PDF 链接
        for link in entry.findall("atom:link", ns):
            if link.get("title") == "pdf":
                paper["pdf_url"] = link.get("href")
        
        # 主分类
        primary_cat = entry.find("arxiv:primary_category", ns)
        if primary_cat is not None:
            paper["primary_category"] = primary_cat.get("term")
        
        if paper.get("arxiv_id") and paper.get("title"):
            papers.append(paper)
    
    return papers


def fetch_all(days_back=7, max_per_query=30):
    """抓取所有分类的论文"""
    categories = load_categories()
    existing_papers = load_papers()
    
    all_new_papers = []
    queries = categories.get("search_queries", [])
    
    print(f"开始抓取论文，共 {len(queries)} 个查询...")
    print(f"已有论文: {len(existing_papers)} 篇")
    print(f"时间范围: 最近 {days_back} 天")
    print("-" * 50)
    
    for i, query in enumerate(queries):
        print(f"\n[{i+1}/{len(queries)}] 搜索: {query}")
        papers = search_arxiv(query, max_results=max_per_query)
        
        new_count = 0
        for paper in papers:
            paper_id = paper["arxiv_id"]
            
            # 去重
            if paper_id in existing_papers:
                continue
            
            # 检查时间范围
            pub_date = paper.get("published", "")
            if pub_date:
                try:
                    pub_dt = datetime.strptime(pub_date, "%Y-%m-%d")
                    cutoff = datetime.now() - timedelta(days=days_back)
                    if pub_dt < cutoff:
                        continue
                except ValueError:
                    pass
            
            # 添加元数据
            paper["fetch_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            paper["query"] = query
            paper["classified"] = False
            paper["categories_manual"] = []
            
            existing_papers[paper_id] = paper
            all_new_papers.append(paper)
            new_count += 1
        
        print(f"  找到 {len(papers)} 篇，新增 {new_count} 篇")
        
        # 遵守 rate limit
        if i < len(queries) - 1:
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # 保存
    save_papers(existing_papers)
    
    print("\n" + "=" * 50)
    print(f"抓取完成!")
    print(f"  新增论文: {len(all_new_papers)} 篇")
    print(f"  总论文数: {len(existing_papers)} 篇")
    
    return all_new_papers


def fetch_recent(days_back=3):
    """只抓取最近几天的论文（日常使用）"""
    return fetch_all(days_back=days_back, max_per_query=20)


def main():
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--recent":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        papers = fetch_recent(days_back=days)
    else:
        days = int(sys.argv[1]) if len(sys.argv) > 1 else 7
        papers = fetch_all(days_back=days)
    
    # 打印新论文
    if papers:
        print(f"\n新增论文列表:")
        for p in papers[:20]:
            print(f"  [{p.get('published', '?')}] {p['title'][:60]}...")
            print(f"    arXiv: {p['arxiv_id']}")
            print(f"    作者: {', '.join(p['authors'][:3])}")
            print()


if __name__ == "__main__":
    main()
