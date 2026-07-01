# Godot Runtime MCP

Send GDScript to a running Godot instance and execute it at runtime—for debugging, white-box testing, and inspecting scene state.

## Install

In your Godot project root, add this repo as a submodule under `addons/`:

```bash
cd /path/to/your/godot-project
git submodule add https://github.com/EEEEEEEEthan/godot_runtime_mcp.git addons/godot_runtime_mcp
```

## Setup

### 1. Autoload

In **Project → Project Settings → Autoload**, add:

```
res://addons/godot_runtime_mcp/game_mcp.gd
```

### 2. MCP configuration

In the project root `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "godot-game": {
      "command": "addons/godot_runtime_mcp/agent_mcp.bat"
    }
  }
}
```

Requires Python 3.10+.

### 3. Get the port number

After the game starts, the log prints:

```
<<<GAME_MCP::PORT=6789>>>
```

You can also have the agent launch the game itself—it will automatically include the log in context.

### 4. Prompt the agent

Example prompt:

```
Use MCP to inspect the scene tree on game port 6789
```
