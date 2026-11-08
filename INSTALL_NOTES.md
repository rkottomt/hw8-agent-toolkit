# Install notes

## Setup

Needs Python 3.10+ and `uv`. From the repo root:

```
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r mcp_server/requirements.txt
```

`.venv/` and `logs/` are gitignored, so a fresh clone needs the venv created and the prompt logs copied into `logs/`.

## NOTES

JSON does not allow comments, so the machine-specific values in `.mcp.json` are listed here. All three are under `mcpServers.log-search`, and all three start with `/Users/rohitkottomtharayil/hw8-agent-toolkit`. Change them on any other machine or if the repo moves:

| Field | Current value |
|---|---|
| `command` | `/Users/rohitkottomtharayil/hw8-agent-toolkit/.venv/bin/python` |
| `args[0]` | `/Users/rohitkottomtharayil/hw8-agent-toolkit/mcp_server/log_search_server.py` |
| `env.LOGS_DIR` | `/Users/rohitkottomtharayil/hw8-agent-toolkit/logs` |
