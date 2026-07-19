# Chinese Academic Preprint Platforms

When searching for Chinese-origin papers, arXiv is often NOT the primary source. Many Chinese researchers and companies (especially Huawei, Baidu, Alibaba) publish on domestic preprint platforms first.

## Key Platforms

### ChinaXiv (中国科学院科技论文预发布平台)
- **URL**: `https://chinaxiv.org/`
- **Affiliation**: Chinese Academy of Sciences (CAS)
- **Content**: Physics, CS, engineering, life sciences
- **Paper URL pattern**: `https://chinaxiv.org/abs/YYYYMM.NNNNN`
- **DOI prefix**: `10.12074/YYYYMM.NNNNN`
- **Notes**: Huawei's τ scaling law paper (2026) was published here. Major Chinese tech company papers often appear here before any English-language venue.

### arXiv China Mirror
- Some Chinese papers are cross-posted to arXiv, but with delays
- Always check ChinaXiv first for recent Chinese tech company papers

### Other Platforms
| Platform | URL | Focus |
|----------|-----|-------|
| CNKI (知网) | cnki.net | Journals, dissertations, conference proceedings |
| Wanfang (万方) | wanfangdata.com.cn | Similar to CNKI |
| CQVIP (维普) | cqvip.com | Journal articles |
| SciEngine (科学引擎) | sciengine.com | STM journals |

## Search Strategy for Chinese Tech Papers

1. **First**: `ddgs text -q '公司名 论文关键词 论文 PDF site:chinaxiv.org' -m 3`
2. **Second**: `ddgs text -q 'Company name paper keyword arxiv 2025 2026' -m 3`
3. **Third**: Search news articles (观察者网, 钛媒体, 财联社) — they often link directly to the paper and provide full translations/summaries

## Pitfalls

1. **ChinaXiv has anti-bot protection** — `curl` may get blocked. Use browser User-Agent headers: `curl -sL -H 'User-Agent: Mozilla/5.0 ...'`
2. **PDFs may not be directly downloadable** — some papers are view-only on the platform. News articles (观察者网 guancha.cn) often provide full Chinese translations.
3. **DOI format differs** — ChinaXiv uses `10.12074/` prefix, not the standard `10.48550/` arXiv prefix
4. **Language** — Papers are often Chinese-first with English abstracts. For learning guides, the Chinese version is preferred (user reads Chinese).
5. **Verification** — Cross-reference with news coverage to confirm paper details (author, date, content). News articles often have better structured summaries than the raw paper.
