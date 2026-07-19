# Tool-Specific Quirks for Project Trial Guides

## Browser Use + MiMo API

### Setup
```python
from browser_use import Agent, Browser, ChatOpenAI

llm = ChatOpenAI(
    model="mimo-v2.5-pro",  # text-only, reliable
    base_url="https://token-plan-cn.xiaomimimo.com/v1",
    api_key="<key>",
)

agent = Agent(
    task="...",
    llm=llm,
    use_vision=False,  # CRITICAL for MiMo-v2.5-pro
)
```

### MiMo Dual-Model Quirk
- `mimo-v2.5-pro`: Text reasoning. Returns 404 "No endpoints found that support image input" if use_vision=True. Use with `use_vision=False`.
- `mimo-v2.5`: Vision model. Works with `use_vision=True` but hallucinates data (got #2 and #3 repos wrong in GitHub trending test).
- **Best combo**: `mimo-v2.5-pro` + `use_vision=False` — most reliable.

### Dependencies
```
pip install browser-use langchain-openai
```
- `langchain-openai` is needed for ChatOpenAI (not bundled with browser-use)
- Python 3.11+ required
- Chrome browser required (uses CDP, not Playwright)

### Windows-Specific
- Use `py -3.14` to specify Python version (default python may be old Anaconda)
- Add `sys.stdout.reconfigure(encoding='utf-8')` for emoji output
- PowerShell `-Command` mangles quotes — write .py files instead of inline code
- Chinese paths (`D:\学习\`) get garbled in PowerShell — copy scripts to Desktop

### Browser Use Auto-Downloads
Browser Use automatically downloads 3 Chrome extensions on first run:
- uBlock Origin Lite (ad blocker)
- I still don't care about cookies
- Force Background Tab

## Graphify

### Setup
```
pip install graphifyy  # Note: extra 'y', PyPI name conflict
graphify install       # Install to Claude Code
graphify hermes install  # Install to Hermes
```

### Key Commands
```bash
graphify extract .                    # AST extraction (no LLM needed for code)
graphify extract . --backend openai   # With LLM for docs/papers/images
graphify cluster-only .               # Generate graph.html + GRAPH_REPORT.md
graphify query "question"             # BFS traversal query
graphify path "A" "B"                 # Shortest path
graphify explain "X"                  # Node explanation
graphify benchmark                    # Token reduction measurement
graphify . --watch                    # Auto-rebuild on file changes
graphify hook install                 # Git post-commit hook
```

### Quirks
- PyPI package is `graphifyy` but CLI command is `graphify`
- Pure code projects (AST) don't need LLM — only docs/papers/images do
- `extract` does AST + optional LLM; `cluster-only` does clustering + visualization
- `graphify-out/` directory is created in the target project directory
- graph.html is self-contained (can open in any browser)
- Token reduction: small projects ~3x, large projects (50+ files) ~71x
