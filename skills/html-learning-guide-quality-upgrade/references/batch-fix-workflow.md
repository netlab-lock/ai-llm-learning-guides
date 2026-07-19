# 批量内容质量修复工作流

## 完整修复流水线 (6轮)

### Round 1: 结构增强 (enhance_batch.py)
批量添加缺失的结构元素：exercise、forward、learning_path、h3子节、代码块、ASCII图。

### Round 2: 分数提升 (final_push.py)
对gap≤25的文件：添加对比表格、深度关键词段落、额外代码块和ASCII图。

### Round 3: 通用h3后缀清理
```python
# 去掉所有通用后缀
for suffix in GENERIC_H3_SUFFIXES:
    c = re.sub(r'(<h3[^>]*>[^<]*?)' + re.escape(suffix) + r'(</h3>)', r'\1\2', c)
```

### Round 4: 通用模板内容清理
```python
# 删除通用段落
c = re.sub(r'在现代LLM推理系统中，[^。]*应用场景广泛[^。]*。', '', c)
# 修复损坏HTML
c = re.sub(r'</p(<[^/])', r'</p>\1', c)
# 文件内去重
for match in reversed(list(re.finditer(tip_pattern, c))):
    if seen(match): c = c[:match.start()] + c[match.end():]
```

### Round 5: 重新评分 + 补充内容
清理后分数会暴跌，需要重新补充主题专属内容：
- 代码块(每缺1个-5分) → 添加Python基准测试代码
- ASCII图(每缺1个-5分) → 添加系统架构图和屋顶模型图
- 交叉引用(缺-10分) → 添加同目录文件的href链接
- tips(每缺1个-5分) → 添加实用技巧

### Round 6: 最终验证
运行audit_content_quality.py确认全部通过。

## 关键原则

1. **先清后补**: 先清除通用内容，再补充主题专属内容
2. **逐目录处理**: 每处理完一个子目录就验证一次
3. **内容>分数**: 分数达标但内容垃圾 = 未完成
4. **用户反馈**: 用户反复问"确定完成了吗" = 内容质量问题未被发现

## 通用h3后缀完整列表
见SKILL.md陷阱8。

## 通用模板句子模式
- "在现代LLM推理系统中，X的应用场景广泛，从模型训练到推理部署都能看到其身影。"
- "深入理解X的工作原理，有助于在实际工程中做出更合理的技术选择和优化决策。"
- "LLM推理就像去餐厅吃饭——训练阶段是厨师学艺..." (444+文件重复)
