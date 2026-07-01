"""Cursor MCP stdio entry point; communicates with a running game over HTTP."""

from __future__ import annotations

import json
from typing import Annotated

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import Field

DEFAULT_HOST = "127.0.0.1"

mcp = FastMCP("godot-game")


class GameCommandError(RuntimeError):
    """Game-side error response or HTTP failure."""


def send_http(
    port: int,
    script: str,
    *,
    host: str = DEFAULT_HOST,
    timeout_seconds: float = 30.0,
) -> object:
    """POST GDScript to the game port; return parsed response ``data`` on success."""
    url = f"http://{host}:{port}/"
    try:
        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.post(
                url,
                content=script.encode("utf-8"),
                headers={"Content-Type": "text/plain; charset=utf-8"},
            )
            response.raise_for_status()
    except httpx.TimeoutException as error:
        raise GameCommandError(
            f"request timed out ({timeout_seconds}s): port={port}",
        ) from error
    except httpx.HTTPError as error:
        raise GameCommandError(f"HTTP request failed: port={port}, {error}") from error

    try:
        body = response.json()
    except json.JSONDecodeError as error:
        raise GameCommandError(
            f"response is not valid JSON: {response.text}",
        ) from error

    if not isinstance(body, dict):
        raise GameCommandError(f"response must be a JSON object: {body}")

    if not body.get("ok", False):
        raise GameCommandError(str(body.get("error", "unknown error")))

    return body.get("data", "")


@mcp.tool()
def run(
    port: Annotated[
        int,
        Field(description="Port from game log marker <<<GAME_MCP::PORT=XXXX>>>."),
    ],
    script: Annotated[
        str,
        Field(
            description=(
                "Full GDScript source code; must define static func run(scene_tree). "
                "run may be async (use await inside)."
            ),
        ),
    ],
) -> str:
    """Execute GDScript in a running Godot instance."""
    try:
        result = send_http(port, script)
    except GameCommandError as error:
        return f"error: {error}"
    return json.dumps(result, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    mcp.run()
