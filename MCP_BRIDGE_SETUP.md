# Blender MCP Bridge Setup Guide

Connect Claude Code to your local Blender installation to generate 3D models via MCP.

## Prerequisites

- Blender installed locally (with Python API support)
- Python 3.8+
- Claude Code or another MCP client

## Step 1: Find Your Blender Path

### macOS
```bash
which blender
# Usually: /Applications/Blender.app/Contents/MacOS/blender
```

### Windows
```cmd
where blender
# Usually: C:\Program Files\Blender Foundation\Blender X.XX\blender.exe
```

### Linux
```bash
which blender
# Usually: /usr/bin/blender
```

## Step 2: Test Blender Access

Verify Blender runs in headless mode:

```bash
blender -b -P --help
```

If this works, Blender is accessible.

## Step 3: Configure Claude Code

### Option A: Global MCP Configuration (Recommended)

**On macOS/Linux:**

Edit `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "blender": {
      "command": "python3",
      "args": ["/path/to/blender-mcp/blender_mcp_server.py"],
      "env": {
        "BLENDER_PATH": "/path/to/blender"
      }
    }
  }
}
```

**On Windows:**

Edit `%APPDATA%\.claude\settings.json`:

```json
{
  "mcpServers": {
    "blender": {
      "command": "python.exe",
      "args": ["C:\\path\\to\\blender-mcp\\blender_mcp_server.py"],
      "env": {
        "BLENDER_PATH": "C:\\Program Files\\Blender Foundation\\Blender X.XX\\blender.exe"
      }
    }
  }
}
```

### Option B: Project-Level Configuration

Create `.claude/settings.json` in your `blender-mcp` directory:

```json
{
  "mcpServers": {
    "blender": {
      "command": "python3",
      "args": ["./blender_mcp_server.py"],
      "env": {
        "BLENDER_PATH": "/your/blender/path/here"
      }
    }
  }
}
```

Replace `/path/to/blender` with your actual Blender executable path from Step 1.

## Step 4: Test the Connection

In Claude Code, run:

```bash
claude mcp list
```

You should see `blender` in the output.

## Step 5: Use It

Now you can generate 3D models from Claude Code sessions. Examples:

### Generate a Lunuff Character

```
@claude I need a Lunuff character model.
```

I'll call the `generate_lunuff` tool and create your character.

### Generate from Text Description

```
@claude Create a smooth sphere 100mm wide for 3D printing.
```

I'll parse your description and generate the model.

### Automatic Tool Selection

```
@claude Make a Lunuff with armor.
```

The unified router automatically:
1. Routes to Lunuff for the character
2. Routes to Text-to-CAD for the armor
3. Returns both models

## Troubleshooting

### "Blender not found"

**Problem:** Error says `Blender not found at: /path/to/blender`

**Solution:** Verify the path:
```bash
/path/to/blender -b --version
```

If it doesn't work, update `BLENDER_PATH` in your settings.

### "Script execution timed out"

**Problem:** Generation takes >60 seconds

**Cause:** Blender startup + generation is slow on first run

**Solution:** Increase timeout in `blender_mcp_server.py` line 51:
```python
timeout=120  # 2 minutes instead of 60 seconds
```

### MCP server won't start

**Problem:** `claude mcp list` doesn't show blender

**Solution:** Check stderr logs:
```bash
# In Claude Code terminal, look for error messages when the server tries to start
# Common issues:
# - Python path wrong (use full path, not `python`)
# - BLENDER_PATH not set or invalid
# - File permissions (make script executable: chmod +x blender_mcp_server.py)
```

### No models appearing

**Problem:** Models generated but no files saved

**Note:** Models generate in Blender's default output location:
- `~/blender-mcp/models/lunuff_character_*.stl`
- `~/blender-mcp/models/text_to_cad_*.stl`

Check these directories for outputs.

## Advanced: Customizing Tool Parameters

Edit the tool definitions in `blender_mcp_server.py` around line 138 to add more parameters.

Example - add material selection:
```python
{
    "name": "generate_lunuff",
    "description": "Generate a Lunuff character",
    "inputSchema": {
        "type": "object",
        "properties": {
            "scale": {"type": "number"},
            "material": {
                "type": "string",
                "enum": ["plastic", "resin", "metal"]
            }
        }
    }
}
```

## Testing Without Claude Code

You can test the server directly:

```bash
python3 blender_mcp_server.py
```

Then in another terminal, send a request:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}}' | python3 blender_mcp_server.py
```

## Performance Notes

- **First run:** ~10-15 seconds (Blender startup overhead)
- **Subsequent runs:** ~5-8 seconds per model
- **Memory:** Blender uses 500MB-2GB per process
- **Concurrency:** Processes run sequentially (one at a time)

For batch operations, each request waits for the previous to complete.

## What's Next

Once connected:

1. Generate Lunuff characters at different scales
2. Create custom objects with Text-to-CAD
3. Combine both for complex scenes
4. Export for 3D printing, rendering, or game engines

See `INTEGRATION_GUIDE.md` for advanced usage patterns.
