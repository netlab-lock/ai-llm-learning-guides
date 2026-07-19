# 死链检测与修复工作流

## 适用场景
HTML学习指南中的交叉引用链接(`href`)指向不存在的文件。常见于：
- 批量脚本添加的链接使用了错误的文件名
- 文件重命名后链接未同步更新
- 相对路径计算错误

## 检测脚本

```python
import re, os

def check_dead_links(base_dir, target_dirs):
    """检测所有HTML文件中的死链"""
    # 构建现有文件集合
    all_files = set()
    for root, dirs, fnames in os.walk(base_dir):
        for fname in fnames:
            if fname.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, fname), base_dir)
                if any(rel.startswith(d) for d in target_dirs):
                    all_files.add(rel)
    
    broken = []
    for f in sorted(all_files):
        path = os.path.join(base_dir, f)
        with open(path, 'r', encoding='utf-8') as fh:
            c = fh.read()
        file_dir = os.path.dirname(f)
        
        for link in re.findall(r'href="([^"]*)"', c):
            if link.startswith(('http', '#', 'mailto')):
                continue
            target = os.path.normpath(os.path.join(file_dir, link))
            if not os.path.exists(os.path.join(base_dir, target)):
                broken.append((f, link, target))
    
    return broken
```

## 修复策略

### 策略1: 按前缀匹配（最常用）
```python
# 构建目录→文件映射
all_files_map = {}  # dirpath -> set of filenames
for root, dirs, fnames in os.walk(base_dir):
    for fname in fnames:
        if fname.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, fname), base_dir)
            d = os.path.dirname(rel)
            all_files_map.setdefault(d, set()).add(fname)

# 对每个死链，尝试按数字前缀匹配
def fix_link(link, file_dir, all_files_map):
    target_dir = os.path.normpath(os.path.join(file_dir, os.path.dirname(link)))
    target_fname = os.path.basename(link)
    
    if target_dir not in all_files_map:
        return None
    
    candidates = all_files_map[target_dir]
    prefix = target_fname.split('-')[0] if '-' in target_fname else ''
    
    # 精确匹配
    if target_fname in candidates:
        return link  # 不应到这里
    
    # 前缀匹配: "01-xxx.html" 匹配 "01-yyy.html"
    for c in candidates:
        if prefix and c.startswith(prefix):
            return os.path.relpath(os.path.join(target_dir, c), file_dir)
    
    # 退回目录第一个文件
    if candidates:
        return os.path.relpath(os.path.join(target_dir, sorted(candidates)[0]), file_dir)
    
    return None
```

### 策略2: 降级为 `#` 锚点
如果找不到正确文件，将链接改为 `href="#"`（保留链接文本，不破坏HTML结构）。

### 策略3: 移除链接标签但保留文本
```python
# <a href="dead.html">文本</a> → 文本
c = re.sub(r'<a[^>]*href="[^"]*"[^>]*>(.*?)</a>', r'\1', c)
```

## 完整修复流程

```python
# 1. 构建文件映射
all_files_map = {}
for root, dirs, fnames in os.walk(base_dir):
    for fname in fnames:
        if fname.endswith('.html'):
            rel = os.path.relpath(os.path.join(root, fname), base_dir)
            d = os.path.dirname(rel)
            all_files_map.setdefault(d, set()).add(fname)

# 2. 逐文件修复
for f in sorted(target_files):
    path = os.path.join(base_dir, f)
    with open(path, 'r', encoding='utf-8') as fh:
        c = fh.read()
    original = c
    file_dir = os.path.dirname(f)
    
    def fix_link_match(m):
        link = m.group(1)
        if link.startswith(('http', '#', 'mailto')):
            return m.group(0)
        target = os.path.normpath(os.path.join(file_dir, link))
        if os.path.exists(os.path.join(base_dir, target)):
            return m.group(0)  # 有效链接，不修改
        
        # 尝试修复
        new_link = fix_link(link, file_dir, all_files_map)
        if new_link:
            return f'href="{new_link}"'
        return 'href="#"'  # 降级
    
    c = re.sub(r'href="([^"]*)"', fix_link_match, c)
    
    if c != original:
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(c)
```

## 关键陷阱

### 陷阱1: 相对路径计算
`os.path.normpath(os.path.join(file_dir, link))` 可能产生 `../` 路径。
用 `os.path.exists(os.path.join(base_dir, target))` 验证而非直接拼接。

### 陷阱2: 外部链接不应修改
以 `http://` 或 `https://` 开头的链接是外部链接，跳过。
以 `#` 开头的是页内锚点，跳过。
以 `mailto:` 开头的是邮件链接，跳过。

### 陷阱3: 修复后需验证
修复后必须重新运行死链检测，确认0死链。
某些修复可能指向了错误的文件（前缀匹配不精确）。
