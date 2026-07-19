# CodeGraph Installation on WSL + Windows

CodeGraph is a pre-indexed code knowledge graph for AI coding agents (Claude Code, Codex, Cursor, OpenCode, Hermes Agent). It exposes MCP tools that let agents query code structure without grep/read loops.

## Installation Steps

### WSL (Hermes Agent)
```bash
# Install via npm (Hermes node is at ~/.hermes/node/)
npm install -g @colbymchenry/codegraph

# Symlink to PATH (Hermes node bin not in PATH by default)
ln -sf ~/.hermes/node/bin/codegraph ~/.local/bin/codegraph

# Configure Hermes
codegraph install --target=hermes --yes
# Writes MCP server config to ~/.hermes/config.yaml
```

### Windows (Claude Code)
```bash
# Install via Windows npm
cmd.exe /c "npm install -g @colbymchenry/codegraph"

# Manually configure Claude Code:
# 1. Add to ~/.claude.json (top level):
#    "mcpServers": { "codegraph": { "type": "stdio", "command": "codegraph", "args": ["serve", "--mcp"] } }
# 2. Add to ~/.claude/settings.json:
#    "permissions": { "allow": ["mcp__codegraph__codegraph_search", "mcp__codegraph__codegraph_context", ...] }
# 3. Add usage instructions to ~/.claude/CLAUDE.md
```

### Per-project initialization
```bash
cd your-project
codegraph init -i    # Builds .codegraph/ knowledge graph index
```

## Key details
- v0.9.5 as of 2026-05-27
- Bundles its own runtime (no Node.js required for install.sh, but npm works too)
- 100% local, no API keys
- Supports 20+ languages via tree-sitter
- Auto-syncs via file watcher (OS native events)
- Tested: 94% fewer tool calls, 77% faster code exploration

## Pitfalls
- WSL codegraph binary at `~/.hermes/node/bin/codegraph` is NOT in PATH by default — must symlink
- Claude Code config is on Windows side (`/mnt/c/Users/<user>/.claude.json`) — edit from WSL using /mnt/ paths
- codegraph install --target=claude writes to WSL ~/.claude.json, NOT Windows — must configure manually
