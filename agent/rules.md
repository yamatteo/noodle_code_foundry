## Managed environment

This project uses `uv` for dependency management and virtual environments.
Always use `uv run python` instead of `python` directly.

## Testing

Whenever tests are added, removed, modified or renamed `${DOCS_PATH}/tests.md`
must be updated accordingly.

## Jupyter notebooks rules
- ALWAYS use Jupyter MCP for notebook tasks
- NEVER manually format JSON payloads or simulate notebook ops.
- FOR ANY Jupyter/Notebook action: just invoke the relevant MCP tool directly
  (e.g. `mcp__jupyter__list_notebooks`). The server is already connected at
  startup — do NOT call `connect_to_jupyter` unless explicitly asked to
  reconnect to a specific URL.
- Examples: "use_notebook", "read_notebook", "execute_cell" → invoke MCP tool.
- If no MCP response, say "Need Jupyter MCP connection" and STOP.
- When you need to interact in any way with a jupyter notebook, use exclusively
  the jupyter MCP tools.