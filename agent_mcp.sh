#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
if command -v python3 >/dev/null 2>&1; then
	PYTHON=python3
else
	PYTHON=python
fi
"$PYTHON" -m pip install -q -r godot_runtime_mcp/requirements.txt >/dev/null 2>&1 || true
exec "$PYTHON" -m godot_runtime_mcp.agent_mcp
