# Install notes

## Setup

Needs Python 3.10+ and `uv`. From the repo root:

```
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python -r mcp_server/requirements.txt
```

`.venv/` and `logs/` are gitignored, so a fresh clone needs the venv created and the prompt logs copied into `logs/`.

## NOTES

JSON does not allow comments, so the machine-specific values in `.mcp.json` are listed here. All three are under `mcpServers.log-search`. Replace the placeholders with absolute paths on your machine:

| Field | Value to set |
|---|---|
| `command` | `<YOUR_PYTHON_PATH>` (the absolute path to `.venv/bin/python`) |
| `args[0]` | `<ABSOLUTE_REPO_PATH>/mcp_server/log_search_server.py` |
| `env.LOGS_DIR` | `<ABSOLUTE_REPO_PATH>/logs` |
