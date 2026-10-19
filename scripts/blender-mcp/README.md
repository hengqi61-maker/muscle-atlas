# Guarded Blender MCP helpers

Local wrappers around pinned `mcp-for-blender==2.2.0` for Muscle Atlas observation.

- `guard.py` / `bootstrap.py` / `server.py` — policy, Blender side, Codex stdio side
- `reviewed-scripts/` — exact SHA-registered observation scripts only

Machine-local runtime (policy, token, isolated Blender user tree, experimental GLB copy) lives under `~/.codex/tools/mcp-for-blender/` and is not committed.

See `docs/dev/blender-mcp-integration.md`.
