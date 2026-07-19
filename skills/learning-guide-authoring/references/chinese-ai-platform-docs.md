# Chinese AI Platform Documentation Sources

Quick reference for scraping model documentation from Chinese AI company developer platforms.

## Kimi (Moonshot AI)

- **Model list**: `https://platform.moonshot.cn/docs/models`
- **API reference**: `https://platform.moonshot.cn/docs/api/models-overview`
- **Tech blog**: `https://moonshotai.github.io/Kimi-K2/`
- **Homepage**: `https://kimi.moonshot.cn` (check banner for announcements)

Known model IDs (as of 2026-05):
- `kimi-k2.6` — flagship, 256k ctx, multimodal, thinking param
- `kimi-k2.5` — multimodal, 256k, thinking/non-thinking modes
- `kimi-k2-0905-preview` — 256k, enhanced agentic coding
- `kimi-k2-0711-preview` — 128k, MoE 1T/32B (original K2)
- `kimi-k2-turbo-preview` — 60-100 tok/s, 256k
- `kimi-k2-thinking` — long thinking, 256k
- `moonshot-v1-8k/32k/128k` — legacy dense models
- `moonshot-v1-*-vision-preview` — legacy vision models

API base: `https://api.moonshot.cn/v1` (OpenAI-compatible)

## DeepSeek

- **API docs**: `https://api-docs.deepseek.com/`
- **Model info**: `https://api-docs.deepseek.com/quick_start/pricing`
- **Technical reports**: published on arXiv and GitHub

## Qwen (Alibaba Cloud / Tongyi)

- **Product page**: `https://tongyi.aliyun.com` (model list embedded in JSON/JS)
- **Model studio**: `https://help.aliyun.com/zh/model-studio/`
- **DashScope API**: `https://dashscope.aliyuncs.com`
- **HuggingFace**: `https://huggingface.co/Qwen`
- **Blog**: `https://qwen.ai/blog`

Known model IDs (as of 2026-05):
- `qwen3-max` — flagship, trillion-param pre-training
- `qwen-plus` — balanced performance/cost
- `qwen-flash` — lightweight, fast
- `qwen3-coder-plus` — 358 languages, 1M ctx, agentic coding
- `qwen3-vl-plus` — vision (image/video)
- `qwen3-omni-flash` — full multimodal (text+vision+audio)
- `qwen-image` — image generation

Also: Wan (万相) video/image generation series, Fun (百聆) speech series.

The tongyi.aliyun.com product page embeds full model metadata in Next.js `__next_f` JSON chunks. Look for `"models":[...]` arrays with name/code/desc fields.

## GLM (Zhipu AI)

- **Open platform**: `https://open.bigmodel.cn/dev/api`
- **Model docs**: `https://open.bigmodel.cn/dev/api#glm-4`

Known model families: GLM-4, GLM-4V (vision), GLM-4-Long (1M ctx), ChatGLM (open-source 6B/9B), CogVLM (vision-language), CogVideoX (video generation).

## Scraping Pattern (Next.js/Mintlify sites)

Most Chinese AI doc sites use Next.js + Mintlify. Content is SSR-rendered in JSON chunks.

```bash
# Extract model names and descriptions
curl -sL --max-time 15 "https://platform.moonshot.cn/docs/models" 2>/dev/null \
  | sed 's/<[^>]*>//g' | sed '/^$/d' \
  | grep -i "model\|模型\|context\|上下文\|参数" | head -40

# Find banner announcements (new model releases)
curl -sL "https://platform.moonshot.cn/docs/models" 2>/dev/null \
  | grep -oP '"content":"[^"]*"' | head -5

# Extract code examples from API docs
curl -sL "https://platform.moonshot.cn/docs/api/models-overview" 2>/dev/null \
  | sed 's/<[^>]*>//g' | sed '/^$/d' \
  | grep -i "model\|kimi\|thinking\|参数" | head -40

# Qwen/Tongyi product page (Next.js, models in __next_f JSON)
curl -sL --max-time 15 "https://tongyi.aliyun.com" 2>/dev/null \
  | grep -oP '"name":"[^"]*".*?"desc":"[^"]*"' | head -20
```

## Pitfalls

- Google/DuckDuckGo search often fails or returns empty for Chinese AI model queries. Go directly to platform docs.
- Browser automation (CDP) tends to timeout on these sites. Use curl instead.
- Model parameter counts (total/active) may not be officially disclosed — mark as "推测" (estimated) in guides.
- Model deprecation timelines are often announced only in platform docs, not blog posts.
