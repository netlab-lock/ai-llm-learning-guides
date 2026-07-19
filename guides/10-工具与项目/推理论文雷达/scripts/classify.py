"""
LLM 推理加速论文分类器
使用 MiMo API 将论文自动分类到技术体系
"""
import json
import os
import sys
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
PAPERS_FILE = os.path.join(DATA_DIR, "papers.json")
CATEGORIES_FILE = os.path.join(DATA_DIR, "categories.json")

# MiMo API 配置
API_URL = "https://token-plan-cn.xiaomimimo.com/v1/chat/completions"
API_KEY = "tp-c326y5b7n4o48z2y3glody822jr9ktn8q9o9r4ya9xv2fk1b"
MODEL = "mimo-v2.5-pro"


def load_papers():
    with open(PAPERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_papers(papers):
    with open(PAPERS_FILE, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)


def load_categories_flat():
    """加载分类体系，展平为列表"""
    with open(CATEGORIES_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    flat = []
    for layer_key, layer in data["categories"].items():
        for sub_key, sub in layer["subcategories"].items():
            flat.append({
                "id": f"{layer_key}.{sub_key}",
                "layer": layer["name"],
                "name": sub["name"],
                "keywords": sub["keywords"]
            })
    return flat


def classify_paper(paper, categories_flat):
    """使用 MiMo 对论文进行分类"""
    title = paper.get("title", "")
    abstract = paper.get("abstract", "")[:500]
    
    # 构建分类选项
    cat_list = "\n".join([f"- {c['id']}: {c['name']} ({c['layer']})" for c in categories_flat])
    
    prompt = f"""你是一个 LLM 推理加速领域的专家。请将以下论文分类到最合适的技术类别。

论文标题: {title}
论文摘要: {abstract}

可选分类:
{cat_list}

请返回 JSON 格式:
{{"categories": ["分类ID1", "分类ID2"], "confidence": "high/medium/low", "reason": "简短说明"}}

注意:
1. 一篇论文可以属于多个分类（最多3个）
2. 只返回 JSON，不要其他内容
3. 如果论文不属于任何分类，返回空列表"""

    try:
        data = json.dumps({
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.1,
            "max_tokens": 200,
        }).encode("utf-8")
        
        req = urllib.request.Request(
            API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}",
            },
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
        
        content = result["choices"][0]["message"]["content"].strip()
        
        # 解析 JSON
        # 处理可能的 markdown 代码块
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        return json.loads(content)
    
    except Exception as e:
        print(f"  [ERROR] 分类失败: {e}")
        return {"categories": [], "confidence": "error", "reason": str(e)}


def classify_all(limit=50):
    """对所有未分类的论文进行分类"""
    papers = load_papers()
    categories_flat = load_categories_flat()
    
    # 找出未分类的论文
    unclassified = [
        (pid, p) for pid, p in papers.items()
        if not p.get("classified", False)
    ]
    
    if not unclassified:
        print("没有需要分类的论文!")
        return
    
    print(f"需要分类的论文: {len(unclassified)} 篇")
    print(f"分类体系: {len(categories_flat)} 个类别")
    print("-" * 50)
    
    classified_count = 0
    skipped_count = 0
    
    for i, (paper_id, paper) in enumerate(unclassified[:limit]):
        print(f"\n[{i+1}/{min(len(unclassified), limit)}] {paper['title'][:50]}...")
        
        result = classify_paper(paper, categories_flat)
        
        if result.get("categories"):
            paper["classified"] = True
            paper["categories_auto"] = result["categories"]
            paper["classify_confidence"] = result.get("confidence", "unknown")
            paper["classify_reason"] = result.get("reason", "")
            classified_count += 1
            print(f"  分类: {', '.join(result['categories'])} ({result.get('confidence', '?')})")
        else:
            paper["classified"] = True
            paper["categories_auto"] = []
            paper["classify_confidence"] = "none"
            paper["classify_reason"] = result.get("reason", "无匹配分类")
            skipped_count += 1
            print(f"  跳过: {result.get('reason', '无匹配分类')}")
    
    save_papers(papers)
    
    print("\n" + "=" * 50)
    print(f"分类完成!")
    print(f"  已分类: {classified_count} 篇")
    print(f"  跳过: {skipped_count} 篇")


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    classify_all(limit=limit)


if __name__ == "__main__":
    main()
