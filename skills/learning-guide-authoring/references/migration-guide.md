# 迁移学习指南制作环境到新电脑

## 核心依赖清单

制作学习指南需要的最小集合：

### 必须复制的 Skill（整目录打包）
```
~/.hermes/skills/productivity/learning-guide-authoring/    ← 核心，50+文件
~/.hermes/skills/research/duckduckgo-search/               ← 搜索能力
~/.hermes/skills/research/arxiv/                           ← 论文搜索
```

### 必须复制的配置
```
~/.hermes/config.yaml    ← MiMo模型配置 + delegation超时设置
```

关键配置项：
```yaml
model:
  default: mimo-v2.5-pro
  provider: xiaomi
  base_url: https://token-plan-cn.xiaomimimo.com/v1
  max_tokens: 131072
delegation:
  child_timeout_seconds: 1800    # 子代理30分钟超时
  max_concurrent_children: 3
```

### 必须安装的 CLI 工具
```bash
pip install duckduckgo-search    # ddgs 搜索工具
sudo apt install mupdf-tools     # PDF论文提取 (可选)
```

## 打包命令

在当前电脑执行：
```bash
# 打包所有相关skill
cd ~/.hermes/skills
tar czf ~/hermes-skills-backup.tar.gz \
  productivity/learning-guide-authoring \
  research/duckduckgo-search \
  research/arxiv

# 单独打包config
cp ~/.hermes/config.yaml ~/hermes-config-backup.yaml
```

## 恢复命令

新电脑执行：
```bash
# 恢复skill
cd ~/.hermes/skills
tar xzf hermes-skills-backup.tar.gz

# 恢复config（注意合并已有配置）
cp hermes-config-backup.yaml ~/.hermes/config.yaml

# 装ddgs
pip install duckduckgo-search
```

## 不需要复制的

- `D:\学习\ 文件` — 内容产出，不是工具链（用网盘/Git/Syncthing同步）
- 其他skill — 做学习指南用不到
- Python环境 — 那边Hermes自带
- ddgs二进制 — pip install即可

## 总量

一个tar包(~200KB) + 一个yaml文件 + 一条pip命令。5分钟搞定。
